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

    soup = response.find_all('button',{'class':'more'})
    time.sleep(0.1)
    try:
        soup = soup[0]
    except:
        soup = 0
    soup = str(soup)

    pattern = re.compile('\d+')
    soup2 = re.findall(pattern,soup)
    mid = soup2[0]
    print(mid)

    return mid

if __name__ == '__main__':
    db = connect(host='192.168.0.21',port=3306,db='db_juejinlian',user='user_juejinlian',password='ac21acWq18E2',charset='utf8')
    cursor = db.cursor()

    try:
        sql = """select id,openid,toutiao_mid from jjb_media"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()


        print(i)
        toutiao_mid = data[i][2]
        if toutiao_mid == '0':
            id = data[i][0]
            openid = data[i][1]
            mid = get_content(openid)
            mid = str(mid)
            time.sleep(0.2)
            param = [mid,id]
            try:
                sql = """update jjb_media set toutiao_mid = %s where id = %s"""
                cursor.execute(sql,param)
                db.commit()
                print('ok!!!!!')
            except:
                db.rollback()
        else:
            pass

    db.close()
