# -*- coding: utf-8 -*-
# @Time         : 2018/2/9 17:24
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : innotree_company_2.0.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : innotree
import json
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

import urllib3

urllib3.disable_warnings()

import re
import time
import requests
import threading
import random
import datetime
import MySQLdb


def isExist(object_item):
    if object_item:
        return object_item
    else:
        return 'Null'


# 代理部分
def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


def get_parse(url):
    headers = {
        'Host': 'www.innotree.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': 'https://www.innotree.cn/inno/database/totalDatabase',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_user_identify_=515633a0-0c83-308c-a400-4fb705304923; JSESSIONID=aaaujzKY7wBfbfNMQqBqw; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1529465712; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1529465712; uID=450357; sID=0764638aec963cbfbec65ee7a9a8adb5; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1529478428; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1529478428'

    }

    while True:
        try:

            index = random.randint(1, len(proxies) - 1)
            proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
            print 'Now Proxy is : ' + str(proxy) + ' @ ' + str(datetime.datetime.now())
            response = requests.get(url, timeout=30, proxies=proxy, headers=headers)
            if response.status_code == 200:
                print 'parse correct'
                return response
                break
            else:
                print 'parse error'
                return None
                break
        except Exception, e:

            print e
            if str(e).find('HTTPSConnectionPool') >= 0:
                time.sleep(3)
                continue
            elif str(e).find('HTTPConnectionPool') >= 0:
                time.sleep(3)
                continue
            else:
                return None
                break


def get_product_parse(id):
    product_url = 'https://www.innotree.cn/inno/company/ajax/projectlist?compId=' + id
    product_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '_user_identify_=515633a0-0c83-308c-a400-4fb705304923; JSESSIONID=aaaujzKY7wBfbfNMQqBqw; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1529465712; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1529465712; uID=450357; sID=0764638aec963cbfbec65ee7a9a8adb5; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1529478428; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1529478428',
        'Host': 'www.innotree.cn',
        'Referer': 'https://www.innotree.cn/inno/company/' + id + '.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    while True:
        try:

            index = random.randint(1, len(proxies) - 1)
            proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
            print 'Now Proxy is : ' + str(proxy) + ' @ ' + str(datetime.datetime.now())
            response = requests.get(product_url, timeout=30, proxies=proxy, headers=product_headers)
            if response.status_code == 200:
                print 'parse correct'
                return response
                break
            else:
                print 'parse error'
                return None
                break
        except Exception, e:

            print e
            if str(e).find('HTTPSConnectionPool') >= 0:
                time.sleep(3)
                continue
            elif str(e).find('HTTPConnectionPool') >= 0:
                time.sleep(3)
                continue
            else:
                return None
                break


# 正 则

def re_findall(pattern, html):
    if re.findall(pattern, html):
        return re.findall(pattern, html)
    else:
        return 'N'


def reS_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


# 清理数据
def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace('"', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')
    return detag


def splitag(html):
    detag = re.subn('<[^>]*>', '|', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')

    return detag


# 获得中文
def get_chinese(str):
    b = re.compile(u"[\u4e00-\u9fa5]*")
    c = "".join(b.findall(str.decode('utf8')))
    return c


def get_id_fromDB():

    conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="innotree",
                           charset="utf8")
    cursor = conn.cursor()

    today_date = time.strftime("%Y-%m-%d")
    cursor.execute('select distinct corp_id from table_innotree_investment_info where datestamp = "' + today_date+'"')
    all_ids = []
    all = cursor.fetchall()
    for x in range(len(all)):
        all_ids.append(all[x][0])

    cursor.execute('select company_id from table_innotree_company_baseinfo')
    old_ids = []
    old = cursor.fetchall()
    for y in range(len(old)):
        old_ids.append(old[y][0])

    need_ids = []
    for need_id in all_ids:
        if need_id not in old_ids:
            need_ids.append(need_id)

    cursor.close()
    conn.close()
    return need_ids


def get_info(id):
    try:
        conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="innotree",
                               charset="utf8")
        cursor = conn.cursor()

        url = 'https://www.innotree.cn/inno/company/' + id + '.html'
        ct = get_parse(url)

        if ct:

            content = str(ct.text)
            # print content
            title = \
                reS_findall('<title>(.*?)</title>', content)[
                    0].decode('utf8')
            print detag(title)
            if detag(title) == '首页_因果树':
                print '解析失败,跳转首页了'
                pass
            else:
                rounds = reS_findall('<span class="mech_170525_nav_h3_s01">(.*?)</span>', content)[0]
                print detag(rounds).replace('(', '').replace(')', '')

                province = re_findall('<a href="/inno/database/totalDatabase\?areasName=(.*?)"', content)[0]
                print detag(province)

                website = re_findall('href="(.*?)" class="mech_170822_nav_d02_a02"', content)[0]
                print website

                tag = re_findall('<a href="/inno/database/totalDatabase\?tagquery=(.*?)"', content)
                tags = '|'
                for x in tag:
                    tags += x + '|'
                print tags

                company_name = reS_findall('<span>公司中文名: </span>(.*?)</span>', content)[0]
                print detag(company_name)

                register_address = reS_findall('<span>注册地址: </span>(.*?)</span>', content)[0]
                print detag(register_address)

                create_time = reS_findall('<span>成立时间: </span>(.*?)</span>', content)[0]
                print detag(create_time)

                register_amount = reS_findall('<span>注册资本: </span>(.*?)</span>', content)[0]
                print detag(register_amount)

                legal_representative = reS_findall('<span>法人代表: </span>(.*?)</span>', content)[0]
                print detag(legal_representative)

                official_contact = reS_findall('<span>官方联系方式: </span>(.*?)</span>', content)[0]
                print detag(official_contact)

                company_brief = reS_findall('<h3 class="de_170822_d01_d02_h3">.*?:</h3>(.*?)</p>', content)[0]
                print detag(company_brief)

                cursor.execute(
                    'insert into table_innotree_company_baseinfo values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        id
                        , detag(title)[:-4]
                        , detag(rounds).replace('(', '').replace(')', '')
                        , detag(province)
                        , website
                        , tags
                        , detag(company_name)
                        , detag(register_address)
                        , detag(create_time)
                        , detag(register_amount)
                        , detag(legal_representative)
                        , detag(official_contact)
                        , detag(company_brief)
                        , str(datetime.datetime.now())
                        , str(datetime.datetime.now())[:10]
                    ))
                conn.commit()
                print '公司id: ' + id + ' 的基本信息 插入成功 @ ' + str(datetime.datetime.now())

    except:
        print traceback.format_exc()


if __name__ == '__main__':
    # while True:
    proxies = get_proxy()
    need_ids = get_id_fromDB()

    # start_no = 0
    # end_no = len(need_ids)
    # thread_num = 5
    # while start_no < (end_no - thread_num + 1):
    #     threads = []
    #
    #     for inner_index in range(0, thread_num):
    #         threads.append(threading.Thread(target=get_info, args=(need_ids[start_no + inner_index],)))
    #     for t in threads:
    #         t.setDaemon(True)
    #         t.start()
    #     t.join()
    #     start_no += thread_num
    for id in need_ids:
        get_info(id)
    print '执行完毕  _@_ ' + str(datetime.datetime.now())
    # id = '3467672994577708827'
    # get_info(id)