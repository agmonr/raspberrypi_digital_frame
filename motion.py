#!/usr/bin/env python3
import os,time,datetime,cv2,subprocess,json,numpy,tkinter,croniter
from crontab import CronTab 
from random import randint
import picamera
import picamera.array
import sys
from datetime import datetime,timedelta
import logging

level    = logging.DEBUG
format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers = [logging.FileHandler('dframe.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)




"""
 The motion part was copy from this lovely projects:

 Lightweight Motion Detection using python picamera libraries.
 Requires a Raspberry Pi computer with a picamera module.
 This code is based on a raspberry pi forum post by user utpalc
 modified by Claude Pageau for this working example.

 This project can be used for further development
 and is located on GitHub at
 https://github.com/pageauc/picamera-motion
 For a full featured program see my GitHub pi-timolo project at
 https://github.com/pageauc/pi-timolo
"""



class motion:
  def __init__(self):
    self.threshold = 10  # How Much pixel changes
    self.sensitivity = 100  # How many pixels change
    self.streamWidth = 1280  # motion scan stream Width
    self.streamHeight = 800
    self.imageVFlip = True       # Flip image Vertically
    self.imageHFlip = True       # Flip image Horizontally


  def get_stream_array(self):
      """ Take a stream image and return the image data array"""
      with picamera.PiCamera() as camera:
          camera.resolution = (self.streamWidth, self.streamHeight)
          with picamera.array.PiRGBArray(camera) as stream:
              camera.vflip = self.imageVFlip
              camera.hflip = self.imageHFlip
              camera.exposure_mode = 'auto'
              camera.exposure_mode = 'night'
              camera.awb_mode = 'auto'
              camera.capture(stream, format='rgb')
              camera.close()
              return stream.array

  def display(self):
    with picamera.PiCamera() as camera:
      camera.vflip = self.imageVFlip
      camera.start_preview()
      time.sleep(10)


  def scan_motion(self):
      """ Loop until motion is detected """
      data1 = self.get_stream_array()
      for f in range(1,3):
          data2 = self.get_stream_array()
          for y in range(0, self.streamHeight,20):
              for x in range(0, self.streamWidth,20):
                  # get pixel differences. Conversion to int
                  # is required to avoid unsigned short overflow.
                  diff = abs(int(data1[y][x][1]) - int(data2[y][x][1]))
                  if diff > 50:
                    logging.debug(f' motion detected {diff}')
                    return (True)
          
          data1 = data2

      return (False)


