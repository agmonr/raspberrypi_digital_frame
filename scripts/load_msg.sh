#!/bin/bash
export DISPLAY=:0
while true; do
timeout 10 xloadimage /opt/frame/install/loading01.jpg &
sleep 7
timeout 10 xloadimage /opt/frame/install/loading02.jpg &
sleep 7
done
