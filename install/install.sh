#!/bin/bash

Version=$( grep -c 'Raspbian GNU/Linux 10' /etc/issue )
echo ${Version}

sudo apt -y update
sudo apt-get -y upgrade
sudo apt install -y vim uhubctl git htop
sudo apt install -y xserver-xorg python3-venv python3-pip python3-tk 
sudo apt install -y  libjasper-dev libjasper-dev python3-pyqt5  libqt4-test libatlas-base-dev 


ln -sf /root/raspberrypi_digital_frame/install/frame.service /etc/systemd/system/frame.service
systemctl daemon-reload
systemctl enable frame

mkdir ../logs/
python3 -m venv ../env/ 


source ../env/bin/activate
./python_install.sh

