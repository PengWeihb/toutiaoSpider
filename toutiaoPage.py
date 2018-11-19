# -*- coding:utf-8 -*-

import urllib3
import time
from bs4 import BeautifulSoup
from pymysql import *
import html
from urllib import request
import re

'''
此代码主要是根据已经爬下来的列表详情页，依据文章的URL抓取文章的内容
'''

def loadLink(source_url,userId):
    proxies = {}
    try:
        proxy_handler = request.ProxyHandler(proxies)
        opener = request.build_opener(proxy_handler)
        accept = 'https://www.toutiao.com/i' + userId + '/'
        opener.addheaders = [
            ('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'),
            #('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7'),
            ('Cookie', 'tt_webid=6549097213473031687'),
            ('Referer', accept),
            ('Host', 'm.toutiao.com')
        ]

        request.install_opener(opener)
        soup = request.urlopen(source_url,timeout=5)
        body = soup.read().decode('utf-8')
        time.sleep(0.1)
        print(body)
        urllib3.disable_warnings()
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(str(error_time) + '\n')
            e.write(source_url + '\n')
        print(source_url)
        return '[]'

    response = BeautifulSoup(body,'lxml')
    time.sleep(0.1)
    print(response)

    try:
        content = response.find_all('script')
    except:
        return '[]'

    if len(content) > 6:
        time.sleep(0.1)
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
                text = content.replace('div&gt;&lt;','').replace('&lt;/div&gt;','')
                text = html.unescape(text)
                return text
            else:
                return '[]'

        else:
            return '[]'
    else:
        return '[]'

if __name__ == "__main__":
    db = connect(host="secret", port=3306, db="Spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = '''SELECT id,source_url,article_content FROM toutiaoPage'''
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        print('ok')
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        url = data[i][1]
        content = data[i][2]
        pattern = re.compile(r'\d+')
        user_id = re.findall(pattern, url)
        userId = user_id[0]
        print(userId)

        '''
        if content == '["视频"]':
            pass
        elif content == '["图集"]':
            pass
        else:
        '''
        if content == '[]':
            time.sleep(0.1)
            page = loadLink(url,userId)
            n = id
            n = str(n)
            params = [page,n]
            try:
                sql = """update toutiaoPage set article_content=%s where id=%s"""
                cursor.execute(sql,params)
                db.commit()
            except:
                db.rollback()
            time.sleep(0.2)

    db.close()
