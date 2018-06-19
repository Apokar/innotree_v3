#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : HuaiZ
# first edit : 2017-11-2
# 爬取 近期 融资信息

import requests
import re
import MySQLdb
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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

round_dict = {
    "1.0": "种子轮",
    "2.0": "天使轮",
    "3.0": "Pre-A轮",
    "4.0": "A轮",
    "5.0": "A+轮",
    "6.0": "Pre-B轮",
    "7.0": "B轮",
    "8.0": "B+轮",
    "9.0": "Pre-C轮",
    "10.0": "C轮",
    "11.0": "C+轮",
    "12.0": "Pre-D轮",
    "13.0": "D轮",
    "14.0": "D+轮",
    "15.0": "E轮",
    "16.0": "F轮",
    "17.0": "G轮",
    "18.0": "H轮",
    "19.0": "Pre-IPO",
    "20.0": "新三板",
    "21.0": "新三板定增",
    "30.0": "PIPE",
    "40.0": "IPO",
    "41.0": "股票增发",
    "50.0": "并购",
    "60.0": "战略投资",
    "404.0": "未透露",
}

def get_proxies():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=86020600B1D5E92725E68858AEBCF346&status=1&type=static").text.split('\n')))
    return proxies


def get_one_page(url):
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        content = req.text
        return content
    else:
        print 'error code hz_001'


def get_info(content):
    content = content.replace('\\"', '"')

    full_names = re.findall('"name":"(.*?)","insts"', content)
    alias = re.findall('"alias":"(.*?)",', content)
    tags = re.findall('"tags":"(.*?)",', content)
    finance_time = re.findall('"idate":"(.*?)",', content)
    finance_amount = re.findall('"amount":"(.*?)",', content)
    round = re.findall('"round":(.*?)}', content)
    create_time = re.findall('"edate":"(.*?)",', content)
    location = re.findall('"address":"(.*?)",', content)
    invester_list = re.findall('"insts":\[{(.*?)}]', content)

    conn = MySQLdb.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306,
                           charset="utf8")
    cursor = conn.cursor()

    for i in range(10):
        invest = ''
        print full_names[i]
        print alias[i]
        print tags[i]
        print finance_time[i]
        print finance_amount[i]
        print round[i]
        print location[i]
        print create_time[i]

        invester_count = re.findall('"instName":"(.*?)"', invester_list[i])
        for x in range(len(invester_count)):
            invest += invester_count[x] + ' '
        print invest
        cursor.execute(
            'insert into table_innotree_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                full_names[i],
                alias[i],
                tags[i],
                finance_time[i],
                finance_amount[i],
                round_dict[round[i]],
                location[i],
                create_time[i],
                invest,
                str(datetime.datetime.now()),
                str(datetime.datetime.now())[:10]
            ))
        print alias[i] + '投资事件插入完成 ' + str(datetime.datetime.now())[:19]
    conn.commit()
    print '第 测试页 插入完成'


def main(url):
    content = get_one_page(url)

    get_info(content)


if __name__ == '__main__':
    url = 'https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st=1&ps=10&areaName=&rounds=&show=0&idate=&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain='

    main(url)
