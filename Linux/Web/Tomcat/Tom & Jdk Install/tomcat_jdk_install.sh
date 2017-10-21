#!/bin/bash

jdk_rpm_file="jdk-8u77-linux-x64.rpm"
tomcat_tar_file="apache-tomcat-8.0.30.tar.gz"
tomcat_install_dir="/usr/local/tomcat/"
tomcat_dir="apache-tomcat-8.0.30"
NULL=/dev/null

print_info () {

	if [ -n "$1" ] && [ -n "$2" ] ;then
		case "$2" in
		OK)
    		echo -e "\e[32;1m$1 \t\t\t [OK]\e[0m"
     		;;
  		Fail)
       		echo -e "\e[31;1m$1 \t\t\t [Fail]\e[0m"
        	;;
     	other)
        	echo -e "\e[32;1m$1 \t\t\t \e[0m"
           	;;
		error)	
        	echo -e "\e[31;1m$1 \t\t\t \e[0m"
			;;
        *)
             echo "Usage info {OK|Fail}"
        esac
   fi
}

install_jdk (){
	if [ -f $jdk_rpm_file ];then
		rpm -vih $jdk_rpm_file > $NULL
		[ $? -eq 0 ] && print_info "$jdk_rpm_file install" "OK" || print_info "$jdk_rpm_file install" "Fail" 
	else
		print_info "$jdk_rpm_file no such file." "error"
	fi
}

install_tomcat (){
	if [ -f $tomcat_tar_file ];then
		tar -xf $tomcat_tar_file > $NULL
		#echo "tomcat_dir=$tomcat_dir"
		mv $tomcat_dir $tomcat_install_dir
		
		if [ -d $tomcat_install_dir ];then
			print_info "tomcat install" "OK"
		fi

	else 
		print_info "$tomcat_tar_file no such file." "error"
	fi
}

install_jdk
install_tomcat

