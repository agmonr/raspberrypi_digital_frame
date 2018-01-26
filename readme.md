# Python Digital Frame for Raspberry pi

The Raspberry pi digital frame is a python based digital frame. 

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
* Installing necessity python and system dependencies.
* Copy project files to /opt/frame/
* Register the application as services.

## Vagrant for dev
* Will also download some sample images.

## Services
* They are 2 main services: backend for configure and contolling the frame, and a frame which display the images and control the screen.




