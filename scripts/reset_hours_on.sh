#!/bin/bash
# script to set all days to default 
for f in $( seq 1 5); do
  /opt/frame/scripts/update.sh  'clock_on/'$f '{"hours":"000000010000000000001100"}'
done
  /opt/frame/scripts/update.sh  'clock_on/6' '{"hours":"000000010000100000000000"}'
  /opt/frame/scripts/update.sh  'clock_on/7' '{"hours":"000000000000000000001100"}'
