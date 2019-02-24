from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import pymysql
from langconv import *


# 简体转换繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line


data = []
for ii in range(20):
    print(ii)
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    url = 'https://www.qmsjmfb.com'
    result = requests.get(url, headers=headers).content
    soup = BeautifulSoup(result, 'lxml')
    ul = soup.find('ul', attrs={'class': 'name_show'}).find_all('li')
    repeat = 0
    add = 0
    for i in ul:
        x = i.text
        # 繁体
        # x = chs_to_cht(i.text)
        # 去掉括号内中文
        # x = x[0:x.rfind('(', 1)]
        data.append(x)
l1 = list(set(data))
print(len(l1))
db = pymysql.connect(host="localhost", user="root", password="root", db="fb")
cur = db.cursor()
sql = 'INSERT INTO NAME (NAME, TYPE) VALUES'
for i in l1:
    sql += '("%s", 0),' % i
sql = sql[0:len(sql)-1]
print(sql)
cur.execute(sql)
print("成功添加%d条数据" % len(l1))
db.close()
