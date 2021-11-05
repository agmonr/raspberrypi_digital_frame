#!/usr/bin/env bash
cd /root/raspberrypi_digital_frame/ 
export DISPLAY=:0
killall X
killall Xorg
#[[ "x$( pgrep X)" == "x" ]] && sudo /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
sudo /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
sleep 3
while true; do 
	python3 ./frame.py
done

