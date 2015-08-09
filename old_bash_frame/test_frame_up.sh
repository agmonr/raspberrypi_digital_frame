#!/bin/bash
Result=$( ps fax | grep -v grep | grep -e frame.sh )
if [ "$Result" == "" ]; then
	/home/frame/start.sh
fi
