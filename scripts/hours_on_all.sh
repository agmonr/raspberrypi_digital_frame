#!/bin/bash
# script to set all days to default 
for f in $( seq 1 7); do
  /opt/frame/scripts/update.sh  'h_display/'$f '{"hours":"111111111111111111111111"}'
done
