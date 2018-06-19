#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : HuaiZ
# first edit : 2017-11-2
# 爬取 近期 融资信息
import json

import requests
import re
import MySQLdb

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host="221.226.72.226", user="root", passwd="somao1129", db="innotree", port=13306, charset="utf8")
cursor = conn.cursor()
