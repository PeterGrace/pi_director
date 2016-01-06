#!/usr/bin/env python
import os
import sys
import re
import logging
from sh import (
    convert,
    xdotool,
    sudo
)

logging.basicConfig(level=logging.INFO)

border_colors = [
    {
        'red': 172,
        'green': 170,
        'blue': 164
    }
]

''' first we will refresh the screenshot '''
sudo('/home/pi/fb2png', '-p', '/dev/shm/fb.png')

''' then we will check the color of pixel 0,0 '''
output = convert('/dev/shm/fb.png', '-format', '%[pixel: u.p{0,0}]', 'info:')
regexp = "(?:(^.*?\((\d+),(\d+),(\d+)\)$)|(\S+))"
match = re.search(regexp, str(output))
if match is not None:
    if re.search('^srgb.*$', match.group(0)) is None:
        logging.info("we got a color instead of an srgb value.")
    else:
        point = {}
        point['red'] = int(match.group(2))
        point['green'] = int(match.group(3))
        point['blue'] = int(match.group(4))

        ''' if our color in 0,0 matches our known widget border color, then we think we're in windowed mode. '''
        if point in border_colors:
            logging.info("screen appears to be windowed, executing xdotool")
            new_env = os.environ.copy()
            new_env["DISPLAY"] = ":0"
            xdotool('key', 'F11', _env=new_env)
        else:
            logging.info("color doesn't match known window border color, assuming fullscreen.")
else:
    logging.info("convert did not produce output we would expect.  Output: {output}".format(output=output))
    sys.exit(1)
