#!/bin/bash
for f in $( seq 0 7); do
  curl http://frame/api/days/$f
done
