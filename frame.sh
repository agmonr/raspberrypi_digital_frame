#!/usr/bin/env bash
export DISPLAY=:0
[[ "x$( pgrep X)" == "x" ]] && sudo /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
export LD_PRELOAD='/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 Object_detection_picamera.py'
sleep 1
while true; do 
	python3 ./frame.py
done

