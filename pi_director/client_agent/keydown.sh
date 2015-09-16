#!/usr/bin/env bash
export DISPLAY=:0
while (true)
do
        xdotool keydown Shift_L keyup Shift_L
        sleep 30
done

