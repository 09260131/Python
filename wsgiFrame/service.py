# -*- coding:utf-8 -*-
import re

from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server

class Application:

    ROUTETABLE = []

    @classmethod
    def register(cls, pattern):
        def wrapper(handler):
            cls.ROUTETABLE.append((re.compile(pattern), handler))
        return wrapper

    @dec.wsgify
    def __call__(self, request):

        for pattern, handler in self.ROUTETABLE:
            if pattern.search(request.path):
                return handler(request)
        raise exc.HTTPNotFound(u"您访问的页面被外星人劫持了")


@Application.register('^/$')
def index(request):
    res = Response()
    res.body = "<h1>💗石豪喜欢贺焕焕💗</h1>"
    return res

@Application.register('^/shtohhh$')
def showpython(request):
    res = Response()
    res.body = "<h1>💗但是往往向往的东西越难获得💗</h1>"
    print "hhh"
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
