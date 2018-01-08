#!/bin/bash

DEST='/opt/frame/'

[[ "$USER" != "root" ]] && echo "This script should be run under root" && exit 2
mkdir -p /opt/frame/
if [ -d "/root/project" ]; then # we are in a vagrant box
	cp -rfv /root/project/* "${DEST}"
else
	cp -rfv ../* "${DEST}" # we are probably running from git clone
fi
apt-get -y update
apt-get -y upgrade
apt-get install -y curl\
  wget\
  vim\
  screen\
  python-opencv\
  python-pip\
  python-requests\
  python-httplib2\
  xserver-xorg\
  mysql-server 

pip install --upgrade pip
pip install -r "${DEST}"install/requirements.txt  

mysql -u root < "${DEST}"install/create_user.sql 
mysql -u root < "${DEST}"install/create_tables.sql

for f in "${DEST}"/service/*; do 
  ln -sf "$f" /etc/systemd/system/multi-user.target.wants/
done
systemctl daemon-reload

