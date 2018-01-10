#!/bin/bash
# script to manualy update via the rest api
# useage:
#./update.sh 'days/1' '{"hours":"00000011100000001111111"}'

#[[ "$1" == "" ]] || [[ "$2" == "" ]] && curl -H "Content-Type: application/json" -X GET -i http://localhost:5000/ ; echo ""; exit 0

Current=$( curl -s http://localhost:5000/$1 | python -m json.tool ) >> /dev/null
echo -e "Current Value\n*************\n" $Current
etag=$( echo $Current | grep "_etag" | awk -F\" '{ print $8 }' )
curl -s -H "If-Match: $etag" -H "Content-Type: application/json" -X PATCH -i "http://localhost:5000/$1" -d "$2" >> /dev/null 

echo -e "Updated Value\n*************\n" $( curl -s http://localhost:5000/$1 | python -m json.tool )
