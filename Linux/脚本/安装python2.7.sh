wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz

tar xvf Python-2.7.9.tgz
cd Python-2.7.9
./configure --prefix=/usr/local/python27
make
make install
mv /usr/bin/python /usr/bin/python_old
ln -s /usr/local/python27/bin/python /usr/bin/python
