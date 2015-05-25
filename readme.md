Small script to use your raspberrypi as Digital frame.
The Script was tested with version2, v1 might be too slow
The Script is under GPLv3.

Installtion:
use a freash installtion of Raspbian (testing with version 7)

install python image manipulation library

apt-get install python-opencv

Set the root folder where your photes are located in the config.py file

Copy frame.py, config.py and start.sh to the pi user home dir (/home/pi)
Set start.sh execaction:

chmod +x start.sh


add "su -c '/home/pi/start.sh' pi" to /etc/rc.local just before the "exit 0"


 

