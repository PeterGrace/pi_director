#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

<% BASEURL= request.route_url('home')[:-1] %>

###################################
# begin borrowing from raspi-config
raspicfg=$( which raspi-config )
eval "$( sed -n '/^disable_raspi_config_at_boot/,/^}/p' $raspicfg )"
eval "$( sed -n '/^disable_boot_to_scratch/,/^}/p' $raspicfg )"

# enable ssh
update-rc.d ssh enable &&
invoke-rc.d ssh start &&

# setup boot-to-desktop
if [ -e /etc/init.d/lightdm ]; then
	if id -u pi > /dev/null 2>&1; then
		update-rc.d lightdm enable 2
		sed /etc/lightdm/lightdm.conf -i -e "s/^#autologin-user=.*/autologin-user=pi/"
		disable_boot_to_scratch
		disable_raspi_config_at_boot
	else
		echo "pi user removed, cannot setup boot to desktop"
		exit 1
	fi
else
	echo "lightdm not installed, cannot setup boot to desktop"
	exit 1
fi
# done borrowing from raspi-config
##################################

apt-get -y update
apt-get -y install unclutter xdotool matchbox-window-manager iceweasel python-pip imagemagick git lightdm
wget ${BASEURL}/client_agent/xsession -O .xsession
wget ${BASEURL}/client_agent/keydown.sh -O keydown.sh
wget ${BASEURL}/client_agent/refresh.sh -O refresh.sh
wget ${BASEURL}/client_agent/xdokey.sh -O xdokey.sh
wget ${BASEURL}/client_agent/frozen_screen_detect.sh -O frozen_screen_detect.sh
wget ${BASEURL}/client_agent/pifm_agent.py -O pifm_agent.py

chown pi.pi -R ~pi/.xsession ~pi/pifm_agent.py ~pi/keydown.sh ~pi/refresh.sh ~pi/frozen_screen_detect.sh
chmod a+x .xsession keydown.sh refresh.sh frozen_screen_detect.sh pifm_agent.py

mkdir /home/pi/src
cd /home/pi/src
git clone https://github.com/AndrewFromMelbourne/fb2png
cd fb2png
make
cp fb2png /home/pi/
cd /home/pi
pip install requests sh
chown pi:pi -R *

su pi -c 'echo -e "* * * * *\t/home/pi/pifm_agent.py >/dev/null 2>&1" | crontab'
echo "display_rotate=0" >> /boot/config.txt

echo "If everything worked properly, this pi automatically reboot soon."
sed -i "0,/def/ s#http://pi_director#${BASEURL}#" .xsession pifm_agent.py


