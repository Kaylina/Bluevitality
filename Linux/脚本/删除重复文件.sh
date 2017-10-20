#!/bin/bash
# 用途查找并删除重复文件

ls -lS --time-style=long-iso | awk 'BEGIN {
  getline;getline;
  name1=$8;size=$5
  }
  {
    name2=$8;
    if(size==$5){
      "md5sum "name1 | getline;csum1=$1;
      "md5sum "name2 | getline;csum2=$2;
      if(csum=1==csum2){
        print name1;printname2
      }
    };
    size=$5;name1=name2;
  }
' | sort -u > duplicate_files

cat duplicate_files | xargs -I {} md5sum {} | sort | uniq -w 32 | awk '{print "^"$2"$"}' | sort -u > dumplicate_simple
echo Removing...
comm duplicate_files duplicate_simple -2 -3 | tee /dev/stderr | xargs rm 
echo Removed duplicates files successfully
