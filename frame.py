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
    print "self.day "+str(self.Day)
    hours=(requests.get(url+"/days/"+self.Day).json()["hours"][now.hour])
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
    print "Hours_on "+hours_on
    if hours_on=="1":
      self.tvservice_on()
      os.system('/opt/frame/show.py')  
      self.tvservice_off()

  def write_log(self,Text):
    print(time.strftime("%H:%M:%S ")+Text+"\n")
    f=open(LogFile,'a')
    f.write(time.strftime("%H:%M:%S ")+Text+"\n")
    f.close()

  def main(self):
    self.msg=""
    self.Hour=str(time.strftime("%H"))
    self.Day=int(datetime.datetime.today().weekday()+2)
    if self.Day > 7:
      self.Day=self.Day-7
    self.Day=str(self.Day)
    SleepTime=10
    while 1:
      self.check_on_off()
      time.sleep(SleepTime)  #You are going to sleep deeper and deeper
      if SleepTime < 120:
        SleepTime+=3


Frame01 = frame()


