#!/bin/bash
morph=0
pngs=()
while [ $morph -le 100 ]
do
 # echo "converting"
  #convert $1 -fill black -colorize $(( 100 - $morph ))% png:- | convert $2 -fill black -colorize $morph% png:- | feh --bg-scale -
  #convert "$1" -resize 1920x1080 -fill black -colorize $morph% \( "$2" -resize 1920x1080 -alpha Opaque -channel A -evaluate Multiply `bc -l <<< $morph/100.0` +channel -set page +$((100-$morph)) \) -layers merge -crop 1920x1080 png:-|feh --bg-scale -

  png=$(convert "$1" \( "$2" -alpha Opaque -channel A -evaluate Multiply $(bc -l <<< $morph/100.0) +channel -set page +$((100-$morph)) \) -layers merge -crop 1920x1080 -|base64)
  pngs+=( "$png" )
  morph=$(($morph + $3))
  #echo "sleeping"
  #sleep $4
done
echo "loaded"
for t in {0..${!pngs[@]}..1}
do
  
  base64 --decode <<< pngs[$t] |convert - png:- | feh --bg-scale -
  sleep $4
done
feh --bg-scale "$2"
#convert mpr:bgImages -delete 0--1

