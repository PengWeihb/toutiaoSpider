# -*- coding:utf-8 -*-

import requests
import urllib3
import time
from bs4 import BeautifulSoup
from pymysql import *
import sys
from fake_useragent import UserAgent

sys.getdefaultencoding()

#中国经济网
def loadLink(source_url):
    ua = UserAgent()
    headers = {
        #'User-Agent':ua.random,
        'Host': 'm.ce.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'wdcid=17845dda0f992773; _ga=GA1.3.1525765210.1543726895; wdses=7d7a7041a21fa181; __tasessionId=p0dafeh901543828064293; _gid=GA1.3.571101673.1543828065; wdlast=1543828625'
    }

    body = requests.get(source_url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.01)
    #print(body)

    soup = body.encode('raw_unicode_escape')
    soup = soup.decode()
    #print(soup)

    response = BeautifulSoup(soup,'lxml')
    time.sleep(0.01)
    #print(response)

    soup2 = response.find_all('article')
    soup2 = soup2[0]
    soup2 = str(soup2)
    soup2 = soup2[9:-10]
    soup2 = soup2.strip()
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
    print(body)

    response = BeautifulSoup(body, 'lxml')
    time.sleep(0.01)

    soup = response.find_all('article')
    #soup = response.find_all('figure')
    #return str(soup)

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
    #print(body)

    response = BeautifulSoup(body, 'lxml')
    time.sleep(0.01)

    soup = response.find_all('div',{'class':'a-con'})
    #print(soup)

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
    # print(body)

    soup = body.encode('raw_unicode_escape')
    soup = soup.decode()
    # print(soup)

    response = BeautifulSoup(soup, 'lxml')
    time.sleep(0.01)
    # print(response)

    soup2 = response.find_all('article')
    #print(soup2)

    try:
        soup2 = soup2[0]
    except:
        return '[]'
    soup2 = str(soup2)
    print(soup2)

    return soup2

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="Spider", user="root", password="123456", charset="utf8")
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