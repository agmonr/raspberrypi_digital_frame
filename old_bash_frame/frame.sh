#!/bin/bash
FullList=/tmp/list
ShowList=/tmp/show
#Photos_Home=/home/Photos/2015/
Photos_Home=/home/Photos/
Home=/home/frame/
Sleep=30

#Line=$( expr $( date +%H%M%S ) % $( find $Photos_Home -maxdepth 1 -type d | wc -l ) + 1 ) # Change folder every day
#Photos=$( find $Photos_Home -maxdepth 1 -type d | tail -n $Line | head -n 1 )
Photos=$( find $Photos_Home -maxdepth 1 -type d ) 
echo $Line
cd $Home
rm $FullList $ShowList

pkill X 
export DISPLAY=:0
sleep 1

x='xinit /etc/X11/xinit/xinitrc :0 '
x='X :0'

$x &
LPID=0
while true; do


	y=$( /usr/bin/tvservice -s | fgrep -c 'progressive') # Test if screen is off
	echo $y
	if [ "$y" == 1 ]; then 
		find -L ${Photos_Home} -type f | grep -i ".j" | sort | uniq > $FullList
		N=$( cat $FullList | wc -l )
		N=$(( N - 20 ))
		for f in $( seq 1 20); do
		       Line=$( echo $RANDOM % $N | bc )
		       tail -n $Line /tmp/list | head -n 200 >> $ShowList
		done



#		S=$( cat $ShowList | wc -l )
#		echo $Start $( date ) >> /home/fbi.log
#		cat /tmp/list | tail -n $Start | head -n 500  > $ShowList
		while read jpg; do


			# Creating html list
			head -n 150 /var/www/index.html > /tmp/index.tmp
			link=$( echo $jpg | sed -e 's|home/||' )
			url="<p> <a href=\".$link\">$( date ) -- $jpg </a> </p>" 
			echo $url > /var/www/index.html
			cat /tmp/index.tmp >> /var/www/index.html

#			cat /home/frame/1.html | sed -e 's|XXX|'http://frame$link'|' > /var/www/1.html 
			cat /home/frame/1.html | sed -e 's|XXX|'$link'|' > /var/www/1.html 

			# creating sym link for the current image display	
			rm /var/www/current.jpg

			ln -s $jpg /var/www/current.jpg

#			echo "$( date ) - $jpg " >> /home/frame/frame.log
	
			# Convert the image to a tmp and adding the a message from file (goes with crontab and so)
		
#if (( ( "$Min" == "30" ) || ( "$Min" == "0" ) )); 
			if Text=$( cat $Home/text.msg );
			then
				nice -n 20 convert -size 2400x1600 -pointsize 180 -font /usr/share/fonts/truetype/culmus/DavidCLM-Bold.ttf -fill grey -stroke black -strokewidth 6 -draw "text 0,180 \"$Text" "$jpg" /tmp/message.jpg
			jpg="/tmp/message.jpg"
			fi

		

#			curl "http://k1789.org/gps/map.png" > /tmp/map.png
#			Mapok=$( file /tmp/map.png | grep 'PNG' )
# 			if [ "$Mapok" != "" ]; then
#	          		jpg=/tmp/map.png
#				Sleep=30
#			fi



			Show="feh -Y -F -Z"
			$Show "$jpg" &
			PID=$!
		
			xset s reset
			sleep 3
			if [ "$LPID" != "0" ]; then
				kill -9 $LPID 
			fi		
			sleep $Sleep
			Sleep=60
			LPID=$PID



		echo $PID $jpg
		done < $ShowList
		
		killall -9 feh
		killall -9 X
		rm %Home/text.msg
		$x &
 
	else
		killall -9 feh
		echo "Sleeping"
		sleep 60
	fi

done

exit 0

