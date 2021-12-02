#!/usr/bin/env bash
killall X
killall Xorg

cd /root/raspberrypi_digital_frame/ 

echo "=== activting python ver env"
source env/bin/activate
echo
echo
echo "=== setting vars"
export DISPLAY=:0
export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
export
echo
echo
echo "=== some flicking"
chvt 2
chvt 1
echo "=== and there will be X"
nohup /usr/bin/X vt1 -nolock -nocursor :0 -s 14400 &
echo "=== time to sleep a bit"
sleep 2
echo "=== Starting frame.py !"
python3 ./frame.py

