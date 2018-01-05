import cv2,os,time,datetime,pickle,subprocess,json,urllib2,requests,httplib2
from random import randint

types=['jpg','jpeg','JPG','JPEG']
url="http://localhost:5000"
tvservice=os.path.exists("/usr/bin/tvservice")
xset=os.path.exists("/usr/bin/xset")


class frame:
  def __init__(self):
    self.import_config()
    self.import_config_state()
    self.List=[]
    self.Shown=[]
    for path, subdirs, files in os.walk(self.root):
      for name in files:
        self.List.append(unicode(path)+"/"+unicode(name))

    print "Number of items "+str(len(self.List))
    self.write_log("------------")
    self.write_log("* Starting *")
    self.List.sort()
    self.main()

  def import_config_state(self):
    self.yscreenresulation=requests.get(url+"/config/3").json()["yscreenresulation"]
    self.xscreenresulation=requests.get(url+"/config/4").json()["xscreenresulation"]

  def import_config(self):
    self.root=requests.get(url+"/config/1").json()["root"]
    self.series=requests.get(url+"/config/5").json()["series"]
    self.grayscale=requests.get(url+"/config/6").json()["grayscale"]
    self.show_half=requests.get(url+"/config/7").json()["show_half"]
    self.check_net=requests.get(url+"/config/8").json()["check_net"]
    self.delay=int(requests.get(url+"/config/2").json()["delay"])
    
  def get_hours_on(self):
    now=datetime.datetime.now() 
    hours=(requests.get(url+"/days/"+str(int(datetime.datetime.today().weekday()))).json()["hours"][now.hour])
    return hours 
  
  def get_hours_show(self):
    now=datetime.datetime.now() 
    hours=(requests.get(url+"/h_display/"+str(int(datetime.datetime.today().weekday()))).json()["hours"][now.hour])
    return hours

  def export_list(self):  #Exporting the image list for the web server
    return 
    self.Shown.append([time.strftime("%H:%M"),self.FileName])
    if len(self.Shown) > 100:
      self.Shown=self.Shown[-100:]
    f=open('shown.pck','w')
    pickle.dump(self.Shown,f)
    f.close()

  def write_log(self,Text):
    f=open('frame.log','a')
    f.write(time.strftime("%H:%M ")+Text+"\n")
    f.close()

  def xset_force_on(self):
    if not xset:
	return
    os.system('export DISPLAY=:0; /usr/bin/xset dpms force on') #Making sure screen stays off

  def read_img(self):
    self.img=cv2.imread(self.FileName)
    print self.FileName
    self.write_log(self.FileName+" "+str(self.img.shape))  
    if self.grayscale: 
      self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    self.xset_force_on()

  def show(self):
    cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE )
    r = int(long(self.yscreenresulation*1000 / self.img.shape[0]*1000)) # *1000 cause we need better precision
    dim = (int(self.img.shape[1]*r)/1000000,self.yscreenresulation)
    self.img=cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
    cv2.moveWindow("Frame", int((self.xscreenresulation-self.img.shape[1])/2), 0) 
    cv2.imshow("Frame",self.img)
    for f in range (0,int(self.delay/10)+1):
      self.xset_force_on()
      key=cv2.waitKey(10000)
      self.import_config()
    self.update_image_name()

  def update_rest(self,lurl,data):
    etag=requests.get(url+lurl).json()["_etag"]
    headers = {'If-Match': etag,'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.patch(url+lurl, data=data, headers=headers)

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

  def check_on(self): 
    if not tvservice:
	return
    hours_on=self.get_hours_on()
    if hours_on=="1":
      Status=subprocess.Popen("/usr/bin/tvservice -s", shell=True, stdout=subprocess.PIPE).stdout.read()
      if Status.find('progressive') == -1:
        self.write_log("Screen off - turning on")
        os.system('/usr/bin/tvservice -p')
    else:
      os.system('/usr/bin/tvservice -o')
      self.write_log("Turning screen off")
      while( time.strftime("%H") == self.Hour):
        time.sleep(600)


  def main1(self):
    self.msg=""
    self.Hour=time.strftime("%H")
    self.Day=datetime.datetime.today().weekday()
    self.check_on()
    self.read_img()
    self.add_hour()
    if self.check_net != 0:
      self.check_net()
    self.export_list()
    self.show()
  

  def main(self):
    count=0
    if self.series > len(self.List):
	    self.series=len(self.List)-1 
    f=randint(0,len(self.List)-self.series)
    while 1:
      self.FileName=self.List[f]
      self.main1()
      count+=1
      f+=1
      if count>=self.series:
        count=0
        f=randint(0,len(self.List)-self.series)
        

Frame01 = frame()
