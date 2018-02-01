#!/bin/bash
export DISPLAY=:0
while true; do
timeout 3 xloadimage /opt/frame/install/loading01.jpg &
sleep 2
timeout 3 xloadimage /opt/frame/install/loading02.jpg &
sleep 2
done
