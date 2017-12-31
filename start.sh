#!/bin/bash

cd /home/pi/
export DISPLAY=:0
x='X -nocursor :0'
$x &
XPID=$$ 

/usr/bin/xset dpms force on
$( which python ) backend.py &
BPID=$$
sleep 1 #wating for server to start

$( which python ) frame.py; PID=$$


for f in $PID $BPID $ZPID; do 
  $( which pkill ) $f
done
