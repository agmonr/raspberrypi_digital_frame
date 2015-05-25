Small script to use your raspberrypi as Digital frame.
The Script was tested with version2, v1 might be too slow
The Script is licensed under GPLv3.

The script will display images from folder and subfolders in specifc time. It will resize the image acording to your config.
With supported monitors (most of the modern one, but not tv sets) it will power off the screen. 
It can add the local time in specifc hours (I am using it in the morining when every minute count, and it is great for the kids too)
The script is set to show images in serias. Usefull when your photos are sorted in folders or by date.
For best results, resize your photos acording to the screen size (I am using ufraw for raw images and digikam for jpgs)
You can show all images in greyscale.
The script was testing only with jpgs.


Installtion:
use a freash installtion of Raspbian (testing with version 7)

install python image manipulation library

apt-get install python-opencv

Set the root folder where your photes are located in the config.py file

Copy frame.py, config.py and start.sh to the pi user home dir (/home/pi)
Set start.sh execaction:

chmod +x start.sh


add "su -c '/home/pi/start.sh' pi" to /etc/rc.local just before the "exit 0"

You can stop the script using (under user pi):
	pkill python

and start it again using the start.sh (to kill it: pkill python; fg )




Todo:
Add web intreface:
	show displayed images 
	enable configuration. 

