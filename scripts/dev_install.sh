#!/bin/bash
[[ "$USER" != "root" ]] && echo "This script should be run under root" && exit 2  
apt install -y python-pip python-opencv xserver-xorg
pip install --upgrade pip
pip install os time datetime pickle subprocess

