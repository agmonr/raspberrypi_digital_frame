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
  x11-utils\
  wget\
  vim\
  screen\
  python-opencv\
  python-pip\
  python-requests\
  python-httplib2\
  xserver-xorg\
  python-cairo-dev\
  mariadb-server-10.0\
  nginx\
  xloadimage

/usr/bin/pip install --upgrade pip

 /usr/local/bin/pip install -r "${DEST}"install/requirements.txt; RESULT=$?
if [ "$RESULT" != "0" ]; then
    echo "Error installing python dependencies. exiting"
    exit 2
fi

mysql -u root < "${DEST}"install/create_tables.sql
mysql -u root < "${DEST}"install/create_user.sql 
mysqladmin reload 

for f in "${DEST}"service/*; do 
    echo ${f}
  ln -sf "$f" /etc/systemd/system
  systemctl daemon-reload
  systemctl enable ${f}
done

ln -sf "${DEST}"/service/show.service /etc/systemd/system/show.service 

systemctl daemon-reload
rm /etc/nginx/sites-enabled/default
ln -s /opt/frame/install/nginx/default /etc/nginx/sites-enabled/default 

rm -rf /var/www/
ln -sf /opt/frame/www/ /var/
ln -sf /home/Photos/ /opt/frame/www/

cp "${DEST}"/install/.vimrc /root/
service nginx restart

