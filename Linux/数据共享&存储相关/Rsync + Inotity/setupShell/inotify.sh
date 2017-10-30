#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    printf "Error: You must be root to run this script!\n"
    exit 1
fi

if [ -s inotify-tools-3.13 ]; then
    rm -rf inotify-tools-3.13
fi

printf "\nInotify Install ...\n\n"
tar zxvf inotify-tools-3.13.tar.gz
cd inotify-tools-3.13
./configure --prefix=/usr/local
make
make install
cd -

if [ ! -f /usr/local/lib/libinotifytools.so ]; then
    printf "Error: inotify-tools compile install failed!\n"
    exit 1
fi

printf "\n===== Inotify tools install Completed! ====\n\n"

