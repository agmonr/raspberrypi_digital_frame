#!/bin/bash

sudo apt -y update
sudo apt-get -y upgrade
sudo apt install -y vim mv git htop
sudo apt install -y xserver-xorg python3-venv python3-pip python3-tk 
python3 -m venv env/ 

source env/bin/activate
./python_install.sh

