#!/usr/bin/env bash
killall X
killall Xorg

cd /root/raspberrypi_digital_frame/ 

echo "=== activting python ver env"
source env/bin/activate

while true; do
  echo
  echo
  echo "=== setting vars"
  export DISPLAY=:0
  export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
  export
  echo
  echo
  echo "=== and there will be X"
  /usr/bin/tvservice -p
  nohup /usr/bin/X vt1 -s 0 -nolock -nocursor -dpms 2>&1 >> /dev/null &
  echo "=== time to sleep a bit"
  sleep 2
  echo "=== Starting frame.py !"
  python3 ./frame.py
done

