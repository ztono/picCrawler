# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 15:21
# @Author  : Junzheng Chen
# @Email   : 947142043@qq.com
# @File    : baidu_pic.py
# @Software: PyCharm

import requests


def download_picture(target_word, save_dir):
    '''
    :param target_word: 想爬取的关键词
    :param save_dir: 存储的目录，将会存储在%save_dir%/target_word
    :return:返回值，暂时没有
    '''
    pass


# target_word 可修改
target_word = "半身照"
url = "http://image.baidu.com/search/index?tn=baiduimage&ie=utf-8&word=" + target_word
html = requests.get(url)
