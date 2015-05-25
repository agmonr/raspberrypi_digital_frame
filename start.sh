#!/bin/bash

cd /home/pi/
export DISPLAY=:0
x='xinit -nocursor :0 '
x='X :0'
$x &
$( which xset )dpms force off
$( which python ) frame.py
$( which pkill ) X
