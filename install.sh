#!/bin/bash
sudo apt install xserver-xorg vim python3-venv python3-pip htop python3-tk 
python3 -m venv env/ 

source env/bin/activate
./python_install.sh

