#coding=utf-8
"""
Create On 2017/3/13

@author: Ron2
"""

import json
import traceback
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site


class HttpResource(Resource, object):
    """
    http的资源服务器
    """
    def __init__(self):
        Resource.__init__(self)


    def render_POST(self, request):
        """
        收到POST请求
        :param request:
        :return:
        """
        try:
            # 在这里解开数据
            data = request.content.read()
            dataDic = json.loads(data)
            requestType = dataDic.get("type")
            if requestType == None:
                return



        except:
            pass
        finally:
            return json.dumps({"errMsg": "success", "errCode": 0})



    def render_GET(self, request):
        """
        收到GET请求
        :param request:
        :return:
        """
        return json.dumps({"errMsg": "get"})





class HttpServer(object):
    """
    接收存档错误的HTTP服务器
    """
    def __init__(self, port):
        """
        :param port:                        端口
        """
        self.port = port
        self.root = None
        self.setup()


    def setup(self):
        """
        :return:
        """
        try:
            _root = Resource()
            _root.putChild("error_data", HttpResource())
            self.root = _root
        except:
            traceback.print_exc()


if __name__ == "__main__":
    httpServer = HttpServer(8080)
    reactor.listenTCP(httpServer.port, Site(httpServer.root))
    reactor.run()

