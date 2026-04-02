#!/usr/bin/bash

#$PIDS=$(pidof sh)
echo "Pids:"
echo $PIDS
for pid in $(pidof sh)
do
  echo "pid: $pid"
  CO1=`ps -f --no-heading -o cmd -p $pid`
  echo $CO1
  COM='sh ' 
  EXPATH='/home/northbot/fehtransitionslideshow.sh '
  DIRPATH='/home/northbot/Docs/Pics ' 
  NUM='100'
  
  CO2="$COM$EXPATH$DIRPATH$NUM"
  echo $CO2
  #echo "program: $C01"
  if [ "$CO1" = "$CO2" ]
  then
    kill $pid
  fi
done

