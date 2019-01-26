# python升级
wget http://python.org/ftp/python/2.7.4/Python-2.7.4.tgz
tar -xvf Python-2.7.4.tgz
cd Python-2.7.4
./configure --prefix=/usr/local/python2.7
make
make install

mv /usr/bin/python /usr/bin/python.old
ln -s /usr/local/python2.7/bin/python2.7 /usr/bin/python


# 安装 pip
wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py --insecure
wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
tar -xf pip-9.0.1.tar.gz
cd pip-9.0.1
python setup.py install
ln -s /usr/local/python2.7/bin/pip /usr/bin/pip