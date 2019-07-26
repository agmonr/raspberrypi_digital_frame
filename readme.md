# Python Digital Frame for Raspberry pia

A python based digital frame with rest api and web interface. Wasn't build to security, DO NOT USE ON OPEN NETWORK!:)


# HighLights!
* Built to save power. The application is putting the screen on standby mode using the Raspberry pi tools to control the screen. (Doesn't work on tvs)
* Using only a Raspberry pia, a memory card and a screen you can create a lovely digital photo frame, for the pleasure of your family. A great way show some of the thousand of photos you never look at. 
* Using A real X server! to show the photos.
* User settings includes: 
``Weekly hours to show photos (when we are at home, most of the year)
``Weekly hours to dispaly the clock so people will know they really need to get going.
* Rest api server to control the settings.
* Can be set to display the same photo on multiple screens.
* Fully install script on Raspberry pia (Debian 10)
* Fully dev env including terraform script files.
* Scripts examles to set the rest api.
* Log file open on port 80


# Requirements
* Raspberry pi vagrant/.vagrant/SoC version 2 or 3.
* Tested on raspbian stretch.
* A display set (A tv set might not be set on and off by the hdmi connection)

## main features
* Dispalying jpg files at specfic interval.
* Settigns can be configured and changed while the frame is on.
* Current hour is added in the top left cornert of the image being display.
* The screen will be turn off in specfic hours per weekday.
* Can Check net connectivity and put mark on top of the photos.
* web interface shows the current image, can download it, turn screen on and off.

## install script
* use cd install; sudo ./install.sh script u
* Installing necessity python and system dependencies.
* Copy project files to /opt/frame/
* Register the application as services.

## Vagrant for dev
* Will also download some sample images.

## Services
* They are 2 main services: backend for configure and contolling the frame, and a frame which display the images and control the screen.




