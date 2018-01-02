#!/bin/bash

cd /home/pi/
export DISPLAY=:0
/usr/bin/xxset s off
/usr/bin/xset dpms force on
x='X -nocursor :0'
$x &
XPID=$$ 


[ ! "$( lsof -i :5000 )" ] && $( which python ) backend.py &
BPID=$$
sleep 1 #wating for server to start

$( which python ) frame.py; PID=$$

for f in $PID $BPID $ZPID; do 
  $( which pkill ) $f
done
