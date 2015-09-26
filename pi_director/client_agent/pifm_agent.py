#!/usr/bin/env python
import os
import subprocess
import sys
import pickle
import requests
import json
import logging
import socket
import atexit
from sh import sudo

CACHE_FILE = "/home/pi/cache.pickle"
PIFM_HOST = "http://pi_director"
LOCK_DIR = "/dev/shm/pifm.lock"
should_reboot = False

logging.basicConfig(filename='/dev/shm/pi_director.log',
                    level=logging.INFO,)
# http://stackoverflow.com/questions/13733552/
# logging.getLogger().addHandler(logging.StreamHandler())


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
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address sends no packets
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
original_cache = {}
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
img_response = requests.post(PIFM_HOST+'/api/v1/screen/{mac}'.format(mac=mac),
                             files=filelist)

# Compare cache to newest results
r_newurl = requests.get(PIFM_HOST+'/api/v1/cache/{mac}'.format(mac=mac))
piurl = json.loads(r_newurl.text)

try:

    # Set URL
    if piurl['url'] != cache['url']:
        logging.info("New URL requested, restarting lightdm")
        sudo('service', 'lightdm', 'restart')
        cache['url'] = piurl['url']
    else:
        logging.info("URL same as last time, nothing to see here")

    # Set Orientation
    if 'orientation' not in cache.keys():

        # Left for compaitibility with landscape checkbox 9/25/15
        logging.info("orientation not in keys, using landscape")
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
    else:
        logging.info("orientation key found, using orientation")

        if piurl['orientation'] != cache['orientation']:
            cache['orientation'] = piurl['orientation']
            logging.info('Orientation update requested, added to cache.')

            if piurl['orientation'] == 0:
                logging.info("orientation change, setting rotate to 0")
                sudo('sed', '-i', 's/display_rotate.*/display_rotate=0/g',
                     '/boot/config.txt')
                should_reboot = True
            if piurl['orientation'] == 90:
                logging.info("orientation change, setting rotate to 1")
                sudo('sed', '-i', 's/display_rotate.*/display_rotate=1/g',
                     '/boot/config.txt')
                should_reboot = True
            if piurl['orientation'] == 180:
                logging.info("orientation change, setting rotate to 2")
                sudo('sed', '-i', 's/display_rotate.*/display_rotate=2/g',
                     '/boot/config.txt')
                should_reboot = True
            if piurl['orientation'] == 270:
                logging.info("orientation change, setting rotate to 3")
                sudo('sed', '-i', 's/display_rotate.*/display_rotate=3/g',
                     '/boot/config.txt')
                should_reboot = True
        else:
            should_reboot = False

    # pifm server will unset the command(s) after results are sent
    if piurl['requested_commands']:
        cmd_url = PIFM_HOST+'/api/v2/reqcmds/{mac}'.format(mac=mac)

        def _reqcmd_resp(data=None, err=None):
            if err:
                return requests.post(cmd_url,
                                     json={'status': 'error', 'msg': str(err)})

            return requests.post(cmd_url,
                                 json={'status': 'OK', 'data': data})

        def _reqcmd():
            logging.info("Found arbitrary commands to run.")

            try:
                commands = json.loads(piurl['requested_commands'])
            except:
                logging.info("jsonnot acceptable for requested commands.")
                return {'err': "pifm_client.py: malformed json for  commands"}

            output = []

            for command in commands:
                tmpout = sudo(command['cmd'], *command['args'])
                output.append({'stdout': tmpout.stdout,
                              'stderr': tmpout.stderr})

            output = json.dumps(output)
            return {'data': output}

        _reqcmd_resp(**_reqcmd())
        del piurl['requested_commands']    # never cache this

except Exception, e:
    logging.info('Exception found: '+str(e))
    cache['url'] = piurl['url']
    cache['landscape'] = piurl['landscape']
    sudo('service', 'lightdm', 'restart')
    should_reboot = True


# Push logs to Server
# Compare cache to current
logdir = '/var/log/'
logfiles = ['/dev/shm/pi_director.log', logdir+'daemon.log',
            logdir+'debug', logdir+'messages',
            logdir+'kern.log', logdir+'syslog',
            logdir+'daily.out']
log_offset = '524288'  # Byes of log to send

for logfile in logfiles:
    post_needed = False
    if os.path.isfile(logfile):
        command = ['tail', '-c', log_offset, logfile]
        log_tail = subprocess.check_output(command)
        if logfile not in cache.keys():
            cache[logfile] = log_tail
            post_needed = True
        if log_tail != cache[logfile]:
            cache[logfile] = log_tail
            post_needed = True
        else:
            logging.info("No change detected in "+str(logfile))

        if post_needed:
            payload = {'pi_log': log_tail, 'filename': logfile}
            file_response = requests.post(PIFM_HOST+'/api/v1/pi_log/'+mac,
                                          data=payload)
            logging.debug(file_response)
# Send if changed

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
