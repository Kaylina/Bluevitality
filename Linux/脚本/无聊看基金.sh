#!/bin/bash

c003625=$(curl -s http://fund.eastmoney.com/003625.html | grep -oP '(?<=gz_gszzl">)........'| grep -oP ".*(?=<)") #创金合信资源股票发起C
p002259=$(curl -s http://fund.eastmoney.com/002259.html | grep -oP '(?<=gz_gszzl">)........'| grep -oP ".*(?=<)") #
j260103=$(curl -s http://fund.eastmoney.com/260103.html | grep -oP '(?<=gz_gszzl">)........'| grep -oP ".*(?=<)") #
j260112=$(curl -s http://fund.eastmoney.com/260112.html | grep -oP '(?<=gz_gszzl">)........'| grep -oP ".*(?=<)") #
j519772=$(curl -s http://fund.eastmoney.com/519772.html | grep -oP '(?<=gz_gszzl">)........'| grep -oP ".*(?=<)") #

> /usr/share/nginx/html/2/digit.html

echo "<html>" >>  /usr/share/nginx/html/2/digit.html
echo "<head>" >>  /usr/share/nginx/html/2/digit.html
echo "<title>?</title>" >>  /usr/share/nginx/html/2/digit.html
echo '<meta http-equiv="refresh" content="45">' >>  /usr/share/nginx/html/2/digit.html
echo "</head>" >>  /usr/share/nginx/html/2/digit.html
echo "<body>" >>  /usr/share/nginx/html/2/digit.html
echo "<pre>" >>  /usr/share/nginx/html/2/digit.html
printf "%-20s \t %-50s \n" "-创金合信资源股票发起C   " "$c003625"  >>  /usr/share/nginx/html/2/digit.html
printf "%-20s \t %-50s \n" "-鹏华健康环保混合        " "$p002259"  >>  /usr/share/nginx/html/2/digit.html
printf "%-20s \t %-50s \n" "-景顺长城动平衡          " "$j260103"  >>  /usr/share/nginx/html/2/digit.html
printf "%-20s \t %-50s \n" "-景顺长城能源基建混合    " "$j260112"  >>  /usr/share/nginx/html/2/digit.html
printf "%-20s \t %-50s \n" "-交银新生活力灵活配置混合" "$j519772"  >>  /usr/share/nginx/html/2/digit.html
echo "</pre>" >>  /usr/share/nginx/html/2/digit.html
echo "</body>" >>  /usr/share/nginx/html/2/digit.html
echo "</html>" >>  /usr/share/nginx/html/2/digit.html
