# coding=utf-8
"""
Create On 2017/3/5

@author: Ron2
"""


import json
import httplib

# 23.248.162.44:8080/listen
conn = httplib.HTTPConnection("23.248.162.44", 8080)
print "conn ==> ", id(conn)


def upload_handler(event, context):
    """
    :param event:
    :param context:
    :return:
    """

    conn.request("POST", "/listen")
    response = conn.getresponse()
    data = response.read()

    return json.dumps({"errMsg": "upload success", "sha1": data})

