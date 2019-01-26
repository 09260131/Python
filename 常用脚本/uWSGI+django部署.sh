pip install uwsgi
ln -s /usr/local/python2.7/bin/uwsgi /usr/local/bin/uwsgi

#先在项目目录下建立一个测试文件：
vim foobar.py
def application(env,start_response):
    start_response('200 ok',[('Content-Type','text/html')])
    return [b"Hello World"]

uwsgi --http :9000 --wsgi-file foobar.py
#通过浏览器访问http://ip:9000能看到hello world说明成功
#然后停止服务



#############################
pip3 install django
ln -s /usr/local/python356/bin/django-admin /usr/local/bin/django-admin


############################# 安装 nginx
# 准备工作
yum -y install gcc automake autoconf libtool make
yum install gcc gcc-c++

cd /usr/local/src
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.39.tar.gz
tar -zxvf pcre-8.39.tar.gz
cd pcre-8.34
./configure
make
make install

cd /usr/local/src
wget http://zlib.net/zlib-1.2.11.tar.gz
tar -zxvf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make
make install

cd /usr/local/src
wget https://www.openssl.org/source/openssl-1.0.1t.tar.gz
tar -zxvf openssl-1.0.1t.tar.gz

cd /usr/local/src
wget http://nginx.org/download/nginx-1.1.10.tar.gz
tar -zxvf nginx-1.1.10.tar.gz
cd nginx-1.1.10
./configure
make
make install