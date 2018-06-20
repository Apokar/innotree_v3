#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : HuaiZ
# first edit : 2018-6-19
# 爬取 近期 融资信息
import time
import traceback
import random
import urllib

import requests
import re
import pymysql
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


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


def get_timestamp(tt):

    timeArray = time.strptime(tt, "%Y-%m-%d")

    timeStamp = int(time.mktime(timeArray))

    return timeStamp


def get_proxies():
    proxy_list = list(set(urllib.urlopen(
        'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().split('\n')[
                          :-1]))
    index = random.randint(0, len(proxy_list) - 1)
    current_proxy = proxy_list[index]
    print "NEW PROXY:\t%s" % current_proxy
    proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
    return proxies


def get_one_page(url):
    while True:
        try:
            proxies = get_proxies()
            req = requests.get(url, headers=headers, proxies=proxies)
            if req.status_code == 200:
                content = req.text
                return content
            else:
                print 'error code hz_001'
                continue

        except Exception,e:

            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'Max retries exceeded with url'
                continue
            else:
                print str(e)
                break


def get_info(content, finished_stamp):
    while True:
        try:
            content = content.replace('\\"', '"')

            full_names = re.findall('"name":"(.*?)",', content)
            alias = re.findall('"alias":"(.*?)",', content)
            corp_id = re.findall('"ncid":"(.*?)",', content)
            tags = re.findall('"tags":"(.*?)",', content)
            finance_time = re.findall('"idate":"(.*?)",', content)
            finance_amount = re.findall('"amount":"(.*?)",', content)
            round = re.findall('"round":(.*?)}', content)
            create_time = re.findall('"edate":"(.*?)",', content)
            location = re.findall('"address":"(.*?)",', content)
            invester_list = re.findall('"insts":\[{(.*?)}]', content)

            today_date = time.strftime("%Y-%m-%d")
            today_stamp = get_timestamp(today_date)

            conn = pymysql.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306,
                                   charset="utf8")
            cursor = conn.cursor()

            for i in range(10):
                print '第'+str(i+1)+'条'
                invest = ''
                print full_names[i]
                print finance_time[i]
                # print alias[i]
                # print tags[i]
                # print finance_time[i]
                # print finance_amount[i]
                # print round[i]
                # print location[i]
                # print create_time[i]
                finance_stamp = get_timestamp(finance_time[i])
                invester_count = re.findall('"instName":"(.*?)"', invester_list[i])
                for x in range(len(invester_count)):
                    invest += invester_count[x] + ' '
                # print invest

                print str(finished_stamp)
                print str(finance_stamp) + ' ' + str(finance_time[i])
                print str(today_stamp) + ' ' + str(today_date)
                if finished_stamp < get_timestamp(finance_time[i]) < today_stamp:
                    cursor.execute(
                        'insert into table_innotree_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                            full_names[i],
                            alias[i],
                            corp_id[i],
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
                    conn.commit()
                    print alias[i] + '  投资事件插入完成 ' + str(datetime.datetime.now())[:19]

                elif get_timestamp(finance_time[i]) == today_stamp:
                    print '今天刚更新的内容 保证完整性 先不爬'

                else:

                    print ' 根据时间限制 无可爬内容 睡眠1天 86400秒后继续;'
                    quit()

            print '插入完成'
            break
        except Exception, e:
            print traceback.format_exc()

            if str(e).find('20006') >= 0:
                cursor.close()
                conn.close()
                conn = pymysql.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306,
                                   charset="utf8")
                cursor = conn.cursor()
                print '数据库连接重启 ' + str(datetime.datetime.now())[:19]
                time.sleep(3)
                continue
            elif str(e).find('20003') >= 0:
                cursor.close()
                conn.close()
                conn = pymysql.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree",
                                       port=13306,
                                       charset="utf8")
                cursor = conn.cursor()
                print '数据库连接重启 ' + str(datetime.datetime.now())[:19]
                time.sleep(3)
                continue
            elif str(e).find('IndexError'):
                print content
                time.sleep(10)
                continue
            else:
                break


def main(url, finished_stamp):
    content = get_one_page(url)

    get_info(content,finished_stamp)


def add_corp_info(finished_stamp):
    # finished_stamp = '2018-06-15'
    conn = pymysql.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306,
                           charset="utf8")
    cursor = conn.cursor()

    # cursor.execute('select a.corp_id from table_innotree_investment_info a left join table_innotree_company_baseinfo b on a.corp_id = b.company_id where a.last_finance_time > ' + str(finished_stamp) +' and b.company_id is null ')
    cursor.execute('select a.corp_id from table_innotree_investment_info a where a.last_finance_time > ' + str(finished_stamp) )

    corp_id_list = cursor.fetchall()

    print corp_id_list


if __name__ == '__main__':
    while True:
        conn = pymysql.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306,
                               charset="utf8")
        cursor = conn.cursor()

        cursor.execute('select max(last_finance_time) from table_innotree_investment_info')

        finished_date = cursor.fetchall()[0][0]
        finished_stamp = get_timestamp(finished_date)
        cursor.close()
        conn.close()

        print '上次爬结束的 日期是 : ' + finished_date


        for i in range(1,10):
            url = 'https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st='+str(i)+'&ps=10&areaName=&rounds=&show=0&idate=&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain='

            main(url,finished_stamp)

            print '第'+str(i)+'一页爬好了'

            time.sleep(3)








