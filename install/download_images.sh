#!/bin/bash
# The script will download some demo images.

curl https://digitalframedotblog.wordpress.com/raspberry-pi-digital-frame/ | grep -oh 'https://digitalframedotblog.files.wordpress.com/[0-9]\{4\}/[0-9]\{2\}/[^.]*' | sort | uniq > /tmp/images.txt
DIR=/home/Photos/
mkdir -p "$DIR"
cd "$DIR"

while read l; do
       	File=${DIR}$( echo $l | awk -F"/"  '{print $NF}' )".jpg"
	echo "checking $File"
	[[ ! -f $File ]] && echo "Downloding $l.jpg"; curl -s "$l.jpg" > $File 
	
done < /tmp/images.txt

service xserver start
service backend start
service frame start
