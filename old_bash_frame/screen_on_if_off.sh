#!/bin/bash
if [ "$( /usr/bin/tvservice -s | fgrep -c 'progressive' )" == "1" ]; then exit 0; fi
/home/frame/screen_off.sh
/usr/bin/tvservice -p
sleep 5
/home/frame/start.sh &
sleep 5
/home/frame/start.sh &
