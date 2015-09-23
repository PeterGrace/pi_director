#!/usr/bin/env python
import os
import sys
import pickle
import requests
import json
import logging
import socket
import atexit
from sh import sudo

CACHE_FILE = "/home/pi/cache.pickle"
PIFM_HOST = "http://den-storno-itlin.ds.stackexchange.com:6543"
LOCK_DIR = "/dev/shm/pifm.lock"

logging.basicConfig(level=logging.INFO)


def release_lock():
    os.rmdir(LOCK_DIR)


def acquire_lock():
    try:
        # we are using a directory because that is an atomic operation
        os.mkdir(LOCK_DIR)
    except OSError:
        logging.info('PIFM Agent is already running according to: '+LOCK_DIR)
        sys.exit(0)

    atexit.register(release_lock)


def get_default_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    local_ip_address = s.getsockname()[0]
    return local_ip_address


def getmac(interface):
    try:
        mac = open('/sys/class/net/'+interface+'/address').readline()
    except:
        mac = "00:00:00:00:00:00"

    return mac[0:17]


# lock it up -- long-running arbitrary commands could hose us
acquire_lock()

# Initialize cache
original_cache={}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = {}

original_cache = cache.copy()
# Get mac address
mac = getmac('eth0')
ip = get_default_ip()

# Send ping to server
requests.get(PIFM_HOST+'/api/v2/ping/{mac}/{ip}'.format(mac=mac, ip=ip))

# push screenshot to server
sudo('/home/pi/fb2png', '-p', '/dev/shm/fb.png')
# /api/v1/screen/{macaddress}
filelist = {'screenshot': open('/dev/shm/fb.png', 'rb')}
img_response = requests.post(PIFM_HOST+'/api/v1/screen/{mac}'.format(mac=mac), files=filelist)

# Compare cache to newest results
r_newurl = requests.get(PIFM_HOST+'/api/v1/cache/{mac}'.format(mac=mac))
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

    # pifm server will unset the command(s) after results are sent
    if piurl['requested_commands']:
        def _reqcmd_resp(data=None, err=None):
            if err:
                return requests.post(PIFM_HOST+'/api/v2/reqcmds/{mac}'.format(mac=mac),
                                     json={'status': 'error', 'msg': str(err)})

            return requests.post(PIFM_HOST+'/api/v2/reqcmds/{mac}'.format(mac=mac),
                                 json={'status': 'OK', 'data': data})

        def _reqcmd():
            logging.info("Found arbitrary commands to run.")

            try:
                commands = json.loads(piurl['requested_commands'])
            except:
                logging.info("Didn't get acceptable json for requested commands.")
                return {'err': "pifm_client.py: malformed json for requested commands"}

            output = []

            for command in commands:
                tmpout = sudo(command['cmd'], *command['args'])
                output.append({'stdout': tmpout.stdout, 'stderr': tmpout.stderr})

            output = json.dumps(output)
            return {'data': output}

        _reqcmd_resp(**_reqcmd())
        del piurl['requested_commands']    # never cache this

except KeyError:
    logging.info("No previous url in cache, so, we're initializing it.")
    cache['url'] = piurl['url']
    cache['landscape'] = piurl['landscape']
    sudo('service', 'lightdm', 'restart')
    should_reboot = True


'''Commit cache to disk'''
if cmp(cache, original_cache) != False:
    with open(CACHE_FILE, "wb") as f:
        logging.info("Writing back changes to pickle")
        pickle.dump(cache, f)
else:
    logging.info("Cache is the same, not re-writing")

if should_reboot:
    sudo('reboot')

# vim: set expandtab tabstop=4 shiftwidth=4 autoindent smartindent: 