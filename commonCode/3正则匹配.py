import re

reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

s1 = '127.0.0.1'
ip_list = []
for _ip in reip.findall(s1):
    ip_list.append(_ip)