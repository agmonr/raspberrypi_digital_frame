# Python Digital Frame for Raspberry pi
A python based digital frame with rest API and web interface. Wasn't build to security, DO NOT USE ON OPEN NETWORK!:)

## Highlights
Built to save power. The application is putting the screen on standby mode using the Raspberry pi tools to control the screen.
Using only a Raspberry pi, a memory card and a screen you can create a lovely digital photo frame, for the pleasure of your family. A great way to show some of the thousand of photos you never look at.
Can work offline.
Rest API server to control the settings.
Full install script on Raspberry pi (Debian 10)
Full dev env including Terraform settings files.
BASH Scripts examples to set the rest API.
Log file open on port 80 with links to the photos.
Doesn't have yet.
Cloud support. Should be set manually by the user.

## Requirements
Raspberry pi 2+ with a large memory card, virtual box and vagrant for dev.
For prod: a display set (a TV set might not be set on and off by the HDMI connection)

## main features
Displaying jpeg files at specific interval.
Settings can be configured and changed while the frame is on.
Current hour is added in the top left corner of the image being displayed.
The screen will be turned off in specific hours per weekday.
Can Check net connectivity and put mark on top of the photos.
How to install
Get a good power supply for the Raspberry pi and a nice screen. Follow the instruction on Raspberry web side and then come back to here.

Hi Again.

    git clone https://github.com/agmonr/raspberrypi_digital_frame.git
    cd raspberrypi_digital_frame/install
    sudo ./install.sh

and hope for good. 
You should have the software installed on '/opt/frame/'. 
The default photos folder is '/home/Photos/' 
The example scripts will set the screen for always on or off and some other stuff. 
You should have a few new services running now; take a look in the services folder. HAVE FUN.

## Vagrant for dev
Will also download some sample images.

