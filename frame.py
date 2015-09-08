import cv2,os,time,datetime,pickle,subprocess
from random import randint
from config import *

class frame:
	def __init__(self):
		os.system('export DISPLAY=:0; /usr/bin/xset dpms force on') #Making sure screen stays on
		self.List=[]
		self.Shown=[]
		for path, subdirs, files in os.walk(root):
    			for name in files:
				if types.count(name[-3:])>0:
        				self.List.append( os.path.join(path, name) )
		self.write_log("------------")
		self.write_log("* Starting *")
		self.List.sort()
		self.main()

	def export_list(self):	#Exporting the image list for the web server
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


	def read_img(self):
		self.img=cv2.imread(self.FileName)
		self.write_log(self.FileName+" "+str(self.img.shape))	
		if GrayScale: 
			self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		os.system('export DISPLAY=:0; /usr/bin/xset dpms force on') #Making sure screen stays off

	def show(self):
		cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE )
		r = int(long(YScreenResulation*1000 / self.img.shape[0]*1000)) # *1000 cause we need better precision
		dim = (int(self.img.shape[1]*r)/1000000,YScreenResulation)
		self.img=cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
		cv2.moveWindow("Frame", int((XScreenResulation-self.img.shape[1])/2), 0) 
		cv2.imshow("Frame",self.img)
		key=cv2.waitKey(1000*Delay)

	def add_hour(self):
		if hours_show[self.Day].count(self.Hour)>0:
			self.msg=time.strftime("%H:%M")
			self.add_text()
			return

		if Show_Half and (time.strftime("%M")=='30' or time.strftime("%M")=='00'):
		 	self.msg=time.strftime("%H:%M")
                        self.add_text()

	
	def check_net(self):
		Status=subprocess.Popen("/bin/ping -c1 -w2 " +str (Net_target), shell=True, stdout=subprocess.PIPE).stdout.read()
		if Status.find ('100% packet loss') > 0:
			self.msg=":( "+self.msg
			self.add_text()
	

	def add_text(self,x=50,y=170,size=4.2):
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(self.img, self.msg, (x,y), font, size,(0,0,0),18)
		cv2.putText(self.img, self.msg, (x,y), font, size,(255,255,255),7)

	def check_on(self):
		if hours_on[self.Day].count(self.Hour)>0:
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
		if Check_net != 0:
			self.check_net()
		self.export_list()
		self.show()
	

	def main(self):
		count=0
		f=randint(0,len(self.List)-series)
		while 1:
			self.FileName=self.List[f]
			self.main1()
			count+=1
			f+=1
			if count>=series:
				count=0
				f=randint(0,len(self.List)-series)
				

Frame01 = frame()
