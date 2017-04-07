#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by LJ on 2017/3/27
from bs4 import BeautifulSoup
import requests



HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

# 获取soup对象
def getSoup(url):
    request = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(request.content, 'lxml')
    return soup


if __name__ == '__main__':
    pass