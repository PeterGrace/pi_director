- in raspi-config, enable ssh to pi
- in raspi-config, specify boot to desktop
- ssh into pi
- sudo apt-get -y update
- sudo apt-get -y install unclutter xdotool matchbox-window-manager chromium python-pip
- copy .xsession to ~pi
- copy keydown.sh to ~pi
- copy pifm_agent.py to ~pi
- sudo pip install requests (requests is needed for pifm_agent.py to work)
- sudo pip install sh (sh is used for pifm_agent)
- add crontab for pifm_agent.py to run every minute
- add display_rotate=0 to end of /boot/config.txt
- make sure url in .xsession and pifm_agent reflects the right instance of pifm you wish to talk to

-- At this point, when the crontab fires, it will automatically register the mac address into the configured web instance, with a default website of www.stackexchange.com.  From there, we can affect what is displayed.  

BEWARE -- the machine will reboot the first time as the cache gets proper settings saved.
