#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: zabbix_config.py
# Create Date: 2017-09-27 16:26
# Modify Date: 2017-09-27 16:26
#***************************************************************#
import sys, commands, json

def init_zabbix_config(ip, proxy_ip):
    fp = open("/tmp/%s.conf" % ip, mode="w")
    text = "PidFile=/var/run/zabbix/zabbix_agentd.pid\nLogFile=/var/log/zabbix/zabbix_agentd.log\nLogFileSize=0\nServer=%s\n" \
           "ServerActive=%s:10051\nHostname=%s\nInclude=/etc/zabbix/zabbix_agentd.d/" % (proxy_ip, proxy_ip, ip)
    fp.write(text)
    fp.close()
    cmd = "scp /tmp/%s.conf root@%s:/etc/zabbix/zabbix_agentd.conf" % (ip, ip)
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        return False, output
    # 重启zabbix agent
    command_zabbix = 'ssh -o ConnectTimeout=30 root@%s "/etc/init.d/zabbix-agent restart"' % ip
    commands.getstatusoutput(command_zabbix)
    return True, 'succ!'



if __name__ == '__main__':
    if len(sys.argv) == 3:
        state, msg = init_zabbix_config(sys.argv[1], sys.argv[2])
        if not state:
            print msg
            exit(500)
        print 'succ!'
    else:
        print 'params error!'
        exit(400)
