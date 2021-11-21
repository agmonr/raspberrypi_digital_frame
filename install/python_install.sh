#!/bin/bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt 

Version=$( grep -c 'Raspbian GNU/Linux 10' /etc/issue )
if [ ${Version} == "1" ]; then 
	python3 -m pip install picamera==1.13
fi
