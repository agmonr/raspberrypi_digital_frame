#!/usr/bin/env python3
import os,time,datetime,cv2,subprocess,json,numpy,tkinter,croniter
from crontab import CronTab 
from random import randint
import picamera
import picamera.array
import sys
from datetime import datetime,timedelta

types=['jpg','jpeg','JPG','JPEG']
xset=os.path.exists("/usr/bin/xset")

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


  def check(self):
    return(self.scan_motion())


  def get_stream_array(self):
      """ Take a stream image and return the image data array"""
      with picamera.PiCamera() as camera:
          camera.resolution = (self.streamWidth, self.streamHeight)
          with picamera.array.PiRGBArray(camera) as stream:
              camera.vflip = self.imageVFlip
              camera.hflip = self.imageHFlip
              camera.exposure_mode = 'auto'
              camera.awb_mode = 'auto'
              camera.capture(stream, format='rgb')
              camera.close()
              return stream.array



  def scan_motion(self):
      """ Loop until motion is detected """
      data1 = self.get_stream_array()
      while True:
          data2 = self.get_stream_array()
          diff_count = 0
          for y in range(0, self.streamHeight):
              for x in range(0, self.streamWidth):
                  # get pixel differences. Conversion to int
                  # is required to avoid unsigned short overflow.
                  diff = abs(int(data1[y][x][1]) - int(data2[y][x][1]))
#                  print (f'diff',end=" " )
                  print (f'{diff}')

                  
                  return (diff)
          
          data1 = data2





class frame:
  def __init__(self):

    self.tvServiceBin=os.path.exists("/usr/bin/tvservice") 
    print (self.tvServiceBin)
    self.read_config()    
    self.write_log("------------")
    self.write_log("* Starting *")
    
    self.write_log("* finish importing config *")
    self.tvservice_on()
    root = tkinter.Tk()
    self.xscreenresulation=root.winfo_screenheight()
    self.yscreenresulation=root.winfo_screenwidth()
    
    self.write_log("* finish importing config *")
    #self.import_config_state()
    self.List=[]
    self.lastMotion=datetime.utcnow()
    self.screenOn=True
    self.Shown=[]
    for path, subdirs, files in os.walk(self.root):
      self.write_log(str(path))
      for name in files:
        self.List.append(str(path)+"/"+str(name))

    self.write_log("Total of "+str(len(self.List))+" images in "+str(self.root))
    self.List.sort()
    self.main()
        
  def read_config(self):
    f = open('config.json',)
    data = json.load(f)
    self.LogFile=(data['config']['LogFile'])
    self.root=(data['config']['Root'])
    self.hoursOn=(data['config']['hoursOn'])
    self.hoursOff=(data['config']['hoursOff'])
    self.delay=(data['config']['Delay'])
    self.series=(data['config']['Series'])
    self.grayscale=(data['config']['Grayscale'])
    self.show_half=(data['config']['ShowHalfHour'])
    self.showClock=(data['config']['clockOn'])
    self.scale=(data['config']['FontScale'])
    self.check_net=0
    f.close()
    

  def tvservice_off(self):
      if self.getTvStatus() and self.tvServiceBin == True:
        os.system('sudo /usr/bin/tvservice -o')  

  def tvservice_on(self):
      if not self.getTvStatus() and self.tvServiceBin == True:
        os.system('sudo /usr/bin/tvservice -p')
        os.system('sudo /bin/chvt 2')
        os.system('sudo /bin/chvt 1')

  def getTvStatus(self):
      if self.tvServiceBin is False:
          return True
      displayStatus=str(subprocess.run(['sudo','/usr/bin/tvservice','-s'], stdout=subprocess.PIPE))
      if 'TV is off' in displayStatus:
        return False
      else:
        return True
      

  def write_log(self,Text):
    print(time.strftime("%H:%M:%S ")+Text+"\n")
    f=open(self.LogFile,'a')
    f.write(time.strftime("%H:%M:%S ")+Text+"\n")
    f.close()

  def read_img(self):
    self.img=cv2.imread(self.FileName)
    self.write_log(self.FileName+" "+str(self.img.shape))  
    if self.grayscale=="True": 
      self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

  def show(self):
    cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE )
    self.img=self.image_resize(self.img, self.yscreenresulation, self.xscreenresulation)
    cv2.moveWindow("Frame", int((self.yscreenresulation-self.img.shape[1])/2), int((self.xscreenresulation-self.img.shape[0])/2))
    cv2.imshow("Frame",self.img)
    for f in range(0, int(self.delay)):
      key=cv2.waitKey(1)
      self.motionCheck()

  def motionCheck(self):
    motion01=motion()
    check=motion01.check()
    if check>10:
      motion01.display()
      self.lastMotion=datetime.utcnow()


  def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    #dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    w2 = int (( height / float(h) ) * w)
    #dim_width = (width, int(h * r))
   
    h2 = int (( width / float (w) ) * h )
#    dim_height = (int(w * r), height)
#    print (dim_height)

    if w2 < width :
        h2 = height
    else:
        w2 = width

    # resize the image
    return cv2.resize(image, ( w2, h2))

  def add_hour(self):  # Adding hour to displayed image
    hoursClock= CronTab(self.showClock)
    
    print (hoursClock.previous())
    if (hoursClock.previous()>-3600):
      self.msg=time.strftime("%H:%M")
      self.add_text()
      return

    if self.show_half=="1" and (time.strftime("%M")=='30' or time.strftime("%M")=='00'):
       self.msg=time.strftime("%H:%M")
       self.add_text()
  
  def check_net(self): #Check internet connection
    Status=subprocess.Popen("/bin/ping -c1 -w2 " +str (Net_target), shell=True, stdout=subprocess.PIPE).stdout.read()
    if Status.find ('100% packet loss') > 0:
      self.msg=":( "+self.msg
      self.add_text()

  def add_text(self,x=50,y=170):
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    # org 
    scale=self.scale
    fontScale = scale
    org = (20, 100+scale*15) 
    # fontScale 
    # Line thickness of 2 px 
    thickness = int(scale)
    linecolor = (0,0,0)
    linethickness = int(scale)
    bodycolor = (170,255,255)
    bodythinkness = int(scale)

    # Using cv2.putText() method
    #  cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA)  
    cv2.putText(self.img, self.msg, org, font, fontScale, linecolor, linethickness, cv2.LINE_AA) 
    cv2.putText(self.img, self.msg, org, font, fontScale, bodycolor, bodythinkness, cv2.LINE_AA) 


  def check_on_off(self):
    hoursOn= CronTab(self.hoursOn)
    hoursOff= CronTab(self.hoursOff)
    if (hoursOn.previous()<hoursOff.previous()):
        self.tvservice_off()
        return False
    else:
       self.tvservice_on()
       return True 
    
  def write_log(self,Text):
    print(time.strftime("%H:%M:%S ")+Text+"\n")
    f=open(self.LogFile,'a')
    f.write(time.strftime("%H:%M:%S ")+Text+"\n")
    f.close()

  def write_history_html(self,Text):
    FileName=Text.replace("/home/","")
    History=[]
    History.append(str(time.strftime("<p>%H:%M:%S ")+"<a href="+FileName+" download link>"+FileName+"</a></font></center></p>\n"))
    try:
      with open(HistoryFile) as f:
        for g in range(0,100):
         Line=f.readline()
         if len(Line)>1:
           History.append(str(Line))
      f.close()
    except:
      print ( "Starting new file" )

    f=open(HistoryFile,'w') 
    for g in range(0,len(History)):
      f.write(str(History[g]))
    f.close()

  def display(self):
    if self.check_on_off():
      self.msg=""
      self.Hour=str(time.strftime("%H"))
      self.read_img()
      self.add_hour()
      self.show()

  def main(self):
    count=0
    if (len(self.List))<int(self.series):
      f=1
    else:
      f=randint(0,(len(self.List)-int(self.series)))

    while 1:
      self.FileName=self.List[f]
      past=datetime.utcnow() - timedelta(minutes=60)
      print (self.lastMotion)
      print (past)
      if self.lastMotion>past:
        self.tvservice_on()
        print ('display')
        self.display()
      else:
        print (self.lastMotion)
        self.tvservice_off()
        print ('not display')
        self.motionCheck()
      count+=1
      f+=1
      if count>=int(self.series):
        count=0
        f=randint(0,len(self.List)-self.series)

Frame01 = frame()
