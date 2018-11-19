# -*- coding:utf-8 -*-

from pymysql import *
import re

'''
对之前已经获取的URL，分别提取其userID及其对应的mid,存入MySQL
'''

def user_ID():
    db = connect(host="secret", port=3306, db="Spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = 'SELECT MainUrl FROM Media'
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
    for i in range(len(data)):
        url = data[i][0]
        pattern = re.compile(r'\d+')
        id = re.findall(pattern,url)
        if len(id) == 2:
            user_id = id[0]
            mid = id[1]
        else:
            user_id = ''
            mid = ''
        print(user_id)
        print(mid)
        n = i+1
        user_id = str(user_id)
        mid = str(mid)
        n = str(n)
        Update_user(user_id,mid,n)

    db.close()

def Update_user(user_id,mid,n):
    params = [user_id,mid,n]
    db = connect(host="secret", port=3306, db="Spider", user="root", password="secret", charset="utf8")
    conn = db.cursor()

    try:
        sql = """update Media set userId=%s,mid =%s WHERE iid=%s"""
        user_mid = conn.execute(sql,params)
        db.commit()
    except:
        db.rollback()
    db.close()

if __name__ == "__main__":
    user_ID()
