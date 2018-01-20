#!/bin/bash
for f in $( seq 1 10); do
  echo "== "$f" =="
  curl http://frame/api/days/$f
  echo " "
done
