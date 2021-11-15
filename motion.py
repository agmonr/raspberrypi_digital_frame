#!/usr/bin/env python3
import os,time,datetime,cv2,subprocess,json,numpy,tkinter,croniter
from random import randint
import picamera
import picamera.array
import sys
from datetime import datetime,timedelta
from log import *
from pathlib import Path
from crontab import CronTab

from datetime import datetime
from datetime import timedelta
from crontab import CronTab
from croniter import croniter
from fractions import Fraction


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
    self.read_config()



  def read_config(self):
    try:
      f = open('motion.json',)
    except:
      logging.critical=('failed to load config file')
      sys.exit(2)
  
    try:
      data = json.load(f)
      self.captureRoot=           (data['config']['captureRoot'])
      self.xScanStep=             (data['config']['xScanStep'])
      self.yScanStep=             (data['config']['yScanStep'])
      self.streamWidth=           (data['config']['streamWidth'])
      self.streamHeight=          (data['config']['streamHeight'])
      self.numberOfMotions=       (data['config']['numberOfMotions'])
      self.scanTime=              (data['config']['scanTime'])
      self.xCaptureRes=           (data['config']['xCaptureRes'])
      self.yCaptureRes=           (data['config']['yCaptureRes'])
      self.sensitivity=           (data['config']['sensitivity'])
      self.highSensitivity=       (data['config']['highSensitivity'])
      self.highSensitivityHours=  (data['config']['highSensitivityHours'])
      self.numberOfMotionsHigh=   (data['config']['numberOfMotionsHigh'])
      self.images2Capture=        (data['config']['images2Capture'])
      self.xCaptureResVideo=      (data['config']['xCaptureResVideo'])
      self.yCaptureResVideo=      (data['config']['yCaptureResVideo'])
      self.captureRootVideo=      (data['config']['captureRootVideo'])
      self.captureVideoDuration=  (data['config']['captureVideoDuration'])


      f.close()
      self.imageVFlip=       True
    except ValueError:
      logging.critical('Decoding JSON has failed')

    return True
   
  def checkCron(self, cront):
    base = datetime.now()
    iter = croniter(cront, datetime.now())
    prev=(iter.get_prev(datetime)+timedelta(minutes=1))
    if base < prev:
      return True

    return False


  def get_stream_array(self):
      """ Take a stream image and return the image data array"""
      with picamera.PiCamera() as camera:
          camera.resolution = (self.streamWidth, self.streamHeight)
          with picamera.array.PiRGBArray(camera) as stream:
              camera.exposure_mode = 'night'
              camera.capture(stream, format='rgb')
              camera.close()
              return stream.array

  def display(self):
    with picamera.PiCamera() as camera:
      camera.vflip = self.imageVFlip
      camera.start_preview()
      time.sleep(10)

  def createPath(self, captureRoot, dirName):
      try:
        Path(f'{dirName}').mkdir(parents=True, exist_ok=True)
      except:
        logging.critical(f'failed to mkdir f{dirName}')
        sys.exit(2)

  def capture(self):
    logging.debug('motion.capture()')
    for f in range(1,self.images2Capture):
      with picamera.PiCamera() as camera:
        camera.vflip = self.imageVFlip
        camera.resolution = (self.xCaptureRes, self.yCaptureRes)

        if self.checkCron(self.highSensitivityHours) is True:
#          camera.framerate = Fraction(1, 20)
#          camera.shutter_speed = 200000
#          camera.exposure_mode = 'off'
#          camera.iso = 800
          camera.exposure_mode = 'night'
        else:
          camera.exposure_mode = 'auto'

        fileName=str(datetime.today().strftime("%H%M%S%f"))
        dirName=self.captureRoot+str(datetime.today().strftime("%Y%m%d"))

        try:
          self.createPath(self.captureRoot, dirName)
          print (self.captureRoot)
          print (dirName)
          camera.capture(f'{dirName}/{fileName}.jpg')

        except:
          logging.critical(f'failed to save image to f{dirName}/{fileName}')
          sys.exit(2)


  def captureVideo(self):
    logging.debug('motion.captureVideo()')
    dirName=self.captureRootVideo+str(datetime.today().strftime("%Y%m%d"))
    self.createPath(self.captureRootVideo, dirName)
    try:
      with picamera.PiCamera() as camera:
          camera.resolution = (self.xCaptureResVideo, self.yCaptureResVideo)
          fileName=str(datetime.today().strftime("%H%M%S%f"))
          camera.start_recording(f'{dirName}/{fileName}.h264')
          camera.wait_recording(self.captureVideoDuration)
          camera.stop_recording()
    except:
      logging.critical(f'failed to save video to f{dirName}/{fileName}')
      sys.exit(2)

  
    return True

  def scan_motion(self):
      """ Loop until motion is detected """
      logging.debug('motion.scan_motion()')
      data1 = self.get_stream_array()

      if self.checkCron(self.highSensitivityHours) is True:
        sensitivity=self.highSensitivity
        numberOfMotions=self.numberOfMotionsHigh
      else:
        sensitivity=self.sensitivity
        numberOfMotions=self.numberOfMotions


      dateLimit=datetime.now()+ timedelta(seconds=self.scanTime)
      while datetime.now() < dateLimit:
          diffShows=0
          data2 = self.get_stream_array()
          for y in range(0, self.streamHeight,self.xScanStep):
              for x in range(0, self.streamWidth,self.yScanStep):
                  # get pixel differences. Conversion to int
                  # is required to avoid unsigned short overflow.
                  diff = abs(int(data1[y][x][1]) - int(data2[y][x][1]))
                  if diff>sensitivity:
                    diffShows+=1 


          if (diffShows) >numberOfMotions:
            logging.debug(f'==== motion detacted {diffShows}')
            #self.capture() -> moved to the frame class
            return (diffShows)
          
          data1 = data2

      return (-1)

"""
for f in range (1,100):
  print (f)
  motion01=motion()
  motion01.scan_motion()
"""
