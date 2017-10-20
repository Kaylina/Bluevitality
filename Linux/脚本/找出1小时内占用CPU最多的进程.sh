#!/bin/bash
# 用途 计算1小时内进程占用CPU 情况

SECS=3600
UNIT_TIME=60

STEP=$(($SECS/$UNIT_TIME))
echo Watching CPU usage...;

for((i=0;i<STEPS;i++))
do
 ps -eo comm,pcpu | tail -n +2 >> /tmp/cpu_usage.$$
 sleep $UNIT_TIME
done

echo 
echo CPU eaters:

cat /tmp/cpu_usage.$$ | \
awk '{process[$1]+=$2}END{for(i in process)print i,process[i]}' | sort -nrk 2 | head
rm -f /tmp/cpu_usage.$$
