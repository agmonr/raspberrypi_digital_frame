#!/bin/bash
[[ "$USER" != "root" ]] && echo "This script should be run under root" && exit 2
mkdir -p /opt/frame/
if [ -d "/root/project" ]; then # we are in a vagrant box
	cp -rfv /root/project/* /opt/frame/
else
	cp -rfv ../* /opt/frame/ # we are probably running from git clone
fi
apt-get -y update
apt-get -y upgrade
apt-get install -y curl wget screen python-opencv xserver-xorg vim python-pip python-requests python-httplib2 mysql-server 
pip install --upgrade pip
pip install -r requirements.txt  

mysql -u root < create_user.sql 
mysql -u root < create_tables.sql


cd /opt/frame/
for f in /opt/frame/service/*; do 
  ln -s "$f" /etc/systemd/system/multi-user.target.wants/
done
systemctl daemon-reload

