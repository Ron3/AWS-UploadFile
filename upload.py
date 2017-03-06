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


aws_key = os.environ.get("aws_access_key_id")
aws_secret = os.environ.get("aws_secret_access_key")
region_name = os.environ.get("AWS_REGION")

'''
别人说，session写在这里。在同一个container里，他是会重用的
我已经在看过他的id,测试环境里，确实看到他的id是不变的
但不知道这样理解重用这个session对不对？
'''
session = boto3.Session(aws_access_key_id=aws_key,
                        aws_secret_access_key=aws_secret,
                        region_name=region_name)

name = "shxd-s3"
s3 = session.resource('s3')


def upload_handler(event, context):
    """
    上传处理的函数
    :param event:
    :param context:
    :return:
    """
    print "session=> ", id(session)
    print "os.environ ==> ", os.environ

    fileName = event.get("fileName")
    if fileName == None:
        return json.dumps({"errMsg": "fileName error"})

    data = event.get("fileData")
    if data == None:
        return json.dumps({"errMsg": "fileData error"})

    # path = "/tmp/" + fileName
    # fileObj = open(path, "wb")
    # fileObj.write(data)
    # fileObj.close()

    # aws_key = os.environ.get("aws_access_key_id")
    # aws_secret = os.environ.get("aws_secret_access_key")
    # region_name = os.environ.get("AWS_REGION")

    # session = boto3.Session(aws_access_key_id=aws_key,
    #                         aws_secret_access_key=aws_secret,
    #                         region_name=region_name)



    s3.Bucket(name).put_object(Key=fileName, Body=data)

    return json.dumps({"errMsg": "upload success", "sha1": "00000000"})



