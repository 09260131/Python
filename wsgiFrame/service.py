# -*- coding:utf-8 -*-
import re

from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server

class Application:

    ROUTETABLE = []

    @classmethod
    def route(cls, pattern, *methods):    # 注册路由函数
        def wrapper(handler):
            cls.ROUTETABLE.append((methods, re.compile(pattern), handler))    # 正则表达式寻找路径
        return wrapper

    @classmethod
    def get(cls, pattern):    # 过滤GET方法
        return cls.route(pattern, 'GET')

    @classmethod
    def post(cls, pattern):    # 过滤POST方法
        return cls.route(pattern, 'POST')

    @dec.wsgify
    def __call__(self, request):
        for methods, pattern, handler in self.ROUTETABLE:
            if (request.method.upper() in methods) or (not methods):
                if pattern.search(request.path):
                    return handler(request)
        raise exc.HTTPNotFound(u"您访问的页面被外星人劫持了")


@Application.get('^/$')
def index(request):
    res = Response()
    res.body = "<h1>💗石豪喜欢贺焕焕💗</h1>"
    return res

# @Application.post('^/shtohhh$')
@Application.route('^/shtohhh$', 'GET', 'POST')
def showpython(request):
    res = Response()
    res.body = "<h1>💗但是往往向往的东西越难获得💗</h1>"
    return res

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9998
    server = make_server(ip, port, Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
