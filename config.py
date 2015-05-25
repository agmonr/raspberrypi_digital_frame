root="/home/Photos/"			#Images Root folder
Delay=10 				#Daley in sec between images
XScreenResulation=1920			#Screen Resoution
YScreenResulation=1080		
types=['jpg','jpeg','JPG','JPEG'] 	#Supported image types
serias=20				#length of image serias
GrayScale=1                     	#Show in greyScale


hours_show=[0,1,2,3,4,5,6,7] 		# Array init 
hours_on=[0,1,2,3,4,5,6,7] 		# Array init


#When the script will add the hour to the image
hours_show[0]=['7','20'] #monday
hours_show[1]=['7','20'] 
hours_show[2]=['7','20']
hours_show[3]=['7','20']
hours_show[4]=['7','20']
hours_show[5]=['7','20']
hours_show[6]=['7','20'] #Sunday

# When the script will set the screen on
hours_on[0]=['06','07','08','16','17','18','19','20','21','22','23'] #Monday
hours_on[1]=['06','07','08','16','17','18','19','20','21','22','23']
hours_on[2]=['06','07','08','16','17','18','19','20','21','22','23']
hours_on[3]=['06','07','08','16','17','18','19','20','21','22','23']
hours_on[4]=['06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] #Friday
hours_on[5]=['06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
hours_on[6]=['06','07','08','16','17','18','19','20','21','22','23'] #Sunday
