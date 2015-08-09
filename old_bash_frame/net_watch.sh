#!/bin/bash
Log=/var/log/messages

for i in $( seq 1 5); do
	ping -c1 192.168.2.152
	y="$?"
	curl -s "http://192.168.2.7/NetWatch" 
	[ "$y" == 0 ] && exit

	echo "Failed network $( date )" >> $Log
	/etc/init.d/networking stop
	/sbin/ifconfig wlan2 down
sleep 10
	/etc/init.d/networking start
	/sbin/ifconfig wlan2 up
	pkill dhclient 
	dhclient wlan2
echo "Down $( date )" >> $Log

curl -s "http://192.168.2.7/88888888888888888888888NetRestarted" 
sleep 30
done

Up=$( uptime | grep min | awk '{ print $3 }' )
if [ "$Up" == "" ]; then
	echo "$( date ) - Reboooooting....." >> $Log
	/sbin/halt
        /sbin/init 0
fi


if [ "$Up" -gt "5" ]; then
	echo "$( date ) - rebooooooooooooooting...." >> $Log
	/sbin/reboot	
        /sbin/init 6
fi

