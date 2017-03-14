# coding=utf-8
"""
Create On 2017/3/5

@author: Ron2
"""

#  pip install  requests -t /Users/Ron2/Documents/github/AWS-UploadFile
# import requests

import json
import boto3
import os
import time
import random
import traceback
import httplib

''' AWS第一台服务器的内网ip '''
EC2_IP = "172.31.0.115"
EC_PORT = 7777

session = boto3.Session()
name = "shxd-s3"
s3 = session.resource('s3')



def upload_handler(event, context):
    """
    上传处理的函数
    :param event:
    :param context:
    :return:
    """
    # print "session=> ", id(session), id(s3)
    # print "os.environ ==> ", os.environ

    userName = event.get("userName")
    if userName == None:
        return json.dumps({"errMsg": "userName error"})

    data = event.get("fileData")
    if data == None:
        return json.dumps({"errMsg": "fileData error"})

    ''' 写入s3.假设这里出了异常 '''
    try:
        fileName = str(int(time.time())) + ".txt"
        s3.Bucket(name).put_object(Key=fileName, Body=data)
    except:
        traceback.print_exc()
        print "[ConnectionError]Save S3 Error"
        global session, s3
        session = boto3.Session()
        s3 = session.resource('s3')

        ''' 写入s3失败.这里将数据写入到EC2 '''
        _post_to_ec2(userName, data)

    return json.dumps({"errMsg": "upload success", "sha1": "00000000"})




def _post_to_ec2(userName, fileData):
    """
    将数据写入到EC2
    :param userName:
    :param fileData:
    :return:
    """
    if userName == None or fileData == None:
        return

    try:
        ''' TODO 这里就涉及到数据结构. '''

        ''' 暴2的错误存档 '''
        REQUEST_TYPE_ERROR_GAME_DATA = 1101

        httpConn = httplib.HTTPConnection(EC2_IP, EC_PORT)
        httpConn.request("POST", "/error_data", json.dumps({"type": REQUEST_TYPE_ERROR_GAME_DATA, "key1": "RonRonRonRon1231"}))
        response = httpConn.getresponse()
        data = response.read()
        httpConn.close()

        print "EC2 ResponseData ==> ", data
    except:
        traceback.print_exc()






