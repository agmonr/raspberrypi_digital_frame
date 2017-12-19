root="/home/user/background/"			#Images Root folder
Delay=6 				#Daley in sec between images
YScreenResulation=1080
XScreenResulation=1920
types=['jpg','jpeg','JPG','JPEG'] 	#Supported image types
series=20				#Length of image serias
GrayScale=0                     	#Show in greyScale
Show_Half=1                     	#Show hour every 30 minutes
Check_net=1				#check internet connection
Net_target='8.8.8.8'			# address to ping 

hours_show=[0,1,2,3,4,5,6,7] 		# Array init 
hours_on=[0,1,2,3,4,5,6,7] 		# Array init


#When the script will add the hour to the image
hours_show[0]=['07','20'] #Monday
hours_show[1]=['07','20']
hours_show[2]=['07','20']
hours_show[3]=['07','20']
hours_show[4]=['07']
hours_show[5]=[]
hours_show[6]=['07','20'] #Sunday


# When the script will set the screen on
hours_on[0]=['06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] #Friday
hours_on[1]=hours_on[0]
hours_on[2]=hours_on[0]
hours_on[3]=hours_on[0]
hours_on[4]=hours_on[0]
hours_on[5]=hours_on[0]
hours_on[6]=['06','07','08','16','17','18','19','20','21','22','23'] #Sunday
