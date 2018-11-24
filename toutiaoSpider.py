# -*- coding:utf-8 -*-

import math
import hashlib
import requests
import urllib3
import time
import json
import re
from bs4 import BeautifulSoup
from pymysql import *
import html
from datetime import datetime

'''
今日头条号主主页历史文章内容抓取，抓取号主发布的所有内容、以及阅读数、评论数、推荐数、文章标签等信息
'''

def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = "479BB4B7254C150"
        CP = "7E0AC8874BB0985"
        return AS,CP
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS,CP

def loadPage1(user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'i.snssdk.com',
        'Referer': 'http://m.toutiao.com/profile/'+str(user_id)+'/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = 'http://i.snssdk.com/dongtai/list/v9/?user_id=' + str(user_id) + '&callback=jsonp1'
    try:
        body = requests.get(url,headers=headers,verify=False)
    except:
        pass
    urllib3.disable_warnings()
   
    try:
        loadPage2(user_id,mid)
    except:
        print('loadPage2 is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
        return

def loadPage2(user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'open.snssdk.com',
        'Referer': 'http://m.toutiao.com/profile/' + str(user_id) + '/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = 'http://open.snssdk.com/jssdk_signature/?appid=wxe8b89be1715734a6&noncestr=Wm3WZYTPz0wzccnW&timestamp=1525658149265&url=http%3A%2F%2Fm.toutiao.com%2Fprofile%2F' + str(user_id) + '%2F%23mid%3D' + str(mid) + '&callback=jsonp2'
    try:
        body = requests.get(url, headers=headers, verify=False)
    except:
        pass
    urllib3.disable_warnings()

    try:
        loadPage3(user_id,mid)
    except:
        print('loadPage3 is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
       
        return

def loadPage3(user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'i.snssdk.com',
        'Referer': 'http://m.toutiao.com/profile/' + str(user_id) + '/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = 'http://i.snssdk.com/dongtai/list/v9/?user_id=' + str(user_id) + '&max_cursor=1524477477396&callback=jsonp3'
    try:
        body = requests.get(url, headers=headers, verify=False)
    except:
        pass
    
    urllib3.disable_warnings()
    time.sleep(0.1)

    try:
        loadPage4(user_id,mid)
    except:
        print('loadPage4 is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
  
        return

def loadPage4(user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'www.toutiao.com',
        'Referer': 'http://m.toutiao.com/profile/' + str(user_id) + '/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'tt_webid=6549097213473031687; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16306fba12766c-0947bc1e837c5b-3c3c5b0b-1fa400-16306fba1286e0; tt_webid=6549097213473031687; uuid="w:7172e1edd4994c0c93ac5c79225526da"; _ga=GA1.2.258617572.1525330898; sso_login_status=0; __tasessionId=1xz7yw0za1525509676981; CNZZDATA1259612802=1617668685-1524827486-https%253A%252F%252Fwww.google.com.sg%252F%7C1525509300'
    }

    ascp = getASCP()
    url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=&uid=' + str(user_id) + '&media_id=' + str(mid) + '&output=json&is_json=1&count=20&from=user_profile_app&version=2&as=' + ascp[0] + '&cp=' + ascp[1] + '5AEF4BD2B2F4FE1&callback=jsonp4'
    try:
        body = requests.get(url, headers=headers, verify=False)
        urllib3.disable_warnings()
        body = str(body.text)
        body = body[7:-1]
        time.sleep(2.8)
        soup = json.loads(body)
        data = soup['data']
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time)+'\n')
            e.write(url + '\n')
        
        return

    for i in range(20):
        time.sleep(0.1)
        try:
            data2 = data[i]
        except:
            time.sleep(0.1)
            return
        try:
            # 文章链接
            source_url = data2['source_url']
            source_url = str(source_url)
            print(source_url)
            # 文章标题
            title = data2['title']
            title = str(title)
            print(title)
            # 文章作者
            author = data2['detail_source']
            author = str(author)
            print(author)
        except:
            error_time = int(time.time())
            with open('error_url.txt', 'a') as e:
                e.write(user_id + '\n')
                e.write(str(i) + '\n')
                e.write(str(error_time) + '\n')
                e.write(url + '\n')
            return
        try:
            # 文章发布时间
            date_time = data2['datetime']
            date_time = str(date_time)
            date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            print(date_time)
        except:
            date_time = '[]'
        try:
            #文章分类
            category = data2['tag']
            category = str(category)
            print(category)
        except:
            category = '[]'
        #文章内容
        has_video = data2['has_video']
        has_gallery = data2['has_gallery']
        if has_video == True:
            article_content = '["视频"]'
        else:
            if has_gallery == True:
                article_content = '["图集"]'
            else:
                article_content = '[]'
        try:
            # 关键词
            keywords = data2['keywords']
            keywords = str(keywords)
            if keywords != '':
                keywords = keywords.split(',')
            else:
                keywords = '[]'
            keywords = str(keywords)
            print(keywords)
        except:
            keywords = '[]'
            pass
        try:
            # 标签
            label = data2['label']
            label = str(label)
            print(label)
        except:
            label = '[]'
            pass
        try:
            #总阅读数
            total_read_count = data2['total_read_count']
            total_read_count = int(total_read_count)
            print(total_read_count)
        except:
            try:
                total_read_count = data2['go_detail_count']
                total_read_count = int(total_read_count)
                print(total_read_count)
            except:
                total_read_count = 0
            pass
        try:
            #应用外阅读数
            external_visit_count = data2['external_visit_count']
            external_visit_count = int(external_visit_count)
            print(external_visit_count)
        except:
            external_visit_count = 0
            pass
        try:
            # 应用内阅读数
            internal_visit_count = data2['internal_visit_count']
            internal_visit_count = int(internal_visit_count)
            print(internal_visit_count)
        except:
            try:
                internal_visit_count = int(total_read_count)-int(external_visit_count)
                print(internal_visit_count)
            except:
                internal_visit_count = 0
            pass
        try:
            #评论数
            comment_count = data2['comment_count']
            comment_count = int(comment_count)
            print(comment_count)
        except:
            comment_count = 0
            pass
        try:
            #转发数
            share_count = data2['share_count']
            share_count = int(share_count)
            print(share_count)
        except:
            share_count = 0
            pass
        try:
            #推荐数
            impression_count = data2['impression_count']
            impression_count = int(impression_count)
            print(impression_count)
        except:
            impression_count = 0
            pass

        time_stamp = datetime.timestamp(date_time)
        time_stamp = int(time_stamp)
        t = 1483200000
        if time_stamp < t:
            return
        else:
            pass

        items = {
            'source_url':source_url,
            'category':category,
            'title':title,
            'author':author,
            'datetime':date_time,
            'keywords':keywords,
            'label':label,
            'total_read_count':total_read_count,
            'internal_visit_count':internal_visit_count,
            'external_visit_count':external_visit_count,
            'comment_count':comment_count,
            'article_content':article_content,
            'share_count':share_count,
            'impression_count':impression_count
        }

        sql = """insert into toutiaoPage(source_url,category,title,author,datetime,keywords,label,total_read_count,internal_visit_count,external_visit_count,comment_count,share_count,impression_count,article_content) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor.execute(sql, (
            items["source_url"], items['category'],items["title"], items["author"], items["datetime"], items["keywords"],items["label"], items["total_read_count"], items["internal_visit_count"], items["external_visit_count"],items["comment_count"],items['share_count'],items['impression_count'],items["article_content"]))
            db.commit()
            print(items["source_url"] + " is success")
        except:
            db.rollback()

    has_more = soup['has_more']
    if has_more == 1:
        pass
    else:
        return

    try:
        behot = soup['next']
        print(behot)
        max_behot_time = behot['max_behot_time']
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        behot_time = 'behot_time is error'
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
            e.write(behot_time + '\n')
        return

    time.sleep(0.1)
    try:
        loadPage5(max_behot_time,user_id,mid)
    except:
        print('loadPage5 is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(str(max_behot_time) + '\n')
            e.write(url + '\n')
        return

def loadPage5(max_behot_time,user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'www.toutiao.com',
        'Referer': 'http://m.toutiao.com/profile/' + str(user_id) + '/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'tt_webid=6549097213473031687; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16306fba12766c-0947bc1e837c5b-3c3c5b0b-1fa400-16306fba1286e0; tt_webid=6549097213473031687; uuid="w:7172e1edd4994c0c93ac5c79225526da"; _ga=GA1.2.258617572.1525330898; sso_login_status=0; __tasessionId=1xz7yw0za1525509676981; CNZZDATA1259612802=1617668685-1524827486-https%253A%252F%252Fwww.google.com.sg%252F%7C1525509300'
    }

    ascp = getASCP()
    url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=' + str(max_behot_time) + '&uid=' + str(user_id) + '&media_id=' + str(mid) + '&output=json&is_json=1&count=20&from=user_profile_app&version=2&as=' + \
          ascp[0] + '&cp=' + ascp[1] + '5AEF4BD2B2F4FE1&callback=jsonp5'
    try:
        body = requests.get(url, headers=headers, verify=False)
        urllib3.disable_warnings()
        body = str(body.text)
        body = body[7:-1]
        time.sleep(0.2)
        soup = json.loads(body)
        data = soup['data']
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
       
        return

    for i in range(10):
        time.sleep(0.2)
        try:
            data2 = data[i]
        except:
            time.sleep(10)
            return
        try:
            # 文章链接
            source_url = data2['source_url']
            source_url = str(source_url)
            print(source_url)
            # 文章标题
            title = data2['title']
            title = str(title)
            print(title)
            # 文章作者
            author = data2['detail_source']
            author = str(author)
            print(author)
        except:
            error_time = int(time.time())
            with open('error_url.txt', 'a') as e:
                e.write(user_id + '\n')
                e.write(str(i) + '\n')
                e.write(str(error_time) + '\n')
                e.write(url + '\n')
            return
        try:
            # 文章发布时间
            date_time = data2['datetime']
            date_time = str(date_time)
            date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            print(date_time)
        except:
            date_time = '[]'
        try:
            # 文章分类
            category = data2['tag']
            category = str(category)
            print(category)
        except:
            category = '[]'
        # 文章内容
        has_video = data2['has_video']
        has_gallery = data2['has_gallery']
        if has_video == True:
            article_content = '["视频"]'
        else:
            if has_gallery == True:
                article_content = '["图集"]'
            else:
                article_content = '[]'
        try:
            # 关键词
            keywords = data2['keywords']
            keywords = str(keywords)
            if keywords != '':
                keywords = keywords.split(',')
            else:
                keywords = '[]'
            keywords = str(keywords)
            print(keywords)
        except:
            keywords = '[]'
            pass
        try:
            # 标签
            label = data2['label']
            label = str(label)
            print(label)
        except:
            label = '[]'
            pass
        try:
            # 总阅读数
            total_read_count = data2['total_read_count']
            total_read_count = int(total_read_count)
            print(total_read_count)
        except:
            try:
                total_read_count = data2['go_detail_count']
                total_read_count = int(total_read_count)
                print(total_read_count)
            except:
                total_read_count = 0
            pass
        try:
            # 应用外阅读数
            external_visit_count = data2['external_visit_count']
            external_visit_count = int(external_visit_count)
            print(external_visit_count)
        except:
            external_visit_count = 0
            pass
        try:
            # 应用内阅读数
            internal_visit_count = data2['internal_visit_count']
            internal_visit_count = int(internal_visit_count)
            print(internal_visit_count)
        except:
            try:
                internal_visit_count = int(total_read_count) - int(external_visit_count)
                print(internal_visit_count)
            except:
                internal_visit_count = 0
            pass
        try:
            # 评论数
            comment_count = data2['comment_count']
            comment_count = int(comment_count)
            print(comment_count)
        except:
            comment_count = 0
            pass
        try:
            # 转发数
            share_count = data2['share_count']
            share_count = int(share_count)
            print(share_count)
        except:
            share_count = 0
            pass
        try:
            # 推荐数
            impression_count = data2['impression_count']
            impression_count = int(impression_count)
            print(impression_count)
        except:
            impression_count = 0
            pass

        time_stamp = datetime.timestamp(date_time)
        time_stamp = int(time_stamp)
        t = 1483200000
        if time_stamp < t:
            return
        else:
            pass

        items = {
            'source_url': source_url,
            'category': category,
            'title': title,
            'author': author,
            'datetime': date_time,
            'keywords': keywords,
            'label': label,
            'total_read_count': total_read_count,
            'internal_visit_count': internal_visit_count,
            'external_visit_count': external_visit_count,
            'comment_count': comment_count,
            'article_content': article_content,
            'share_count': share_count,
            'impression_count': impression_count
        }

        sql = """insert into toutiaoPage(source_url,category,title,author,datetime,keywords,label,total_read_count,internal_visit_count,external_visit_count,comment_count,share_count,impression_count,article_content) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor.execute(sql, (
                items["source_url"], items['category'], items["title"], items["author"], items["datetime"],
                items["keywords"], items["label"], items["total_read_count"], items["internal_visit_count"],
                items["external_visit_count"], items["comment_count"], items['share_count'], items['impression_count'],
                items["article_content"]))
            db.commit()
            print(items["source_url"] + " is success")
        except:
            db.rollback()

    has_more = soup['has_more']
    if has_more == 1:
        pass
    else:
        return

    try:
        behot = soup['next']
        print(behot)
        max_behot_time = behot['max_behot_time']
        print(max_behot_time)
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        behot_time = 'behot_time is error'
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
            e.write(behot_time + '\n')
        return

    i = 6
    try:
        time.sleep(0.1)
        loadPage(max_behot_time,i,user_id,mid)
    except:
        print('loadPage is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(str(max_behot_time) + '\n')
            e.write(url + '\n')
        return

def loadPage(max_behot_time,i,user_id,mid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'www.toutiao.com',
        'Referer': 'http://m.toutiao.com/profile/' + str(user_id) + '/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'tt_webid=6549097213473031687; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16306fba12766c-0947bc1e837c5b-3c3c5b0b-1fa400-16306fba1286e0; tt_webid=6549097213473031687; uuid="w:7172e1edd4994c0c93ac5c79225526da"; _ga=GA1.2.258617572.1525330898; sso_login_status=0; __tasessionId=1xz7yw0za1525509676981; CNZZDATA1259612802=1617668685-1524827486-https%253A%252F%252Fwww.google.com.sg%252F%7C1525509300'
    }

    ascp = getASCP()
    url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=' + str(
        max_behot_time) + '&uid=' + str(user_id) + '&media_id=' + str(mid) + '&output=json&is_json=1&count=10&from=user_profile_app&version=2&as=' + \
          ascp[0] + '&cp=' + ascp[1] + '5AEF4BD2B2F4FE1&callback=jsonp' + str(i)
    try:
        body = requests.get(url, headers=headers, verify=False)
        urllib3.disable_warnings()
        body = str(body.text)
        time.sleep(0.1)
        if i>=6 and i<=9:
            body = body[7:-1]
        else:
            body = body[8:-1]

        soup = json.loads(body)
        data = soup['data']
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
        return

    for i in range(10):
        time.sleep(0.1)
        try:
            data2 = data[i]
        except:
            return
        try:
            # 文章链接
            source_url = data2['source_url']
            source_url = str(source_url)
            print(source_url)
            # 文章标题
            title = data2['title']
            title = str(title)
            print(title)
            # 文章作者
            author = data2['detail_source']
            author = str(author)
            print(author)
        except:
            error_time = int(time.time())
            with open('error_url.txt', 'a') as e:
                e.write(user_id + '\n')
                e.write(str(i) + '\n')
                e.write(str(error_time) + '\n')
                e.write(url + '\n')
            return
        try:
            # 文章发布时间
            date_time = data2['datetime']
            date_time = str(date_time)
            date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            print(date_time)
        except:
            date_time = '[]'
        try:
            # 文章分类
            category = data2['tag']
            category = str(category)
            print(category)
        except:
            category = '[]'
        # 文章内容
        has_video = data2['has_video']
        has_gallery = data2['has_gallery']
        if has_video == True:
            article_content = '["视频"]'
        else:
            if has_gallery == True:
                article_content = '["图集"]'
            else:
                article_content = '[]'
        try:
            # 关键词
            keywords = data2['keywords']
            keywords = str(keywords)
            if keywords != '':
                keywords = keywords.split(',')
            else:
                keywords = '[]'
            keywords = str(keywords)
            print(keywords)
        except:
            keywords = '[]'
            pass
        try:
            # 标签
            label = data2['label']
            label = str(label)
            print(label)
        except:
            label = '[]'
            pass
        try:
            # 总阅读数
            total_read_count = data2['total_read_count']
            total_read_count = int(total_read_count)
            print(total_read_count)
        except:
            try:
                total_read_count = data2['go_detail_count']
                total_read_count = int(total_read_count)
                print(total_read_count)
            except:
                total_read_count = 0
            pass
        try:
            # 应用外阅读数
            external_visit_count = data2['external_visit_count']
            external_visit_count = int(external_visit_count)
            print(external_visit_count)
        except:
            external_visit_count = 0
            pass
        try:
            # 应用内阅读数
            internal_visit_count = data2['internal_visit_count']
            internal_visit_count = int(internal_visit_count)
            print(internal_visit_count)
        except:
            try:
                internal_visit_count = int(total_read_count) - int(external_visit_count)
                print(internal_visit_count)
            except:
                internal_visit_count = 0
            pass
        try:
            # 评论数
            comment_count = data2['comment_count']
            comment_count = int(comment_count)
            print(comment_count)
        except:
            comment_count = 0
            pass
        try:
            # 转发数
            share_count = data2['share_count']
            share_count = int(share_count)
            print(share_count)
        except:
            share_count = 0
            pass
        try:
            # 推荐数
            impression_count = data2['impression_count']
            impression_count = int(impression_count)
            print(impression_count)
        except:
            impression_count = 0
            pass

        time_stamp = datetime.timestamp(date_time)
        time_stamp = int(time_stamp)
        t = 1483200000
        if time_stamp < t:
            return
        else:
            pass

        items = {
            'source_url': source_url,
            'category': category,
            'title': title,
            'author': author,
            'datetime': date_time,
            'keywords': keywords,
            'label': label,
            'total_read_count': total_read_count,
            'internal_visit_count': internal_visit_count,
            'external_visit_count': external_visit_count,
            'comment_count': comment_count,
            'article_content': article_content,
            'share_count': share_count,
            'impression_count': impression_count
        }

        sql = """insert into toutiaoPage(source_url,category,title,author,datetime,keywords,label,total_read_count,internal_visit_count,external_visit_count,comment_count,share_count,impression_count,article_content) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor.execute(sql, (
                items["source_url"], items['category'], items["title"], items["author"], items["datetime"],
                items["keywords"], items["label"], items["total_read_count"], items["internal_visit_count"],
                items["external_visit_count"], items["comment_count"], items['share_count'], items['impression_count'],
                items["article_content"]))
            db.commit()
            print(items["source_url"] + " is success")
        except:
            db.rollback()

    try:
        behot = soup['next']
        max_behot_time = behot['max_behot_time']
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        behot_time = 'behot_time is error'
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
            e.write(behot_time + '\n')
        return

    try:
        has_more = soup['has_more']
        if has_more == 1:
            i += 1
            if i >= 10:
                i = 10
            else:
                time.sleep(0.2)
            try:
                time.sleep(0.2)
                loadPage(max_behot_time,i,user_id,mid)
            except:
                print('loadPage is wrong!!!')
                error_time = int(time.time())
                with open('error_url.txt', 'a') as e:
                    e.write(user_id + '\n')
                    e.write(str(error_time) + '\n')
                    e.write(str(i) + '\n')
                    e.write(str(max_behot_time) + '\n')
                return
        else:
            return
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        has_more = 'has_more is error'
        with open('error_url.txt', 'a') as e:
            e.write(user_id + '\n')
            e.write(str(error_time) + '\n')
            e.write(url + '\n')
            e.write(has_more + '\n')
        return

def loadLink(source_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Host': 'www.toutiao.com',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept - Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'tt_webid=6549097213473031687; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16306fba12766c-0947bc1e837c5b-3c3c5b0b-1fa400-16306fba1286e0; tt_webid=6549097213473031687; uuid="w:7172e1edd4994c0c93ac5c79225526da"; _ga=GA1.2.258617572.1525330898; sso_login_status=0; __tasessionId=1xz7yw0za1525509676981; CNZZDATA1259612802=1617668685-1524827486-https%253A%252F%252Fwww.google.com.sg%252F%7C1525509300'
    }
    try:
        body = requests.get(source_url, headers=headers, timeout=5, verify=False).text
        urllib3.disable_warnings()
    except:
        print('something is wrong!!!')
        error_time = int(time.time())
        with open('error_url.txt', 'a') as e:
            e.write(str(error_time) + '\n')
            e.write(source_url + '\n')
        return

    response = BeautifulSoup(body,'lxml')

    try:
        content = response.find_all('script')
    except:
        return '[]'

    if len(content) > 6:
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
                text = str(text)
                return text
            else:
                return '[]'

        else:
            return '[]'
    else:
        return '[]'

if __name__ == "__main__":
    db = connect(host="secret", port=3306, db="Spider", user="root", passwd="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = 'SELECT userId,mid FROM User'
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        user_id = data[i][0]
        mid = data[i][1]
        loadPage1(user_id, mid)
        time.sleep(0.1)

    db.close()
