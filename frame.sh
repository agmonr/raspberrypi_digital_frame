#!/usr/bin/env bash
killall X
killall Xorg

cd /root/raspberrypi_digital_frame/ 
source env/bin/activate
export DISPLAY=:0
#[[ "x$( pgrep X)" == "x" ]] && sudo /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
sudo /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
sleep 3
python3 ./frame.py

