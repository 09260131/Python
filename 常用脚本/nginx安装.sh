yum install -y wget
yum install -y vim-enhanced
yum install -y make cmake gcc gcc-c++

# 下载nginx安装包
echo "下载nginx安装包"
wget http://nginx.org/download/nginx-1.6.2.tar.gz

# 安装依赖包
echo "安装依赖包"
yum install -y pcre pcre-devel
yum install -y zlib zlib-devel
yum install -y openssl openssl-devel
tar -zxvf nginx-1.6.2.tar.gz -C /usr/local/

# 进入nginx-1.6.2目录然后在执行./configure命令,进行configure配置
echo "进行configure配置"
cd /usr/local/nginx-1.6.2
./configure --prefix=/usr/local/nginx

# 编译安装
echo "编译安装"
make && make install

# 启动Nginx
echo "启动Nginx"
/usr/local/nginx/sbin/nginx

# 配置防火墙
echo "配置防火墙"
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload