#!/bin/bash
sudo apt install xserver-xorg vim python3-venv python3-pip htop python3-tk 
python3 -m venv env/ 

source env/bin/activate
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo python3 -m pip install -r requirements.txt 

