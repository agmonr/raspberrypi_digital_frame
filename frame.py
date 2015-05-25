import cv2,os,time,datetime
from random import randint
from time import gmtime, strftime
import subprocess

from config import *

class frame:
	def __init__(self):
		os.system('export DISPLAY=:0; /usr/bin/xset dpms force off') #making sure power save stays off
		self.List=[]
		for path, subdirs, files in os.walk(root):
    			for name in files:
				if types.count(name[-3:])>0:
        				self.List.append( os.path.join(path, name) )
		self.write_log("------------")
		self.write_log("* Starting *")
		self.main()

	def write_log(self,Text):
		f=open('frame.log','a')
		f.write(time.strftime("%H:%M ")+Text+"\n")
		f.close()


	def read_img(self):
		self.img=cv2.imread(self.FileName)
		self.write_log(self.FileName+" "+str(self.img.shape))	
		if GrayScale: 
			self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		os.system('export DISPLAY=:0; /usr/bin/xset dpms force off') #making sure power save stays off

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
		self.Hour=time.strftime("%H")
		self.Day=datetime.datetime.today().weekday()
		self.check_on()
		self.read_img()
		self.add_hour()
		self.show()
	

	def main(self):
		count=0
		f=randint(0,len(self.List)-serias)
		while 1:
			self.FileName=self.List[f]
			try:
				self.main1()
			except:
				print "Problem with img"+self.FileName
				self.write_log( "Problem with img "+self.FileName )

			count+=1
			f+=1
			if count>=serias:
				count=0
				f=randint(0,len(self.List)-serias)
				

Frame01 = frame()
