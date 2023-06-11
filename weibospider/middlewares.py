# encoding: utf-8

from scrapy import signals


class IPProxyMiddleware(object):
    """
    代理IP中间件
    """
    _proxy = ('XXX.XXX.com', '15818')
    @staticmethod
    
    def fetch_proxy():
        """
        获取一个代理IP
        """
        # You need to rewrite this function if you want to add proxy pool
        # the function should return an ip in the format of "ip:port" like "12.34.1.4:9090"
        return None

    

    def process_request(self, request, spider):

        # 用户名密码认证
        username = "username"
        password = "password"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ':'.join(IPProxyMiddleware._proxy)}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}

        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(IPProxyMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception