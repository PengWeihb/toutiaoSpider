# -*- coding:utf-8 -*-

import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from MySQLdb import *

'''
使用selenium + PhantomJS的方式，模拟点击不断获取今日头条号主信息
此方法主要抓取头条主页活跃的号主，可以分类地进行抓取
'''

def user_rearch(style,user_list_1):
    url = 'https://www.toutiao.com/ch/' + style + '/'
    print(url)
    print type(user_list_1)

    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    driver.implicitly_wait(1)

    for i in range(200000):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        response = soup.find_all('a',{'class':'lbtn source'})

        for links in response:
            print links
            links = str(links)
            pattern = re.compile(r'\d+')
            body = re.findall(pattern,links)

            if len(body) != 0:
                data = body[0]
                data = str(data)
                data.strip()
                user_list2 = user_list_1
                print len(user_list2)

                user_list2.append(data)
                print len(user_list2)
                time.sleep(0.5)

                new_user_list = list(set(user_list2))
                new_user_list.sort(key = user_list2.index)
                print len(new_user_list)

                if len(new_user_list) == len(user_list_1):
                    print 'good!'
                    userId = new_user_list[-1]
                    userId = str(userId)
                    MainUrl = 'https://www.toutiao.com/c/user/'+ str(userId) + '/'
                    mid = 'None'
                    sql = """insert into Media(MainUrl,userId,mid) value(%s,%s,%s)"""
                    try:
                        conn.execute(sql,(MainUrl,userId,mid))
                        db.commit()
                    except:
                        db.rollback()
                else:
                    pass

                user_list_1 = new_user_list
            else:
                pass

        print str(i)+' is ok'
        time.sleep(1)
        if i%100 == 0:
            time.sleep(1800)
        else:
            pass
        driver.refresh()
        user_list_1 = new_user_list


if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="Spider", user="root", passwd="123456", charset="utf8")
    conn = db.cursor()
    try:
        sql = 'SELECT userId FROM Media'
        MainUrl = conn.execute(sql)
        data = conn.fetchall()
        db.commit()
    except:
        db.rollback()
    user_list = []
    for i in range(len(data)):
        user_id = data[i][0]
        user_id = str(user_id)
        user_list.append(user_id)
    print user_list

    user_set = set(user_list)
    user_list_1 = list(user_set)
    user_list_1.sort(key = user_list.index)
    print len(user_list_1)
    
    # news_game、news_hot、news_tech、news_entertainment、news_sports、news_car、news_finance、news_travel，and so on.
    style = 'news_game'
    user_rearch(style,user_list_1)
    db.close()
