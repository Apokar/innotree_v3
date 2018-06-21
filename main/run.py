#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : HuaiZ
# first edit : 2018-06-20
import time
import os


def main():
    while True:
        print 'run    innotree_investment.py'
        os.system('python D:\PycharmProjects\innotree_v3\\main\innotree_investment.py')
        time.sleep(5)

        print 'run    innotree_company_2.0.py'
        os.system('python D:\PycharmProjects\innotree_v3\\main\innotree_company_2.0.py')
        time.sleep(5)

        print 'run    add_team_2.0.py'
        os.system('python D:\PycharmProjects\innotree_v3\\main\\add_team_2.0.py')
        time.sleep(5)

        print 'run    add_shareholder_2.0.py'
        os.system('python2 D:\PycharmProjects\innotree_v3\\main\\add_shareholder_2.0.py')
        time.sleep(5)

        print 'run    add_production_2.0.py'
        os.system('python D:\PycharmProjects\innotree_v3\\main\\add_production_2.0.py')
        time.sleep(5)


        print 'run    add_financing_2.0.py'
        os.system('python D:\PycharmProjects\innotree_v3\\main\\add_financing_2.0.py')
        time.sleep(5)

        print '六个脚本跑完了,明天继续'
        time.sleep(86400)


if __name__ == '__main__':
    main()
