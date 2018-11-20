# -*- coding:utf-8 -*-

from MySQLdb import *
import time
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

def loadLink(url):

    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(0.5)
    driver.refresh()
    driver.implicitly_wait(0.5)

    response = BeautifulSoup(driver.page_source, 'lxml')

    try:
        content = response.find_all('script')
    except:
        return '[]'

    if len(content) >= 6:
        time.sleep(0.02)
        content = content[6]
        content = str(content)
        content = content[28:-12]
        content = content.strip()
        content = content.split('},')
        if len(content) > 2:
            content = content[2]
            content = content.strip()
            content = content.split('content:')
            if len(content) >= 2:
                content = content[1]
                content = content.split('groupId:')
                content = content[0].strip()
                content = content[:-1]
                text = content.replace('div&gt;&lt;', '').replace('&lt;/div&gt;', '')
                #text = HTMLParser.unescape(text)
                return text
            else:
                return str(content)

        else:
            return str(content)
    else:
        return '[]'

if __name__ == "__main__":
    db = connect(host="secret", port=3306, db="Spider", user="root", passwd="secret", charset="utf8")
    conn = db.cursor()

    try:
        sql = 'SELECT source_url FROM Article'
        MainUrl = conn.execute(sql)
        data = conn.fetchall()
        db.commit()
    except:
        db.rollback()
        
    for i in range(2259,len(data)):
        url = data[i][0]
        print(url)
        print(i)

        time.sleep(0.5)
        page = loadLink(url)
        n = i + 1
        n = str(n)
        params = [page,n]
        try:
            sql = """update Article set article_content=%s WHERE id=%s"""
            conn.execute(sql,params)
            db.commit()
        except:
            db.rollback()
        time.sleep(0.5)

    db.close()
