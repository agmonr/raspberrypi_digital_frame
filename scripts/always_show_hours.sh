#!/bin/bash
# script to set all days to default 
for f in $( seq 1 7); do
  /opt/frame/scripts/update.sh  'clock_on/'$f '{"hours":"111111111111111111111111"}'
done
