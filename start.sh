#!/bin/bash

cd /home/pi/
export DISPLAY=:0
x='X -nocursor :0 '
$x &
/usr/bin/xset dpms force off
$( which python ) frame.py
$( which pkill ) X
