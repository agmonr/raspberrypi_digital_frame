#!/bin/bash

sudo apt -y update
sudo apt-get -y upgrade
sudo apt install -y vim mv git htop
sudo apt install -y xserver-xorg python3-venv python3-pip python3-tk 
sudo apt install -y  libjasper-dev libjasper-dev python3-pyqt5  libqt4-test libatlas-base-dev 


ln -s /root/raspberrypi_digital_frame/install/frame.service /etc/systemd/system/frame.service
systemctl daemon-reload
systemctl enable fra

mkdir ../logs/
python3 -m venv ../env/ 


source ../env/bin/activate
./python_install.sh

