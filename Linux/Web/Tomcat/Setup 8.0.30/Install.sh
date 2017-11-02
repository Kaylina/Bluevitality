#!/bin/bash

jdk_rpm_file="jdk-8u77-linux-x64.rpm"
tomcat_tar_file="apache-tomcat-8.0.30.tar.gz"
tomcat_dir="apache-tomcat-8.0.30"
tomcat_install_dir="/usr/local/tomcat/"

yum -y install java-1.8.0-openjdk  java-1.8.0-openjdk-devel

if [ -f $tomcat_tar_file ];then
	tar -xf $tomcat_tar_file > /dev/null
	mv $tomcat_dir $tomcat_install_dir
	
	if [ -d $tomcat_install_dir ];then
		echo "tomcat install OK"
	fi
else 
	echo  "$tomcat_tar_file no such file. error"
fi

