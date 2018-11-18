iptables -N REDIS
iptables -A REDIS -s 192.168.0.101 -j ACCEPT
iptables -A REDIS -s 192.168.0.103 -j ACCEPT
iptables -A REDIS -j LOG --log-prefix "unauth-redis-access"
iptables -A REDIS -j REJECT --reject-with icmp-port-unreachable
iptables -I INPUT -p tcp --dport 6379 -j REDIS