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

    fileName = event.get("fileName")
    if fileName == None:
        return json.dumps({"errMsg": "fileName error"})

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
        
    return json.dumps({"errMsg": "upload success", "sha1": "00000000"})



