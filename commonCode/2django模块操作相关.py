# !/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: Python django 模块操作
# Create Date: 2018-06-03
# Modify Date: 2018-06-03

import os
import sys


project_path = os.path.abspath('../..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from consume.models import HostHoursAmount

#############################################  取某一个字段的去重集合  #############################################

commodities = list(HostHoursAmount.objects.exclude(month=u'月份').filter(month='2018年05月')
                   .values_list("commodity").distinct())
commoditie_list = [commoditie[0] for commoditie in commodities]  # 将产品类型去重

#############################################  取某一个字段的去重集合  #############################################