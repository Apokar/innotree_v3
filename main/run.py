#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : HuaiZ
# first edit : 2018-06-20
import time
import traceback
import random
import urllib

import requests
import re
import pymysql
import datetime
import sys

headers = {
    "Host": "www.innotree.cn",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cookie": "_user_identify_=c1320e98-14d3-315f-8a53-5839cc893625; JSESSIONID=aaaGJVFn9qVax8McIUvqw; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1529372878; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1529372878; uID=463157; sID=f71d75366d480fae6a0c2a5c7a24a626; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1529378884; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1529378884"
}


def get_proxies():

    proxy_list = list(set(urllib.urlopen(
        'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().split('\n')[
                          :-1]))
    index = random.randint(0, len(proxy_list) - 1)
    current_proxy = proxy_list[index]
    print "NEW PROXY:\t%s" % current_proxy
    proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
    return proxies

def get_one_page(url,proxies):

    req = requests.get(url,  headers=headers, proxies=proxies)
    print req.status_code
    if req.status_code == 200:
        content = req.text

        return content
    else:
        print 'error code hz_001'


if __name__ == '__main__':
    proxies = get_proxies()
    i = 1
    url = 'https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st='+str(i)+'&ps=10&areaName=&rounds=&show=0&idate=&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain='
    print get_one_page(url,proxies)
