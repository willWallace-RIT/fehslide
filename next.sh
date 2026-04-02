#!/usr/bin/env/ bash
newfile=`find $1 -type f | shuf -n 1`
oldpath=`cat ~/.fehbg | sed -n 2p | cut -d "'" -f2`

oldfile="${oldpath}"
echo $oldfile
python -u ~/fehTransition2.py "$oldfile" "$newfile" 5 .001 200 5

