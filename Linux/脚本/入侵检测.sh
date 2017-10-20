#!/bin/bash
#用途 入侵报告工具，以auth.log作为日志文件

AUTHLOG=/var/log/auth.log

if [[ -n $1 ]];
then
  AUTHLOG=$1
  echo Using Log File : $AUTHLOG
fi

LOG=/tmp/valid.$$.log
grep -v "invalid" $AUTHLOG > $LOG
users=$(grep "Failed password" $LOG | awk '{print $(NF-5)}' | sort | uniq)
printf "%-5s|%-10s|%-10s|%-13s|%-33s|%s\n" "Sr#" "User" "Attempts" "IP address" "Host_Mapping" "Time range"
ucount=0
ip_list="$(grep -eo "[0-9]+\.[0-9]+\.[0-9]+" $LOG | sort | uniq)"
for ip in $ip_list;
do
  grep $ip $LOG > /tmp/temp.$$.log
  for user in $users;
  do 
    grep $user /tmp/temp.$$.log > /tmp/$$.log
    cut -c-16 /tmp/$$.log > $$.time
    tstart=$(head -1 $$.time);
    start=$(date -d "$tstart" "+%s");
    tend=$(tail -1 $$.time);
    end=$(date -d "$tend" "+%s")
    
    limit=$(($end-$start))
    if [$limit -gt 120];
    then
      ucount=$(($ucount+1))
      IP=$(grep -Eo "([0-9]+\.){3}[0-9]+" /tmp/$$.log | head -1);
      TIME_RANGE="$tstart-->$tend"
      ATTEMPTS=$(cat /tmp/$$.log | wc -l);
      HOST=$(host $IP | awk '{print $NF}')
      printf "%-5s|%-10s|%-10s|%-13s|%-33s|%s\n" "$ucount" "$user" "$ATTEMPTS" "$IP" "$HOST" "$TIME_RANGE"
     fi
    done
  done
rm -f /tmp/valid.$$.log /tmp/$$.log $$.time /tmp/temp.$$.log 
