#!/usr/bin/python
import sys,cv2,os,time,datetime,pickle,subprocess,json,urllib2,requests,httplib2
from random import randint

types=['jpg','jpeg','JPG','JPEG']
url="http://localhost:5000"
xset=os.path.exists("/usr/bin/xset")
tvservice=os.path.exists("/usr/bin/tvservice")
LogFile="/opt/frame/log/frame.log"

class frame:
  def __init__(self):
    self.write_log("------------")
    self.write_log("* Starting *")
    self.update_rest("/config/10", {"id":'10', "key":'reread', "value": 'true' } )
    self.import_config()
    self.write_log("* finish importing config *")
    self.import_config_state()
    self.List=[]
    self.Shown=[]
    for path, subdirs, files in os.walk(self.root):
      self.write_log(str(path))
      for name in files:
        self.List.append(unicode(path)+"/"+unicode(name))

    self.write_log("Total of "+str(len(self.List))+" images in "+str(self.root))
    self.List.sort()
    self.main()

  def import_config_state(self):
    self.yscreenresulation=int(requests.get(url+"/config/4").json()["value"])
    self.xscreenresulation=int(requests.get(url+"/config/3").json()["value"])

  def check_import_config(self):
    reread=requests.get(url+"/config/10").json()["value"]
    print reread
    if reread=="true":
        print "Importig config"
        self.import_config
        self.update_rest("/config/10", {"id":'10', "key":'reread', "value": 'false' } )

  def import_config(self):
    self.root=requests.get(url+"/config/1").json()["value"]
    self.delay=int(requests.get(url+"/config/2").json()["value"])
    self.series=requests.get(url+"/config/5").json()["value"]
    self.grayscale=requests.get(url+"/config/6").json()["value"]
    self.show_half=requests.get(url+"/config/7").json()["value"]
    #self.check_net=(requests.get(url+"/config/8").json()["value"])
    self.check_net=0
    
  def get_hours_on(self):
    now=datetime.datetime.now()
    print "self.day "+str(self.Day)
    hours=(requests.get(url+"/days/"+self.Day).json()["hours"][now.hour])
    return hours 
  
  def get_hours_show(self):
    now=datetime.datetime.now()
    hours=(requests.get(url+"/h_display/"+self.Day).json()["hours"][now.hour])
    return hours

  def xset_force_on(self):
    if xset:
      os.system('export DISPLAY=:0; /usr/bin/xset dpms force on')  

  def tvservice_on(self):
    if tvservice:
      os.system('export DISPLAY=:0; /usr/bin/tvservice -p')  

  def tvservice_off(self):
    if tvservice:
      os.system('export DISPLAY=:0; /usr/bin/tvservice -o')  

  def xset_force_off(self):
    if xset:
      os.system('export DISPLAY=:0; /usr/bin/xset dpms force off')  

  def read_img(self):
    self.img=cv2.imread(self.FileName)
    print self.FileName
    self.write_log(self.FileName+" "+str(self.img.shape))  
    if self.grayscale=="true": 
      self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    self.xset_force_on()

  def show(self):
    cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE )
    r = int(long(self.yscreenresulation*1000 / self.img.shape[0]*1000)) # *1000 cause we need better precision
    dim = (int(self.img.shape[1]*r)/1000000,self.yscreenresulation)
    self.img=cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
    cv2.moveWindow("Frame", int((self.xscreenresulation-self.img.shape[1])/2), 0) 
    cv2.imshow("Frame",self.img)
    self.update_image_name()
    for f in range (0,int(self.delay/12)+1):
      self.xset_force_on()
      key=cv2.waitKey(5000)
      self.check_import_config()

  def update_rest(self,lurl,data):
    etag=requests.get(url+lurl).json()["_etag"]
    headers = {'If-Match': etag,'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.patch(url+lurl, data=json.dumps(data), headers=headers)

  def update_image_name(self):
    imagename = '{"image_name": "'+str(self.FileName)+'"}'
    self.update_rest("/state/1", imagename )

  def add_hour(self):
    hours_show=self.get_hours_show()
    if hours_show=="1":
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

  def add_text(self,x=50,y=170,size=4.2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(self.img, self.msg, (x,y), font, size,(0,0,0),18)
    cv2.putText(self.img, self.msg, (x,y), font, size,(255,255,255),7)

  def check_on_off(self):
    hours_on=self.get_hours_on()
    print "Hours_on "+hours_on
    if hours_on=="1":
      self.xset_force_on()
#      self.tvservice_on()
      return 1
    else:
      self.write_log("putting screen off") 
      self.xset_force_off()
#      self.tvservice_off()
      time.sleep(20)

  def write_log(self,Text):
    print(time.strftime("%H:%M:%S ")+Text+"\n")
    f=open(LogFile,'a')
    f.write(time.strftime("%H:%M:%S ")+Text+"\n")
    f.close()

  def main1(self):
    self.msg=""
    self.Hour=str(time.strftime("%H"))
    self.Day=int(datetime.datetime.today().weekday()+2)
    if self.Day > 7:
      self.Day=Self.Day-7
    self.Day=str(self.Day)
    if self.check_net != 0:
      self.check_net()
    if self.check_on_off():
      self.read_img()
      self.add_hour()
      self.show()

  def main(self):
    count=0
    if int(self.series) > len(self.List):
      self.series=len(self.List)-1
    f=randint(0,int(len(self.List))-int(self.series))
    while 1:
      self.FileName=self.List[f]
      self.main1()
      count+=1
      f+=1
      if count>=self.series:
        count=0
        f=randint(0,len(self.List)-self.series)

os.environ['DISPLAY']=':0'        
Frame01 = frame()


