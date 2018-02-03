#!/bin/bash
# script to set all days to default 
for f in $( seq 1 5); do
  /opt/frame/scripts/update.sh  'days/'$f '{"hours":"000000111000000011111111"}'
done
  /opt/frame/scripts/update.sh  'days/6' '{"hours":"000000111111111111111111"}'
  /opt/frame/scripts/update.sh  'days/7' '{"hours":"000000111111111111111111"}'
