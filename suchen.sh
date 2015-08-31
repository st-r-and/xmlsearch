#!/bin/bash
for str in $( sed ':a;N;$!ba;s/\n/ /g;s/\r//g' /media/steve/Backup/reichel-steve/820/IDs.txt )
do 
str="$str.XML"
echo $str suchen
for list in $( ls /media/steve/Backup/reichel-steve/820/ftp/* )
do
#echo $list
if [[ $( unzip -l $list | grep --color -E $str | sed 's/ \+/ /g' | cut -d ' ' -f5 ) == $str ]]
then
 unzip -qo $list $str -d /media/steve/Backup/reichel-steve/820/result1
 echo $str gefunden in $list
 break
fi
done
done
