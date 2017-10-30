#!/bin/bash

ROOTPATH=`pwd`

export LANG=en
#wget  http://www.haproxy.org/download/1.6/src/haproxy-1.6.7.tar.gz;
tar zxvf  ./haproxy-1.6.7.tar.gz
cd $ROOTPATH/haproxy-1.6.7
make TARGET=linux2628 ARCH=x86_64
sudo make PREFIX=/usr/local/haproxy-1.6.7 install
sudo ln -s /usr/local/haproxy-1.6.7  /usr/local/haproxy;

cd /usr/local/haproxy;
sudo mkdir -p bin conf logs var/run  var/chroot


sudo useradd haproxy -s /sbin/nologin;
sudo chown -R haproxy:haproxy /usr/local/haproxy/var/run/;

sudo cp ./haproxy.cfg /usr/local/haproxy/conf;
