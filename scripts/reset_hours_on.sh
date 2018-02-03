#!/bin/bash
# script to set all days to default 
for f in $( seq 1 5); do
  /opt/frame/scripts/update.sh  'h_display/'$f '{"hours":"000000010000000000001100"}'
done
  /opt/frame/scripts/update.sh  'h_display/6' '{"hours":"000000010000100000000000"}'
  /opt/frame/scripts/update.sh  'h_display/7' '{"hours":"000000000000000000001100"}'
