# !/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: Python 时间相关的操作
# Create Date: 2018-06-02
# Modify Date: 2018-06-02
import calendar
import time, datetime


##########################################   获取本月一号和上月一号的时间戳    ##########################################
per_month_firstday = str(
    (datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1)) + ' 00:00:00'

per_month_timestamp = int(
    time.mktime(time.strptime(per_month_firstday, "%Y-%m-%d %H:%M:%S")))   # 获取上月一号的时间戳

this_month_firstday = str(datetime.date.today().replace(day=1)) + ' 00:00:00'
this_month_timestamp = int(
    time.mktime(time.strptime(this_month_firstday, "%Y-%m-%d %H:%M:%S")))  # 获取本月一号的时间戳
##########################################   获取本月一号和上月一号的时间戳    ##########################################

##########################################   获取上月一号的时间    ##########################################
month_firstday = str((datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1))
##########################################   获取上月一号的时间    ##########################################

##########################################   获取指定年月的天数    ##########################################
calendar.monthrange(datetime.datetime.now().year,datetime.datetime.now().month)[1]
##########################################   获取指定年月的天数    ##########################################

##########################################   指定临近三个月的时间戳    ##########################################
month_time = '2018-05' + '-01'
year_month = month_time.split('-')
year = int(year_month[0])
month = int(year_month[1])
if month == 1:
    bmonth = 12
    byear = year - 1
else:
    bmonth = month - 1
    byear = year

month_day = calendar.monthrange(year, month)[1]
bmonth_day = calendar.monthrange(byear, bmonth)[1]

month_time_timestamp = int(time.mktime(time.strptime(month_time, "%Y-%m-%d")))
bmonth_time_timestamp = month_time_timestamp - bmonth_day * 24 * 3600
nmonth_time_timestamp = month_time_timestamp + month_day * 24 * 3600
##########################################   指定临近三个月的时间戳    ##########################################

##########################################   时间戳转时间字符串    ##########################################
timeStamp = 1381419600
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))
##########################################   时间戳转时间字符串    ##########################################

################################  起始时间, 终止时间 获取区间中每天  ################################

import datetime

start = '2018-08-01'
end = '2018-08-03'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

while datestart <= dateend:
    datestart += datetime.timedelta(days=1)
    print type(datestart.strftime('%Y-%m-%d'))

################################  起始时间, 终止时间 获取区间中每天  ################################