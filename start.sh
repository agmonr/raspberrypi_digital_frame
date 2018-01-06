#!/bin/bash

export DISPLAY=:0
/usr/bin/xset s off
/usr/bin/xset dpms force on
#[ ! "$( lsof -i :5000 )" ] && $( which python ) backend.py &
#BPID=$$
#sleep 1 #wating for server to start

#$( which python ) frame.py; PID=$$

#for f in $PID $BPID $ZPID; do 
#  $( which pkill ) $f
#done
