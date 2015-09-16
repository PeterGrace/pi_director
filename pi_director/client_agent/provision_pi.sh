#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

if [ -z "$1" ]; then
  echo "Downloading from GitHub."
  BASEURL="https://raw.githubusercontent.com/PeterGrace/pi_director/master/pi_director"
  USEPIFM=0
else
  echo "Downloading from provided PIFM server."
  BASEURL="${1}"
  USEPIFM=1
fi

###################################
# begin borrowing from raspi-config
raspicfg=$( which raspi-config )
eval "$( sed -n '/^disable_raspi_config_at_boot/,/^}/p' $raspicfg )"
eval "$( sed -n '/^disable_boot_to_scratch/,/^}/p' $raspicfg )"

echo -n "Waiting for ssh keys to generate"
while [ 1 ]; do
  sleep 1
  if [ -e /var/log/regen_ssh_keys.log ] && ! grep -q "^finished" /var/log/regen_ssh_keys.log; then
     echo -n "."
     continue
  else
     break
  fi
done
echo "."

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
  fi
else
  echo "lightdm not installed, cannot setup boot to desktop"
fi
# done borrowing from raspi-config
##################################

apt-get -y update
apt-get -y install unclutter xdotool matchbox-window-manager chromium python-pip imagemagick
wget $BASEURL/client_agent/xsession -O .xsession
wget $BASEURL/client_agent/keydown.sh
wget $BASEURL/client_agent/refresh.sh
wget $BASEURL/client_agent/frozen_screen_detect.sh
wget $BASEURL/client_agent/pifm_agent.py
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

if [ "$USEPIFM" -eq 1 ]; then
  echo "If everything worked properly, this should automatically reboot."
  sed -i "s#http://pi_director#${BASEURL}#" .xsession pifm_client.py
else
  echo "Don't forget to update the .xsession and pifm_client.py with the new PIFM."
fi

