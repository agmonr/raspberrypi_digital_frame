#!/bin/bash

cd /home/pi/
export DISPLAY=:0
x='xinit -nocursor /etc/X11/xinit/xinitrc :0 '
x='X :0'
$x &
xset dpms force standby
python frame.py
pkill X
