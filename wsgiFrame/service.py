# -*- coding:utf-8 -*-
import re

from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server

class Route:

    def __init__(self, prefix):
        self.__prefix = prefix
        self.__routetable = []

    def prefix(self):
        return self.__prefix

    def register(self, pattern, *methods):
        def wrapper(handler):
            self.__routetable.append((methods, re.compile(pattern), handler))
            return handler
        return wrapper

    def get(self, pattern):
        return self.register(pattern, 'GET')

    def post(self, pattern):
        return self.register(pattern, 'POST')

    def match(self, request):

        if not request.path.startswith(self.__prefix):
            return
        for methods, pattern, handler in self.__routetable:
            if (request.method.upper() in methods) or not methods:
                matcher = pattern.match(request.path.replace(self.__prefix, ''))
                if matcher:
                    request.args = matcher.group()
                    request.kwargs = matcher.groupdict()
                    return handler(request)


class Application:

    ROUTETABLE = []

    @classmethod
    def route(cls, *Routes):    # 注册路由函数
        cls.ROUTETABLE += Routes

    @dec.wsgify
    def __call__(self, request):
        for route in self.ROUTETABLE:
            response = route.match(request)
            if response:
                return response

        raise exc.HTTPNotFound(u"您访问的页面被外星人劫持了")

r1 = Route('/sh/')
r2 = Route('/hhh/')
Application.route(r1, r2)

@r1.get('^love$')
def index(request):
    res = Response()
    res.body = "<h1>💗石豪喜欢贺焕焕💗</h1>"
    return res

# @Application.post('^/shtohhh$')
# @Application.route('^/shtohhh$', 'GET', 'POST')
@r2.get('^love$')
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
