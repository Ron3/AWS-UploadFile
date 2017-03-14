#coding=utf-8
"""
Create On 2017/3/13

@author: Ron2
"""



import traceback
from zope.interface import implements
from twisted.python import usage, log
from twisted.plugin import IPlugin
from twisted.application import internet, service
from twisted.web.server import Site

import http_receive_error

class Options(usage.Options):

    optParameters = [
        ["port", None, 7777, "Port for http server ."],
        ]

class BS2ServiceMaker(object):

    implements(service.IServiceMaker, IPlugin)

    tapname = "bs2err"
    description = "Black Pearl BlackSG Server"
    options = Options

    def makeService(self, options):
        top_service = service.MultiService()

        port = int(options["port"])
        httpServer = http_receive_error.HttpServer(port)
        httpService = internet.TCPServer(httpServer.port, Site(httpServer.root))
        
        ''' 启动游戏循环 '''
        gameLoopService = internet.TimerService(1, http_receive_error.gameLoop)

        httpService.setServiceParent(top_service)
        gameLoopService.setServiceParent(top_service)
        return top_service


service_maker = BS2ServiceMaker()

