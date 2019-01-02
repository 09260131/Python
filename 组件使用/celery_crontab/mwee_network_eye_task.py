# -*- coding: utf-8 -*-
from datetime import datetime
import json
import time
from threading import Timer

import statsd
# from .celery import app

from aliyunsdkcms.request.v20180308 import QueryMetricListRequest
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkvpc.request.v20160428 import DescribeBandwidthPackagesRequest, \
    DescribeBandwidthPackagePublicIpMonitorDataRequest


########################## statsd 配置 ##########################
SERVER = '127.0.0.1'
PORT = 8125
PREFIX = 'mwee.network.eye'
DELAYTIME = 3

STATSD_CONNECTION = statsd.Connection(host=SERVER, port=PORT)
STATSD_CLIENT = statsd.Client("mwee.network.eye", STATSD_CONNECTION)
STATSD_GAUGE = STATSD_CLIENT.get_client(class_=statsd.Gauge)
########################## statsd 配置 ##########################


class AliyunBase():

    key = ''
    secret = ''
    regionId = ''

    def __init__(self, regionId='cn-shanghai'):
        self.regionId = regionId
        self.initClient(self.regionId, self.key, self.secret)

    def initClient(self, regionId, key, secret):
        self.clt = client.AcsClient(key, secret, regionId)
        return self.clt

class NATBandwidth(AliyunBase):
    '''
        拉取NAT网关的带宽数据
        (1) getDescribeBandwidthPackages                          查询指定地域的NAT带宽包公网IP的ID(AllocationId:公网IP的ID)
        (2) getDescribeBandwidthPackagePublicIpMonitorData        查询NAT带宽包中指定公网IP的监控数据
    '''
    def getDescribeBandwidthPackages(self, PageNumber=1, PageSize=50):
        try:
            request = DescribeBandwidthPackagesRequest.DescribeBandwidthPackagesRequest()
            request.set_PageNumber(PageNumber)
            request.set_PageSize(PageSize)
            response = self.clt.do_action_with_exception(request)
            result = json.loads(response)
            return True, result['BandwidthPackages']['BandwidthPackage']
        except Exception, ex:
            return False, str(ex)

    def getDescribeBandwidthPackagePublicIpMonitorData(self, AllocationId, StartTime, EndTime):
        try:
            request = DescribeBandwidthPackagePublicIpMonitorDataRequest.DescribeBandwidthPackagePublicIpMonitorDataRequest()
            request.set_AllocationId(AllocationId)
            request.set_StartTime(StartTime)
            request.set_EndTime(EndTime)
            reponse = self.clt.do_action_with_exception(request)
            result = json.loads(reponse)
            return True, result['MonitorDatas']['MonitorData']
        except Exception, ex:
            return False, str(ex)

class SLBBandwidth(AliyunBase):
    '''
        拉取负载均衡SLB的带宽数据
        (1) getDescribeLoadBalancers           SLB所有的外网实例
        (2) getQueryMetricList                 SLB的带宽监控数据
    '''

    def getDescribeLoadBalancers(self, addressType='internet'):
        try:
            request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
            request.set_AddressType(addressType)

            response = self.clt.do_action_with_exception(request)
            result = json.loads(response)
            return True, result['LoadBalancers']['LoadBalancer']
        except Exception, ex:
            return False, str(ex)

    def getQueryMetricList(self, startTime, endTime, metric, project='acs_slb_dashboard', period='60'):
        try:
            request = QueryMetricListRequest.QueryMetricListRequest()
            request.set_Project(project)
            request.set_Period(period)
            request.set_Metric(metric)
            request.set_StartTime(startTime)
            request.set_EndTime(endTime)

            response = self.clt.do_action_with_exception(request)
            result = json.loads(response)
            return True, result['Datapoints']
        except Exception, ex:
            return False, str(ex)


def pullNatBandwidthData():
    '''
        拉取NAT网关的带宽数据
    '''
    try:
        status, datas = NATBandwidth().getDescribeBandwidthPackages()
        allocationIds = []
        if status:
            for data in datas:
                for pia in data['PublicIpAddresses']['PublicIpAddresse']:
                    allocationIds.append(pia['AllocationId'])
        else:
            return False, u'查询指定地域的NAT带宽包公网IP的ID失败 : %s' % str(datas)

        pullStatus = True
        pullMsg = 'succ!'
        cur_time = int(time.time())
        endTime = cur_time - 8*60*60 - DELAYTIME*60 - (cur_time%60)
        startTime = endTime - 60
        endTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(endTime))
        startTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(startTime))
        for allocationId in allocationIds:
            status, datas = NATBandwidth().getDescribeBandwidthPackagePublicIpMonitorData(allocationId, startTime, endTime)
            if status:
                if len(datas) == 0:
                    pullStatus = False
                    pullMsg = u'查询 %s NAT带宽包中指定公网IP的监控数据: 未获取数据' % allocationId
                for data in datas:
                    STATSD_GAUGE.send("nat.rx." + allocationId, data['ReceivedBandwidth'])
                    STATSD_GAUGE.send("nat.tx." + allocationId, data['TransportedBandwidth'])
            else:
                pullStatus = False
                pullMsg = u'查询 %s NAT带宽包中指定公网IP的监控数据: %s' % (allocationId, str(datas))

        return pullStatus, pullMsg
    except Exception, ex:
        return False, u'异常:' + str(ex)

def pullSlbBandwidthData():
    '''
        拉取负载均衡SLB的带宽数据
    '''
    try:
        instanceIds = []
        status, datas = SLBBandwidth().getDescribeLoadBalancers()
        if status:
            for data in datas:
                instanceIds.append(data['LoadBalancerId'])
        else:
            return False, u'查询SLB所有的外网实例失败 : %s' % str(datas)

        pullStatus = True
        pullMsg = 'succ!'
        cur_time = int(time.time())
        endTime = cur_time - DELAYTIME*60 - (cur_time%60)
        startTime = endTime - 60
        metric_list = ['InstanceTrafficRX', 'InstanceTrafficTX']
        for metric in metric_list:
            status, datas = SLBBandwidth().getQueryMetricList(startTime * 1000, endTime * 1000, metric)
            if status:
                datas = json.loads(datas)
                if len(datas) == 0:
                    pullStatus = False
                    pullMsg = u'查询 %s SLB的带宽监控数据错误 : 没有查询到数据' % metric
                for data in datas:
                    instanceId = data['instanceId']
                    if instanceId in instanceIds:
                        average = int(round(data['Average']))
                        if metric == 'InstanceTrafficRX':
                            STATSD_GAUGE.send('slb.rx.'+instanceId, average)
                        else:
                            STATSD_GAUGE.send('slb.tx.' + instanceId, average)
            else:
                pullStatus = False
                pullMsg = u'查询 %s SLB的带宽监控数据错误 : %s' % (metric, str(datas))
        return pullStatus, pullMsg
    except Exception, ex:
        return False, u'异常:' + str(ex)

def pullRedisData():
    '''
        拉取拉取Redis的数据
    '''
    try:
        pullStatus = True
        pullMsg = 'succ!'
        cur_time = int(time.time())
        endTime = cur_time - DELAYTIME*60 - (cur_time%60)
        startTime = endTime - 60
        metric_list = ['MemoryUsage', 'ConnectionUsage', 'CpuUsage', 'IntranetIn', 'IntranetOut']
        for metric in metric_list:
            status, datas = SLBBandwidth().getQueryMetricList(startTime * 1000, endTime * 1000, metric, 'acs_kvstore')
            if status:
                datas = json.loads(datas)
                if len(datas) == 0:
                    pullStatus = False
                    pullMsg = u'查询 %s Redis监控数据错误 : 没有查询到数据' % metric
                for data in datas:
                    instanceId = data['instanceId']

                    if metric == 'MemoryUsage':
                        STATSD_GAUGE.send('redis.memory.percent.' + instanceId, int(round(data['Maximum']*100)))
                    elif metric == 'ConnectionUsage':
                        STATSD_GAUGE.send('redis.connection.percent.' + instanceId, int(round(data['Maximum']*100)))
                    elif metric == 'CpuUsage':
                        STATSD_GAUGE.send('redis.cpu.percent.' + instanceId, int(round(data['Maximum']*100)))
                    elif metric == 'IntranetIn':
                        STATSD_GAUGE.send('redis.intranet.in.' + instanceId, int(round(data['Maximum'])))
                    else:
                        STATSD_GAUGE.send('redis.intranet.out.' + instanceId, int(round(data['Maximum'])))
            else:
                pullStatus = False
                pullMsg = u'查询 %s Redis监控数据错误 : %s' % (metric, str(datas))

        return pullStatus, pullMsg
    except Exception, ex:
        return False, u'异常:' + str(ex)

def pullVpnData():
    '''
        拉取拉取VPN的数据
    '''
    try:
        pullStatus = True
        pullMsg = 'succ!'
        cur_time = int(time.time())
        endTime = cur_time - DELAYTIME*60 - (cur_time%60)
        startTime = endTime - 60
        metric_list = ['net_rx.rate', 'net_tx.rate']
        for metric in metric_list:
            status, datas = SLBBandwidth().getQueryMetricList(startTime * 1000, endTime * 1000, metric, 'acs_vpn')
            if status:
                datas = json.loads(datas)
                if len(datas) == 0:
                    pullStatus = False
                    pullMsg = u'查询 %s VPN监控数据错误 : 没有查询到数据' % metric
                for data in datas:
                    instanceId = data['instanceId']

                    if metric == 'net_rx.rate':
                        STATSD_GAUGE.send('vpn.net.rx.' + instanceId, int(round(data['Value'])))
                    else:
                        STATSD_GAUGE.send('vpn.net.tx.' + instanceId, int(round(data['Value'])))
            else:
                pullStatus = False
                pullMsg = u'查询 %s Redis监控数据错误 : %s' % (metric, str(datas))

        return pullStatus, pullMsg
    except Exception, ex:
        return False, u'异常:' + str(ex)

@app.task
def pullDataService():

    cur_time = int(time.time())
    endTime = cur_time - DELAYTIME * 60 - (cur_time % 60)
    startTime = endTime - 60
    timeQuantum = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime)) + ' ~ ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(endTime)) + ']'

    print(u'########### 拉取阿里云的带宽数据到grafana的job 开始执行 ###########')
    status, msg = pullNatBandwidthData()
    if status:
        print(u'%s    NAT网关的带宽数据到grafana的job 执行结束' % timeQuantum)
    else:
        print(u'%s    NAT网关的带宽数据到grafana的job 执行失败 : %s' % (timeQuantum, msg))
        print(u'告警!')

    status, msg = pullSlbBandwidthData()
    if status:
        print(u'%s    SLB的带宽数据到grafana的job 执行结束' % timeQuantum)
    else:
        print(u'%s    SLB的带宽数据到grafana的job 执行失败 : %s' % (timeQuantum, msg))
        print(u'告警!')

    status, msg = pullRedisData()
    if status:
        print(u'%s    Redis的监控数据到grafana的job 执行结束' % timeQuantum)
    else:
        print(u'%s    Redis的监控数据到grafana的job 执行失败 : %s' % (timeQuantum, msg))
        print(u'告警!')

    status, msg = pullVpnData()
    if status:
        print(u'%s    VPN的监控数据到grafana的job 执行结束' % timeQuantum)
    else:
        print(u'%s    VPN的监控数据到grafana的job 执行失败 : %s' % (timeQuantum, msg))
        print(u'告警!')

    print(u'########### 拉取阿里云的监控数据到grafana的job 执行结束 ###########')

if __name__ == '__main__':
    pullDataService()