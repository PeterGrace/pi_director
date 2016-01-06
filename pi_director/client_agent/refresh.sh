!/bin/bash

export DISPLAY=":0"
WID=$(xdotool search --onlyvisible --class iceweasel|head -1)
if [[ $WID = "" ]]
then
        sudo service lightdm restart
        exit 0
fi
xdotool windowactivate ${WID}
xdotool key ctrl+F5
