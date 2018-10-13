#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: change_hostname.py
# Create Date: 2017-05-10 12:51
# Modify Date: 2017-05-10 12:51
#***************************************************************#
import sys, commands, json

def changeHostname(hostname, ip):

    # 修改主机名
    cmd = 'ssh -o ConnectTimeout=30 %s "if cat /etc/redhat-release | grep \'release 7\';then hostnamectl set-hostname %s;else hostname %s;fi"' % (ip, hostname, hostname)
    status, data = commands.getstatusoutput(cmd)
    if status != 0:
        return False, "change hostname failed:" + data

    # 修改网卡
    cmdb = 'ssh -o ConnectTimeout=30 %s "cat /etc/sysconfig/network | grep "HOSTNAME=" || sed -i \'1 aHOSTNAME=xxx\'  /etc/sysconfig/network"' % ip
    commands.getstatusoutput(cmdb)
    cmdb = 'ssh -o ConnectTimeout=30 %s "sed -i \'s/HOSTNAME=.*/HOSTNAME=%s/\' /etc/sysconfig/network"'  % (ip, hostname)
    status, data = commands.getstatusoutput(cmdb)
    if status != 0:
        return False, "change network failed:" + data

    # 修改hosts
    # cmdb = 'ssh -o ConnectTimeout=30 %s "sed -i \'s/127.0.0.1.*localhost.localdomain localhost4 localhost4.localdomain4/127.0.0.1 %s localhost.localdomain localhost4 localhost4.localdomain4/\' /etc/hosts"'  % (ip, hostname)
    cmd = 'ssh -o ConnectTimeout=30 %s "echo -e \\\"127.0.0.1 localhost\\n127.0.0.1 %s\\n%s %s\\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6\\\" > /etc/hosts "' \
          % (ip, hostname, ip, hostname)
    status, data = commands.getstatusoutput(cmd)
    # cmdb = 'ssh -o ConnectTimeout=30 %s "sed -i \'s/\\(.*\\)%s.*/%s %s/\' /etc/hosts"'  % (ip, ip, ip, hostname)
    # status, data = commands.getstatusoutput(cmdb)
    if status != 0:
        return False, "change hosts failed:" + data

    # 重启zabbix agent
    command_zabbix = 'ssh -o ConnectTimeout=30 %s "/etc/init.d/zabbix-agent restart"' % ip
    commands.getstatusoutput(command_zabbix)

    # 重启rsyslog
    commands_rsyslog = 'ssh -o ConnectTimeout=30 %s "if cat /etc/redhat-release | grep \'release 7\';then systemctl restart  rsyslog;else service rsyslog restart;fi"' % ip
    commands.getstatusoutput(commands_rsyslog)
    return True, 'succ!'



if __name__ == '__main__':
    if len(sys.argv) == 3:
        state, msg = changeHostname(sys.argv[1], sys.argv[2])
        result = {"success": state, 'msg': msg}
    else:
        result={"success": False, "msg": 'params error!'}
    print json.dumps(result)
