#!/bin/bash
echo "Starting digital frame"
export DISPLAY=:0
/usr/bin/python /opt/frame/frame.py >> /opt/frame/logs/frame.log &
PID=$( ps fax | grep -v grep | grep '/usr/bin/python /opt/frame/frame.py' | awk '{ print $1 }' ) # to do in less ugly way
echo $PID > /opt/frame/run/frame.pid
