# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 15:21
# @Author  : Junzheng Chen
# @Email   : 947142043@qq.com
# @File    : baidu_pic.py
# @Software: PyCharm

import os
import random
import re
import time
from urllib.parse import urlencode

import requests


def baidu_decode(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d = {'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
         's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
         'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0',
         '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    if url is None or 'http' in url:
        return url
    else:
        j = url
        for m in c:
            j = j.replace(m, d[m])
        for char in j:
            if re.match('^[a-w\d]+$', char):
                char = d[char]
            res = res + char
        return res


def download_picture_batch(save_dir, param_dict):
    """
    :param param_dict: 参数字典
    :param save_dir: 存储的目录，将会存储在%save_dir%/target_word
    :return:返回值, -1代表不正常
    """
    url = 'https://image.baidu.com/search/acjson?' + urlencode(param_dict)
    try:
        result = requests.get(url)
        while result.status_code != 200:
            result = requests.get(url)
        json_result = result.json()
    except requests.ConnectionError as error:
        print("Connect error!", error.args)
        return -1
    pics = {}
    images_files = {}
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    if json_result.get('data'):
        for pic in json_result.get('data'):
            if pic.get("fromPageTitle"):
                title = pic.get("fromPageTitle")
            else:
                title = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(random.randint(0, 1000))
            title = cop.sub('', title)
            url = baidu_decode(pic.get("objURL"))
            if url:
                pics[url] = title
    else:
        print("Format unrecognized!")
        return -1
    for key in pics:
        try:
            response = requests.get(key)
            if response.status_code != 200:
                continue
            else:
                images_files[pics[key]] = response.content
        except requests.ConnectionError as error:
            print("Connect error!", error.args)
            continue
    if not (save_dir.endswith("\\") or save_dir.endswith("/")):
        save_dir += os.sep
    for key in images_files:
        file_path = save_dir + '{0}.{1}'.format(key, "jpg")
        with open(file_path, "wb") as f:
            f.write(images_files[key])
            print("File {0} Complete!".format('{0}.{1}'.format(key, "jpg")))
    return 0


def download_picture_baidu(batch_number, rn):
    for i in range(1, batch_number+1):
        download_picture_batch("./pics/", {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'queryWord': '半身像',
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '-1',
            'z': '',
            'ic': '0',
            'word': '半身像',
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '0',
            'istype': '2',
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'cg': 'girl',
            'pn': i * rn,
            'rn': rn,
            'gsm': '1e',
            '1537355234668': '',
        })


download_picture_baidu(100, 30)
