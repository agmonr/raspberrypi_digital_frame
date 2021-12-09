Digital frame with motion detection

The aim of the project is to provide a pleasant way to show photos using raspberry pie.

When no motion is detected the screen will go off.

The installation was tested on Raspbian GNU/Linux 10 and probably won't work on other systems. Please enable the camera using the raspi-config util and set the screen resolution.

The dframe now support powering off and on the usb port if no onw at home. You may need to comile uhubctl (for rspi4) . (https://github.com/mvp/uhubctl#raspberry-pi-4b) 

installations:
cd /root/
git clone https://github.com/agmonr/raspberrypi_digital_frame.git
cd raspberrypi_digital_frame/install/
./install.sh


config files:
frame.json
    "Root": [ "/home/Photos/" ] # root folder to the images folders
    "hoursOn": [ "* 05-23 * * *"], # time for the screen should be on. crontab style.
    "clockOn": [ "* 6-8,17-20 * * 0-5", "* 6-8 * * 6" ], # when to show clock
    "camera": "True", #use the camera?
    "captureOn": ["* 22-23,0-6 * * *" ], #when to capture still images
    "captureVideo": ["* 22-23,0-6 * * *" ], # when to capture videos
    "Delay": 60, #delay between images
    "time2Sleep": 600, #time from last motion detected until putting the screen off
    "FontScale": 2, #size of fonts
    "Series": 100, #number of sequence images to show
    "offsetx": 0, 
    "offsety": -28,  
    "Grayscale": "False",
    "ShowHalfHour": "True" #show time every half hour and full hour



