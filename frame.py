#!/usr/bin/env python3
import os,time,datetime,cv2,subprocess,json,numpy,tkinter,sys,array
from random import randint
from croniter import croniter
from datetime import datetime
from datetime import timedelta
from crontab import CronTab
from log import *


with open('/etc/issue') as f:
    if 'Raspbian GNU/Linux 10' in f.read():
        from motion import *
    else:
        print ("running not under Raspbian, camera will not work")



class frame:
  def __init__(self):

    root = tkinter.Tk()
    logging.debug('frame __init__' )
    self.read_config()
    logging.debug('frame __init__ read_config' )

    self.tvServiceBin=os.path.exists("/usr/bin/tvservice") 
    self.yscreenresulation=root.winfo_screenheight()
    self.xscreenresulation=root.winfo_screenwidth()
    logging.debug(f'self.xscreenresulation={self.xscreenresulation}, self.yscreenresulation=${self.yscreenresulation}' )
    self.lastMotion=datetime.now()
    self.startShow=datetime.now()
    self.List=[]
    self.msg=[" "," "]
    self.screenOn=True
    self.alone=False
    self.Shown=[]
    self.screenState=True #true to on
    for rootFolders in self.root:
      for path, subdirs, files in os.walk(rootFolders):
        for name in files:
          self.List.append(str(path)+"/"+str(name))

    logging.info("Total of "+str(len(self.List))+" images in "+str(self.root))

    self.List.sort()
    self.main()
        
  def read_config(self):
    f = open('frame.json',)
    data = json.load(f)
    self.root=(data['config']['Root'])
    self.hoursOn=(data['config']['hoursOn'])
    self.delay=(data['config']['Delay']) # delay between images 
    self.sleep=(data['config']['time2Sleep']) # seconds to go to sleep if no motion detected
    self.series=(data['config']['Series']) # Length of image series
    self.grayscale=(data['config']['Grayscale']) 
    self.show_half=(data['config']['ShowHalfHour'])
    self.showClock=(data['config']['clockOn'])
    self.scale=(data['config']['FontScale'])
    self.offsetx=(data['config']['offsetx'])
    self.offsety=(data['config']['offsety'])
    self.captureOn=(data['config']['captureOn'])
    self.captureVideo=(data['config']['captureVideo'])
    self.aloneMode=(data['config']['aloneMode'])


    self.stations=(data['networks']['stations'])


    self.camera=(data['config']['camera'])
    if self.camera=="True":
      self.camera=True
    else:
      self.camera=False

    self.check_net=0
    f.close()
    

  def tvserviceOff(self):
      logging.info('tvservice_off')
      self.screenState=False
      if self.getTvStatus() and self.tvServiceBin == True:
        os.system('sudo /usr/bin/tvservice -o') 

  def tvserviceOn(self):
      logging.info('tvservice_on')
      self.screenState=True
      if not self.getTvStatus() and self.tvServiceBin == True:
        os.system('sudo /usr/bin/tvservice -p')
        os.system('sudo /bin/chvt 2') #switch to another vt and back to make sure we catch X
        os.system('sudo /bin/chvt 1')

  def getTvStatus(self):
      if self.tvServiceBin is False:
          return True
      displayStatus=str(subprocess.run(['sudo','/usr/bin/tvservice','-s'], stdout=subprocess.PIPE))
      if 'TV is off' in displayStatus:
        self.screenState=False
        return False
      else:
        self.screenState=True
        return True
      



  def read_img(self):
    self.img=cv2.imread(self.FileName)
    if self.grayscale=="True": 
      self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)




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
    if self.checkCron(self.showClock):
      self.msg[0]=time.strftime("%H:%M")
      return True

    if self.show_half=="True" and (time.strftime("%M")=='30' or time.strftime("%M")=='00'):
       self.msg[0]=time.strftime("%H:%M")
       return True


    self.msg[0]=""
    return False



  def ping(self,host):
    command = ['ping', '-c', '1', host]
    return subprocess.call(command) == 0  



  def checkStations(self):
    if self.camera == False: #no need to check if there are people at home if no capture will be done
      return "False"
    for station in self.stations:
      for name, dnsName in station.items():
        if self.ping(dnsName):
          print (f'{name} is home')
          self.alone=False
          return False 
  
    logging.debug ("home alone") 
    self.alone=True
    return True



  def add_text(self,x=50,y=170):

    #font = cv2.FONT_HERSHEY_SIMPLEX 
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    try: 
      scale=int((self.img.shape[0]/self.yscreenresulation)*3)
    except:
      scale=5
    

    logging.debug (f'yscreenresulation={self.yscreenresulation} imgshape[0]={self.img.shape[0]} scale={scale}')
    org = (20, 100+scale*5) 
    thickness = int(scale)
    linecolor = (0,0,0)
    linethickness = int(scale*4)
    bodycolor = (170,255,255)
    bodythinkness = int(scale)
    msg=' '.join(self.msg)

    cv2.putText(self.img, msg, org, font, scale, linecolor, linethickness, cv2.LINE_AA) 
    cv2.putText(self.img, msg, org, font, scale, bodycolor, bodythinkness, cv2.LINE_AA) 



    
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



  def checkMotion(self):
    logging.debug("frame.checkMotion()")

    if self.camera is False:
      time.sleep(30)
      return True

    motion01=motion()
    if motion01.scan_motion()>0: 
      self.lastMotion=datetime.now()
      self.captureMotion()
      self.screenOn=True
      return True 

    return False

  def captureMotion(self):
    logging.debug("frame.captureMotion()")

    if self.checkCron(self.captureOn):
      motion01=motion()
      motion01.capture()

    if self.checkCron(self.captureVideo):
      motion01=motion()
      motion01.captureVideo()

    return True

  def checkOnOff(self):
    logging.debug('frame.checkOnOff()')

    if self.lastMotion< datetime.now() - timedelta(seconds=self.sleep):
      logging.debug(f'{self.lastMotion} {datetime.now()}')
      self.tvserviceOff()
      return False

    if self.checkCron(self.hoursOn) is True: 
       self.tvserviceOn()
       return True 
    else:
       self.tvserviceOff()
       return False 

  def checkCron(self, crons):
    base = datetime.now()
    for cront in crons:
      iter = croniter(cront, datetime.now())
      prev=(iter.get_prev(datetime)+timedelta(minutes=1))

      if base < prev:
        return True 

    return False


  def show(self):
    logging.debug('frame.show()')
    cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE )
    cv2.namedWindow("Frame", flags=cv2.WINDOW_GUI_NORMAL )
    self.img=self.image_resize(self.img, self.xscreenresulation, self.yscreenresulation)
    cv2.moveWindow("Frame", int((self.xscreenresulation-self.img.shape[1])/2+self.offsetx), int((self.yscreenresulation-self.img.shape[0])/2)+self.offsety)
    cv2.imshow("Frame",self.img)
    key=cv2.waitKey(1)
    return True


  def preShow(self):
    logging.debug(f'frame.preShow()')
    logging.info(f'{self.FileName}')

    if self.checkOnOff() == False or self.screenState == False:
      return False

    
    self.Hour=str(time.strftime("%H"))
    self.read_img()
    self.add_hour()
    self.add_text()
    self.show()
    return True


  def main(self):
    """
    If your pictures are sorted by name, they will be dispalied in a group.
    From a random point in file location, a group of {self.serires} will be 
    Dispalied. A way to keep memories togther
    """
    logging.debug('frame.main')
    if (len(self.List))<int(self.series): #when there are fewer images then {self.series}
      f=1
    else:
      f=randint(0,(len(self.List)-int(self.series)))
      logging.debug(f'random image start series {f}')

    count=0



    while 1:
      self.FileName=self.List[f]
      dateLimit=datetime.now()- timedelta(seconds=self.delay)
      self.preShow()

      if self.alone:
        self.captureOn=['* * * * *']
        self.captureVideOn=['* * * * *']
        self.hoursOn=['0 0 0 0 0']
    

      while self.startShow > dateLimit: #loop until pass self.delay seconds from last image show
        self.preShow()
        dateLimit=datetime.now()-timedelta(seconds=self.delay)
        logging.debug(f'waiting for {self.startShow} > {dateLimit}')

        if self.checkMotion() is True and self.checkOnOff() is False:
          self.screenState=True

        count+=1
        f+=1



      if self.checkCron(self.aloneMode):
        self.checkStations()

      self.read_config()
      self.startShow=datetime.now()


 
      if count>=int(self.series):
        count=0
        f=randint(0,len(self.List)-int(self.series)) 
        logging.debug(f'random image start series {f}')

Frame01 = frame()
