# -*- coding:utf-8 -*-

import re

pattern = re.compile('/({[^{}:]+:?[^{}:]*})')
t1 = '/student/{name:str}/xxx/{id:int}'
t2 = '/student/xxx/{id:int}/yyy'
t3 = 'student/{name:}/xxx/{id}'
t4 = '/student/{name:}/xxx/{id:string}'

TYPEPATTERNS = {
    'str': r'[^/]+',
    'word': r'\w+',
    'int': r'[+-]?\d+',
    'float': r'[+-]?\d+\.\d+',
    'any': r'.+'
}

TYPECAST = {
    'str' : str,
    'word': str,
    'int': int,
    'float': float,
    'any': str
}

def transform(kv):

    name, _, type = kv.strip('/{}').partition(':')
    return '/(?P<{}>{})'.format(name, TYPEPATTERNS.get(type, '\w+')), name, TYPECAST.get(type, str)

def parse(src):
    start = 0
    res = ''
    translator = {}
    while True:
        matcher = pattern.search(src, start)
        if matcher:
            res += matcher.string[start:matcher.start()]
            tmp = transform(matcher.string[matcher.start(): matcher.end()])
            res += tmp[0]
            translator[tmp[1]] = tmp[2]
            start = matcher.end()
        else:
            break
    if res:
        return res, translator
    else:
        return src, translator

if __name__ == '__main__':
    print parse(t1)


























