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
        'User-Agent': ua.random
    }

    body = requests.get(url,headers=headers).text
    response = BeautifulSoup(body,'lxml')

    soup = response.find_all('button',{'class':'more'})
    try:
        soup = soup[0]
    except:
        soup = 0
    soup = str(soup)

    pattern = re.compile('\d+')
    soup2 = re.findall(pattern,soup)
    mid = soup2[0]

    return mid

def conn_sql():
     try:
        sql = """select id,openid,toutiao_mid from jjb_media"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

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

if __name__ == '__main__':
    db = connect(host='localhost',port=3306,db='spider',user='root',password='scret',charset='utf8')
    cursor = db.cursor()

    conn_sql()
    
    db.close()
