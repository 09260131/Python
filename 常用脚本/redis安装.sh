wget http://download.redis.io/releases/redis-2.8.3.tar.gz
tar xzf redis-2.8.3.tar.gz
cd redis-2.8.3
make
cd src
make install
mkdir /usr/redis
cp redis-server /usr/redis
cp redis-benchmark /usr/redis
cp redis-cli /usr/redis
cp ../redis.conf /usr/redis

cd /usr/local
rm -rf redis-2.8.3.tar.gz redis.sh