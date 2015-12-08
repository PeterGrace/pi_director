#!/bin/bash

export DISPLAY=":0"
WID=$(xdotool search --onlyvisible --class iceweasel|head -1)
xdotool windowactivate ${WID}
xdotool key ctrl+F5
