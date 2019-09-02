#!/bin/bash
# the script reset the hours that the frame will show the hour (clock on)
# sunday-thursday - on 0700, 2000 ,2100
# friday,  - on 0700, 1300
# staudrday - on 2000, 2100



for f in $( seq 1 5); do
  /opt/frame/scripts/update.sh  'clock_on/'$f '{"hours":"000000010000000000001100"}'
done
  /opt/frame/scripts/update.sh  'clock_on/6' '{"hours":"000000010000100000000000"}'
  /opt/frame/scripts/update.sh  'clock_on/7' '{"hours":"000000000000000000001100"}'
