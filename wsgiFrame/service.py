# -*- coding:utf-8 -*-
import re

from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server

class DictObj:

    def __init__(self, d):
        self._dict = d

    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found.'.format(item))

class Context(dict):

    def __getattr__(self, item):
        try:
            return self[item]
        except Exception, ex:
            raise AttributeError('Attribute {} Not Found.'.format(item))

    def __setattr__(self, key, value):
        self[key] = value

class NestedContext(Context):

    def __init__(self, globalcontext=None):
        super(NestedContext, self).__init__()
        self.globalcontext = globalcontext

    def relate(self, globalcontext=None):
        self.globalcontext = globalcontext

    def __getattr__(self, item):
        if item in self.keys():
            return self[item]
        return self.globalcontext[item]



class Route:

    ####################################################################################################################
    KVPATTERN = re.compile('/({[^{}:]+:?[^{}:]*})')
    TYPEPATTERNS = {
        'str': r'[^/]+',
        'word': r'\w+',
        'int': r'[+-]?\d+',
        'float': r'[+-]?\d+\.\d+',
        'any': r'.+'
    }

    TYPECAST = {
        'str': str,
        'word': str,
        'int': int,
        'float': float,
        'any': str
    }

    def _transform(self, kv):

        name, _, type = kv.strip('/{}').partition(':')
        return '/(?P<{}>{})'.format(name, self.TYPEPATTERNS.get(type, '\w+')), name, self.TYPECAST.get(type, str)

    def _parse(self, src):
        start = 0
        res = ''
        translator = {}
        while True:
            matcher = self.KVPATTERN.search(src, start)
            if matcher:
                res += matcher.string[start:matcher.start()]
                tmp = self._transform(matcher.string[matcher.start(): matcher.end()])
                res += tmp[0]
                translator[tmp[1]] = tmp[2]
                start = matcher.end()
            else:
                break
        if res:
            return res, translator
        else:
            return src, translator

    ####################################################################################################################

    def __init__(self, prefix):
        self.__prefix = prefix
        self.__routetable = []
        self.ctx = NestedContext()    # 绑定全局的上下问

        self.pre_interceptor = []    # 拦截器
        self.post_interceptor = []

    # Request 拦截器注册函数
    def register_preinterceptor(self, fn):
        self.pre_interceptor.append(fn)

    # Response 拦截器注册函数
    def register_postinterceptor(self, fn):
        self.post_interceptor.append(fn)

    def prefix(self):
        return self.__prefix

    def register(self, rule, *methods):
        def wrapper(handler):
            # /student/{name:str}/xxx/{id:int} =>
            # ('/student/(?P<name>[^/]+)/xxx/(?P<id>[+-]?\\d+)'), [<class 'str'>, <class 'int'>]
            pattern, translator = self._parse(rule)
            self.__routetable.append((methods, re.compile(pattern), translator, handler))
            return handler
        return wrapper

    def get(self, pattern):
        return self.register(pattern, 'GET')

    def post(self, pattern):
        return self.register(pattern, 'POST')

    def match(self, request):

        if not request.path.startswith(self.__prefix):
            return

        # 执行拦截器
        for fn in self.pre_interceptor:
            request = fn(self.ctx, request)

        for methods, pattern, trandlator, handler in self.__routetable:
            if (request.method.upper() in methods) or not methods:
                matcher = pattern.match(request.path.replace(self.__prefix, '', 1))
                if matcher:
                    # request.args = matcher.group()
                    # request.kwargs = matcher.groupdict()
                    newdict = {}
                    for k, v in matcher.groupdict().items():
                        newdict[k] = trandlator[k](v)
                    request.vars = DictObj(newdict)
                    reponse = handler(self.ctx, request)
                    for fn in self.post_interceptor:
                        reponse = fn(self.ctx, request, reponse)
                    return reponse



class Application:

    ##################################################
    # 全局上下文
    ctx = Context()
    def __init__(self, **kwargs):
        self.ctx.app = self
        for k, v in kwargs.items():
            self.ctx[k] = v
    ##################################################

    ##################################################
    # 拦截器
    RPE_INTERCEPTOR = []
    POST_INTERCEPTOR = []
    @classmethod
    def register_preinterceptor(cls, fn):
        cls.RPE_INTERCEPTOR.append(fn)

    @classmethod
    def register_postinterceptor(cls, fn):
        cls.POST_INTERCEPTOR.append(fn)
    ##################################################

    ##################################################
    ROUTETABLE = []    # 路由系统
    @classmethod
    def route(cls, *Routes):    # 注册路由函数
        cls.ROUTETABLE += Routes
        for Route in Routes:
            Route.ctx.relate(cls.ctx)
            Route.ctx.router = Route
    ##################################################

    @dec.wsgify
    def __call__(self, request):

        # Request全局拦截
        for fn in self.RPE_INTERCEPTOR:
            request = fn(self.ctx, request)

        for route in self.ROUTETABLE:
            response = route.match(request)
            if response:

                # Response全局拦截
                for fn in self.POST_INTERCEPTOR:
                    response = fn(self.ctx, request, response)

                return response

        raise exc.HTTPNotFound(u"您访问的页面被外星人劫持了")

r1 = Route('/sh/')
r2 = Route('/hhh/')
Application.route(r1, r2)

# @r1.get('^love$')
# def index(request):
#     res = Response()
#     res.body = "<h1>💗石豪喜欢贺焕焕💗</h1>"
#     return res

# @Application.post('^/shtohhh$')
# @Application.route('^/shtohhh$', 'GET', 'POST')
@r2.get('^love$')
def showpython(request):
    res = Response()
    res.body = "<h1>💗焕焕不喜欢石豪💗</h1>"
    return res

#######################################################################
# 拦截器举例子
# @Application.register_preinterceptor
# def showHeaders(ctx, request):
#     print(request.path)
#     print(request.user_agent)
#     return request
#
# @Application.register_postinterceptor
# def showHeaders(ctx, request, response):
#     print(response)
#     return response

# @r1.register_preinterceptor
@r1.get('love/{id:int}')
def showInfo(ctx, request):
    res = Response()
    res.body = "<h1>💗焕焕不喜欢石豪💗</h1>"
    return res

@r1.register_postinterceptor
def showResponse(ctx, request, reponse):
    print reponse
    return reponse

#######################################################################

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
