#!/usr/bin/env python
import os
import pickle
import requests
import json
import logging
from sh import sudo

CACHE_FILE = "/home/pi/cache.pickle"
PIFM_HOST = "http://pi_director"

logging.basicConfig(level=logging.INFO)

def getmac(interface):

    try:
        mac = open('/sys/class/net/'+interface+'/address').readline()
    except:
        mac = "00:00:00:00:00:00"

    return mac[0:17]


'''Initialize cache'''
original_cache={}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = {}

original_cache = cache.copy()
'''Get mac address'''
mac = getmac('eth0')

'''Send ping to server'''
requests.get(PIFM_HOST+'/api/v1/ping/{mac}'.format(mac=mac))

'''push screenshot to server'''
sudo('/home/pi/fb2png','-p','/dev/shm/fb.png')
# /api/v1/screen/{macaddress}
filelist = { 'screenshot': open('/dev/shm/fb.png','rb') }
img_response = requests.post(PIFM_HOST+'/api/v1/screen/{mac}'.format(mac=mac),
                            files=filelist)

'''Compare cache to newest results'''
r_newurl = requests.get(PIFM_HOST+'/ajax/PiUrl/{mac}'.format(mac=mac))
piurl = json.loads(r_newurl.text)

try:
    if piurl['url'] != cache['url']:
        logging.info("New URL requested, restarting lightdm")
        sudo('service', 'lightdm', 'restart')
        cache['url'] = piurl['url']
    else:
        logging.info("URL same as last time, nothing to see here")

    if piurl['landscape'] != cache['landscape']:
        cache['landscape'] = piurl['landscape']
        if piurl['landscape'] == True:
            logging.info("Landscape mode requested, setting rotate to 0")
            sudo('sed', '-i', 's/display_rotate.*/display_rotate=0/g',
                 '/boot/config.txt')
            should_reboot = True
        else:
            logging.info("Portrait mode requested, setting rotate to 3")
            sudo('sed', '-i', 's/display_rotate.*/display_rotate=3/g',
                 '/boot/config.txt')
            should_reboot = True
    else:

        should_reboot = False
except KeyError:
    logging.info("No previous url in cache, so, we're initializing it.")
    cache['url'] = piurl['url']
    cache['landscape'] = piurl['landscape']
    sudo('service', 'lightdm', 'restart')
    should_reboot = True


'''Commit cache to disk'''
if cmp(cache,original_cache) != False:
    with open(CACHE_FILE, "wb") as f:
        logging.info("Writing back changes to pickle")
        pickle.dump(cache, f)
else:
    logging.info("Cache is the same, not re-writing")

if should_reboot:
    sudo('reboot')

