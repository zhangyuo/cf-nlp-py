#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-26 20:39
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : gaode_interface.py
# @Software : PyCharm
# @Desc     :
"""
import json

import requests
from math import radians, cos, sin, asin, sqrt

from geopy.distance import geodesic


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里

    return c * r * 1000

def address_extract(text):
    session = requests.Session()
    session.headers = {"Content-Type": "application/json"}
    # session.proxies = {"http":"", "https": ""}

    # 百度开放平台address接口-https://ai.baidu.com/ai-doc/NLP/vk6z52h5n
    access_token = "24.943decb903ba71fae61eba9900d91c84.2592000.1601037376.282335-22269163"
    URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/address" + "?access_token=" + access_token
    # result = session.post(URL, json=text, timeout=5)
    # print(result.text)

    # 高德-https://lbs.amap.com/api/webservice/guide/api/georegeo
    api_key = "6aee72fb716339e61042505e33e68b45"
    URL = "https://restapi.amap.com/v3/geocode/geo?address=%s&output=json&key=%s" % (text["text"], api_key)
    result = session.get(URL, timeout=5)
    print(result.text)
    return json.loads(result.text)["geocodes"][0]["location"].split(",")

    # from xml.dom.minidom import parseString
    #
    # domobj = parseString(result.text)
    # elementobj = domobj.documentElement
    # subElementobj = elementobj.getElementsByTagName("geocode")
    # for e in subElementobj:
    #     city = e.getElementsByTagName("location")[0]
    #     name = city.childNodes[0].data
    #     print(name)
    #     return name.split(",")

    # return []


if __name__ == "__main__":
    text = {"text": "江岸区蔡家田北区6栋4单元5层1室"}
    location1 = address_extract(text)
    lon1, lat1 = float(location1[0]), float(location1[1])
    text = {"text": "武汉市江岸区蔡家田A区4栋5单元1层1室司法拍卖"}
    # text = {"text": "佛山市顺德区龙江镇儒林大街太平巷横三巷4号"}
    location2 = address_extract(text)
    lon2, lat2 = float(location2[0]), float(location2[1])
    distance = haversine(lon1, lat1, lon2, lat2)
    print(distance)
    print(geodesic((lat1, lon1), (lat2, lon2)).m)  # 计算两个坐标直线距离



