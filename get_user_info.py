# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from pymysql import *
import time

def get_content(openid):
    ua = UserAgent()
    url = 'http://m.toutiao.com/profile/' + str(openid) + '/'
    headers = {
        'User-Agent': ua.random,
        #'cookie': 'tt_webid=6633177721172510211; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16795d64deb4d2-06cf1e2bb36f16-3a3a5d0c-1fa400-16795d64dec651; tt_webid=6633177721172510211; csrftoken=e4399435db5073524703dd9ea9fdea4e; uuid="w:e8e0021456144b609cbcbccb9790fe68"; CNZZDATA1259612802=2038699008-1544404633-https%253A%252F%252Fwww.baidu.com%252F%7C1544410033; __tasessionId=1esoq5zf71544425484956'
    }

    body = requests.get(url,headers=headers).text
    time.sleep(0.1)
    response = BeautifulSoup(body,'lxml')

    try:
        soup = response.find_all('p',{'id':'description'})[0]
        soup2 = BeautifulSoup(str(soup), 'lxml')
        desc = soup2.get_text()
        print(desc)
    except:
        desc = '[]'
    time.sleep(0.1)

    return desc

if __name__ == '__main__':
    db = connect(host='localhost', port=3306, db='spider', user='root', password='secret',charset='utf8')
    cursor = db.cursor()
    try:
        sql = """select id,openid,flag,`describe` from jjb_media"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        flag = data[i][2]
        desc = data[i][3]
        if flag == '今日头条' and desc == '[]':
            print(id)
            #uid = data[i][1]
            #con = get_content(uid)
            con = ''
            param = [con, id]
            try:
                sql = """update jjb_media set `describe` = %s where id = %s"""
                cursor.execute(sql, param)
                db.commit()
                print('ok!!!!!')
            except:
                db.rollback()
        else:
            pass

    db.close()
