#!/bin/bash
- Run `sudo raspi-config`, and enable these settings:
  - Enable SSH by going to `Advanced Options > SSH > Enable`
  - Enable boot to Desktop by going to `Enable Boot to Desktop/Scratch > Desktop Log in as user 'pi' at the graphical desktop`
  - Choose Finish and reboot the Pi when prompted

sudo apt-get -y update
sudo apt-get -y install unclutter xdotool matchbox-window-manager chromium python-pip imagemagick
wget https://raw.githubusercontent.com/PeterGrace/pi_director/master/client_agent/xsession -O .xsession
wget https://raw.githubusercontent.com/PeterGrace/pi_director/master/client_agent/keydown.sh
wget https://raw.githubusercontent.com/PeterGrace/pi_director/master/client_agent/refresh.sh
wget https://raw.githubusercontent.com/PeterGrace/pi_director/master/client_agent/frozen_screen_detect.sh
wget https://raw.githubusercontent.com/PeterGrace/pi_director/master/client_agent/pifm_agent.py
chmod a+x .xsession keydown.sh refresh.sh frozen_screen_detect.sh pifm_agent.py

mkdir ~/src
cd ~/src
git clone https://github.com/AndrewFromMelbourne/fb2png
cd fb2png
make
cp fb2png ~/
sudo pip install requests sh
echo -e "* * * * *\t/home/pi/pifm_agent.py >/dev/null 2>&1" | crontab 
echo "display_rotate=0" >> /boot/config.txt
