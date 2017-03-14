#coding=utf-8
"""
Create On 2017/3/13

@author: Ron2
"""


import json
import os
import time
import base64
import traceback
from twisted.internet import task
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site


''' 暴2的错误数据的根目录 '''
ERROR_DATA_DIR = "/data/bpsg/bs2_error_data"

''' 心跳包 '''
HTTP_REQUEST_TYPE_HEARTBEAT = 1001

''' 暴2的错误存档 '''
REQUEST_TYPE_ERROR_GAME_DATA = 1101


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

            if requestType == HTTP_REQUEST_TYPE_HEARTBEAT:      # 心跳包
                return

            if requestType == REQUEST_TYPE_ERROR_GAME_DATA:     # 处理错误的存档
                self._handleErrorGameData(dataDic)

        except:
            traceback.print_exc()
        finally:
            return json.dumps({"errMsg": "success", "errCode": 0})



    def render_GET(self, request):
        """
        收到GET请求
        :param request:
        :return:
        """
        return json.dumps({"errMsg": "get"})


    def _handleErrorGameData(self, dataDic):
        """
        处理错误的暴2存档
        :param dataDic:                         原始HTTP数据
        :return:
        """
        userName = dataDic.get("userName")
        fileData = dataDic.get("fileData")
        if userName == None or fileData == None:
            return

        fileData = base64.decodestring(fileData)

        ''' fileData '''
        fileName = userName + "_"
        fileName += str(int(time.time()))
        fullPath = os.path.join(ERROR_DATA_DIR, fileName)

        # print "fullPath ==> ", fullPath
        # print "fileData ==> ", fileData

        fileObj = open(fullPath, "wb")
        fileObj.write(fileData)
        fileObj.close()



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


def gameLoop():
    """
    循环
    :return:
    """
    print str(time.time())


if __name__ == "__main__":
    httpServer = HttpServer(7777)
    reactor.listenTCP(httpServer.port, Site(httpServer.root))

    loop = task.LoopingCall(gameLoop)
    loop.start(1)

    reactor.run()

