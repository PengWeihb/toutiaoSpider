# -*- coding:utf-8 -*-

import requests
import urllib3
import time
from bs4 import BeautifulSoup
from pymysql import *
import html
import re
import math
import random
import re

def loadLink(source_url,userId):

    accept = 'https://www.toutiao.com/i' + userId + '/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331',
        #'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Host': 'www.toutiao.com',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': accept,
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        #'Cookie':'tt_webid=6558223951607875079; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16385a3fcb76d9-0a084656577c928-77256752-1fa400-16385a3fcb8440; CNZZDATA1259612802=560349922-1526952779-https%253A%252F%252Fwww.baidu.com%252F%7C1526958179; tt_webid=6558223951607875079; uuid="w:620c77872f314457ac7474a47bc06f4a"; __tasessionId=8chi0s5jf1526959969608'
        'Cookie': 'uuid="w:bfab8d0a69ca4e989faa722278b8c70f"; UM_distinctid=163252b864a2e1-0d3fc10de-554c162f-1fa400-163252b864b32f; _ga=GA1.2.627472936.1527212834; tt_webid=6549099449222137358; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=lbwjy1jvf1527578479037; tt_webid=6549099449222137358; CNZZDATA1259612802=207427604-1525336204-%7C1527578368'
    }

    #proxies = {"http": "http://60.186.255.172:1246"}
    try:
        body = requests.get(source_url,headers=headers,timeout=5,verify=False).text
        urllib3.disable_warnings()
        time.sleep(0.1)
        print(body)


    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url5.txt', 'a') as e:
            e.write(str(error_time) + '\n')
            e.write(source_url + '\n')
        print(url)
        return '[]'

    response = BeautifulSoup(body,'lxml')
    time.sleep(0.1)
    print(response)


    try:
        content = response.find_all('script')
    except:
        return '[]'

    if len(content) >= 6:
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
                #text = str(text)
                return text
            else:
                return str(content)

        else:
            return str(content)
    else:
        return '[]'

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="123456", charset="utf8")
    cursor = db.cursor()

    try:
        sql = 'SELECT source_url FROM toutiao10'
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
    for i in range(8375,len(data)):
        url = data[i][0]
        print(url)
        print(i)
        pattern = re.compile(r'\d+')
        user_id = re.findall(pattern,url)
        userId = user_id[0]
        print(userId)

        #time.sleep(0.5)
        page = loadLink(url,userId)
        n = i + 324001
        n = str(n)
        params = [page,n]
        try:
            sql = """update toutiao10 set article_content=%s WHERE id=%s"""
            cursor.execute(sql,params)
            db.commit()
        except:
            db.rollback()
        time.sleep(0.2)

    db.close()