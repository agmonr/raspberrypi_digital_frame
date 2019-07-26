# Python Digital Frame for Raspberry pi

A python based digital frame with rest api and web interface. Wasn't build to security, DO NOT USE ON OPEN NETWORK!:)


# HighLights!
* Built to save power. The application is putting the screen on standby mode using the Raspberry pi tools to control the screen.
* Using only a Raspberry pia, a memory card and a screen you can create a lovely digital photo frame, for the pleasure of your family. A great way show some of the thousand of photos you never look at. 
* Can work offline.
* Rest api server to control the settings.
* Full install script on Raspberry pi (Debian 10)
* Full dev env including terraform settings files.
* BASH Scripts examples to set the rest api.
* Log file open on port 80 with links to the photos.

# DOESN"T HAVE YET
* Cloud support. Should be set manulay by the user.

# Requirements
* Raspberry pi 2+ with a large memory card and for prod, virtual box and vagreant for dev.
* A display set (A tv set might not be set on and off by the hdmi connection)

## main features
* Dispalying jpg files at specfic interval.
* Settigns can be configured and changed while the frame is on.
* Current hour is added in the top left cornert of the image being display.
* The screen will be turn off in specfic hours per weekday.
* Can Check net connectivity and put mark on top of the photos.

## How to install
Get a good power supply for the Raspberry pie and a nice screen. Follow the instrucation on Raspbery pie web side and then come back to here.

Hi Again.

    git clone https://github.com/agmonr/raspberrypi_digital_frame.git
    cd raspberrypi_digital_frame/install
    sudo ./install.sh
    
 and hope for good.
 If everything will work good, you should have the software installed on /opt/frame/.
 The example scripts can set the screen for always on or off.
 You sould have a few new services running now take a look in the services folder.
 HAVE FUN.

## Vagrant for dev
* Will also download some sample images.
