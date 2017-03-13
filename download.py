#coding=utf-8
"""
Create On 2017/3/13

@author: Ron2
"""

import boto3
import json
import traceback
import types
import os
import hashlib

session = boto3.Session()
name = "shxd-s3"
s3 = session.resource('s3')


def download_handler(event, context):
    """
    下载处理
    :param event:
    :param context:
    :return:
    """

    if type(event) != types.DictType:
        return json.dumps({"errMsg": "Data Resource Error[1]", "errCode": -1})

    userName = event.get("userName")
    if userName == None:
        return json.dumps({"errMsg": "Data Resource Error[2]", "errCode": -1})

    ''' 1, 然后按照规则.组成下载存档的名字 '''
    fileName = userName

    ''' 2, 去s3下载 '''
    skxdBucket = s3.Bucket(name)

    filePath = "/tmp/"
    fullPath = os.path.join(filePath, fileName)
    with open(fullPath, "wb") as data:
        skxdBucket.download_fileobj(fileName, data)

    ''' 3, 下载完成 '''
    fileObj = open(fullPath, "rb")
    data = fileObj.read()
    fileObj.close()

    print "data ==> ", data

    sha256 = hashlib.sha256()
    sha256.update(data)
    print "sha256 ==> ", sha256.hexdigest()

    return json.dumps({"errMsg": "download success", "errCode": 0})










