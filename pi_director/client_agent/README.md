pi_director client agent
===========

# Automated Installation
If you would like to have the pi just set itself up automatically, execute this command:

`curl https://raw.githubusercontent.com/PeterGrace/pi_director/master/pi_director/client_agent/provision_pi.sh | sudo bash`

This will run the provision script that automates the commands below.


# Installation

- Run `sudo raspi-config`, and enable these settings:
  - Enable SSH by going to `Advanced Options > SSH > Enable`
  - Enable boot to Desktop by going to `Enable Boot to Desktop/Scratch > Desktop Log in as user 'pi' at the graphical desktop`
  - Choose Finish and reboot the Pi when prompted
- SSH into the Pi
- Run `sudo apt-get -y update`
- Then run `sudo apt-get -y install unclutter xdotool matchbox-window-manager chromium python-pip imagemagick`
- Copy the `.xsession` to `~/.xsession`
- Copy `keydown.sh` to `/home/pi`
- Copy `pifm_agent.py` to `/home/pi`
- Run `mkdir /home/pi/fb2png_source`, then `cd /home/pi/fb2png_source`
- Run `git clone https://github.com/AndrewFromMelbourne/fb2png`
- Run `make`, and then `cp fb2png /home/pi/fb2png`
- Install some Python libraries
  - `sudo pip install requests` (requests is needed for pifm_agent.py to work)
  - `sudo pip install sh` (sh is used for pifm_agent)
- Add crontab for pifm_agent.py to run every minute. Type `crontab -e`, then `* * * * * /usr/bin/python /home/pi/pifm_agent.py >/dev/null 2>&1` and save and close the file. 
- Run `sudo nano /boot/config.txt` and add display_rotate=0 to end
- Make sure the URL in `~/.xsession` and the variable `PIFM_HOST ` inside `/home/pi/pifm_agent.py` reflect the right URL instance of PIFM you wish to manage this Pi from.

-- At this point, when the crontab fires, it will automatically register the MAC address into the configured web instance, with a default website of www.stackexchange.com. From there, we can affect what is displayed.  

BEWARE -- the machine will reboot the first time as the cache gets proper settings saved.
