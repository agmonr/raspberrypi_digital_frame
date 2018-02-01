#!/bin/bash
# script to set all days to default 
for f in $( seq 1 7); do
  /opt/frame/scripts/update.sh  'days/'$f '{"hours":"11111111111111111111111"}'
done
