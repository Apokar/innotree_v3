# -*- coding: utf-8 -*-
# @Time         : 2018/3/12 14:48
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : add_production_2.0.py
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


def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


# 代理部分
def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


# 清理数据
def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')
    detag = detag.replace('"', ' ” ')
    detag = detag.replace("'", " ” ")

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


def get_id_fromDB():
    conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="innotree",
                           charset="utf8")
    cursor = conn.cursor()

    today_date = time.strftime("%Y-%m-%d")
    cursor.execute('select distinct corp_id from table_innotree_investment_info where datestamp = "' + today_date + '"')
    all_ids = []
    all = cursor.fetchall()
    for x in range(len(all)):
        all_ids.append(all[x][0])

    cursor.execute('select company_id from table_innotree_company_production_info')
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

        # url = 'https://www.innotree.cn/inno/company/' + id + '.html'
        # ct = get_parse(url)
        #
        # if ct:
        #     content = str(ct.text)
            # print content

            ############产品信息#############
        product_content = get_product_parse(id)
        if product_content:
            p_content = product_content.text
            data = json.loads(p_content)
            product_info = data["data"]
            if product_info == []:
                print '公司id: ' + id + ' 没有产品信息 @ ' + str(datetime.datetime.now())


                cursor.execute(
                    'insert into table_innotree_company_production_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
                        id
                        , 'no_data'
                        , 'no_data'
                        , 'no_data'
                        , 'no_data'
                        , str(datetime.datetime.now())
                        , str(datetime.datetime.now())[:10]
                    ))
                conn.commit()

            else:
                print product_info
                print len(product_info)
                for x in range(len(product_info)):
                    print product_info[x]['introduction']
                    print product_info[x]['logo']
                    print product_info[x]['sName']
                    print product_info[x]['score']

                    cursor.execute(
                        'insert into table_innotree_company_production_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
                            id
                            , product_info[x]['sName']
                            , product_info[x]['logo']
                            , product_info[x]['score']
                            , detag(product_info[x]['introduction'])
                            , str(datetime.datetime.now())
                            , str(datetime.datetime.now())[:10]
                        ))
                    conn.commit()
                    print '公司id: ' + id + ' 的产品信息 插入成功 @ ' + str(datetime.datetime.now())


    except:
        print traceback.format_exc()


if __name__ == '__main__':
    # while True:
    proxies = get_proxy()
    need_ids = get_id_fromDB()

    start_no = 0
    end_no = len(need_ids)
    thread_num = 5
    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=get_info, args=(need_ids[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num
    print '执行完毕  _@_ ' + str(datetime.datetime.now()) + 'sleep 24 hours and run again, don\'t kill me '
    time.sleep(86400)

    # id = '3467672994577708827'
    # get_info(id)
