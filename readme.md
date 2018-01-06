# Python Digital Frame for Raspberry pi

The Raspberry pi digital frame is a python based digital frame. 

# Requirements
* Raspberry pi SoC version 2 or 3.
* Tested on raspbian stretch.
* A display set (A tv set might not be controlled via the hdmi connection)

## main features 
* Every featur can be configured and change will the frame is working.
* Dispalying jpg file at specfic interval.
* Adding the current hour on top of the photos being disply.
* Turning off and on the screen in spefic time.
* Checking net connectivity and set mark on top of the photos.

## install script
* Will install necessity python and system dependencies.
* Copy the files to /opt/frame/
* Register the application as services.

## Vagrant for dev
* Will also download some sample images.

## Services
* They are 2 services: backend for configure and contolling the frame, and a frame which display the images and control the screen.

## Todo
* adding a web interface.


