#!/bin/bash
etag=$( curl -s http://localhost:5000/$1 | python -m json.tool | grep "_etag" | awk -F\" '{ print $4 }' )

curl -H "If-Match: $etag" -H "Content-Type: application/json" -X PATCH -i "http://localhost:5000/$1" -d "$2"

