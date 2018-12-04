# -*- coding:utf-8 -*-

import requests
import urllib3
import time
from bs4 import BeautifulSoup
from pymysql import *
import sys
from fake_useragent import UserAgent
sys.getdefaultencoding()

'''
今日头条文章内容抓取，主要抓取的是中国经济网、华尔街见闻、人民网、海外网、环球网、#经济日报、观察者网等网站文章内容
'''

#中国经济网
def loadLink(source_url):
    ua = UserAgent()
    headers = {
        'User-Agent':ua.random,
    }

    body = requests.get(source_url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.01)

    #中文乱码处理
    soup = body.encode('raw_unicode_escape')
    soup = soup.decode()

    response = BeautifulSoup(soup,'lxml')
    time.sleep(0.01)

    soup2 = response.find_all('article')
    soup2 = soup2[0]
    soup2 = str(soup2)
    soup2 = soup2[9:-10].strip()
    print(soup2)

    return soup2

# 华尔街见闻、人民网、海外网
def loadLink2(source_url):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    body = requests.get(source_url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.01)
   
    response = BeautifulSoup(body, 'lxml')
    time.sleep(0.01)

    soup = response.find_all('article')
    try:
        soup = soup[0]
    except:
        return '[]'
    soup = str(soup)
    print(soup)

    return soup

# 环球网
def loadLink3(source_url):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    body = requests.get(source_url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.01)

    response = BeautifulSoup(body, 'lxml')
    time.sleep(0.01)

    soup = response.find_all('div',{'class':'a-con'})

    try:
        soup = soup[0]
    except:
        return '[]'
    soup = str(soup)
    print(soup)

    return soup

#经济日报、观察者网
def loadLink4(source_url):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    body = requests.get(source_url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.1)

    soup = body.encode('raw_unicode_escape')
    soup = soup.decode()

    response = BeautifulSoup(soup, 'lxml')
    time.sleep(0.01)

    soup2 = response.find_all('article')

    try:
        soup2 = soup2[0]
    except:
        return '[]'
    soup2 = str(soup2)
    print(soup2)

    return soup2

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="Spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = 'SELECT display_url,id,article_content FROM toutiao'
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(20694,21125):
        url = data[i][0]
        #print(url)
        id = data[i][1]
        content = data[i][2]

        if content == '[]':
        #if content != '1':
            page = loadLink2(url)
            #time.sleep(10000)
            n = id
            n = str(n)
            params = [page,n]
            try:
                sql = """update toutiao set article_content=%s WHERE id=%s"""
                cursor.execute(sql,params)
                db.commit()
            except:
                db.rollback()
            time.sleep(0.1)
        else:
            print('hahaha')

    db.close()
