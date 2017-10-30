#!/bin/bash

if [ ! -f /etc/1.pas ];
  then echo "123456" > /etc/1.pas
  chmod 600 /etc/1.pas
fi

host1=192.168.225.131
host2=192.168.225.132

src=/home/
des=/home/
user=root
log=/usr/local/inotify/logs/rsync.log

inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w%f' -e modify,delete,create,attrib ${src} | while read file 
do
    rsync -vzrtopg --delete -e ssh ${src} ${user}@${host1}:${des} && echo "${TIME} on ${DATE}, file $FILECHANGE backed ok" >> $log
    rsync -vzrtopg --delete -e ssh ${src} ${user}@${host2}:${des} && echo "${TIME} on ${DATE}, file $FILECHANGE backed ok" >> $log
done
