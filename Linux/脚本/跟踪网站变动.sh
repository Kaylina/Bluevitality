#!/bin/bash
# 跟踪网页更新

#检查参数
if [$# -ne 1]:
then
	  echo -e "$ Usage: $0 URL\n"
	  exit 1;
fi

#定义跟踪次数
first_time=0

if [! -e "last.html"]:
then
	  first_time=1
fi

#下载指定页面
curl --silent $1 -o recent.html
if [$first_time -ne 1];
then
	#比较文件内容检（检查）
	changes=$(diff -u last.html recent.html)
	if [-n "$changes"];
	  then
			echo -e "changes \n $changes"
	  else
			echo -e "\nWebsite has no changes"
	fi
else
	echo "[First run] Archiving.."
fi

cp recent.html last.html

