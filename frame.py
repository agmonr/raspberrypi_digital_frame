#!/usr/bin/python
import sys,os,time,datetime,subprocess,json,urllib2,requests,httplib2
from random import randint

url="http://localhost:5000"
xset=os.path.exists("/usr/bin/xset")
tvservice=os.path.exists("/usr/bin/tvservice")
LogFile="/opt/frame/log/frame.log"

class frame:
  def __init__(self):
    self.write_log("------------")
    self.write_log("* Starting *")
    self.write_log("* finish importing config *")
    self.main()

  def get_hours_on(self):
    now=datetime.datetime.now()
    hours=(requests.get(url+"/days/"+self.day).json()["hours"][now.hour])
    return hours 
  
  def tvservice_off(self):
    os.system('service xserver stop')
    if tvservice:
      print "Tvservice off"
      os.system('/usr/bin/tvservice -o')  

  def tvservice_on(self):
    os.system('service xserver start')
    if tvservice:
      print "Tvservice on"
      os.system('/usr/bin/tvservice -p')  


  def check_on_off(self):
    hours_on=self.get_hours_on()
    if hours_on=="1":
      self.tvservice_on()
      os.system('service show start')
      self.tvservice_off()

  def write_log(self,Text):
    print(time.strftime("%H:%M:%S ")+Text+"\n")
    f=open(LogFile,'a')
    f.write(time.strftime("%H:%M:%S ")+Text+"\n")
    f.close()

  def main(self):
    self.msg=""
    self.Hour=str(time.strftime("%H"))
    self.day=int(datetime.datetime.today().weekday()+2)
    if self.day > 7:
      self.day=self.day-7
    self.day=str(self.day)
    Sleep=10
    while 1:
      self.check_on_off()
      time.sleep(Sleep)
      if Sleep < 120:
        Sleep+=3
    
Frame01 = frame()


