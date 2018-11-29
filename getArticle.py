# -*- coding:utf-8 -*-

import hashlib
import math
import random
import json
import re
import time
from threading import Thread
from urllib.parse import urlencode
import requests
# from get_ascp import getASCP
from bs4 import BeautifulSoup
from pymysql import connect
from datetime import datetime
import sys  # 设置递归深度
sys.setrecursionlimit(100000)
import redis
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
import pymongo

class title(object):
    def __init__(self):
        self.mongoUri = 'mongodb://mongouser:password@ip/admin'
        self.client = pymongo.MongoClient(self.mongoUri)

        self.db = self.client.touTiao

        self.collection = self.db.toutiaoIncrement
        self.url = 'https://is.snssdk.com/pgc/ma/?article_limit_enable=1&max_behot_time={}&user_id={}&media_id={}&as={}&cp={}&current_user_id=0&from_page=detail_article&is_blocked=0&is_following=0&is_default_tab=1&current_type=all&version_code=6.8.0&page_type=1&count=20&output=json&is_json=1&from=user_profile_app&version=2'  # 5AEF4BD2B2F4FE1
        self.n = 0
        # 链接redis
        self.redis_cli = redis.Redis(host='secret', port=6480, db=1, password="password",decode_responses=True)
        self.start_time = int(time.time())
        self.end_time = 1537459200  # 9-20-0
        self.next_over_time = 0
        self.max_behot_time = 0
        self.count = 0

    def getASCP(self):
        t = int(math.floor(time.time()))
        e = hex(t).upper()[2:]
        m = hashlib.md5()
        m.update(str(t).encode(encoding='utf-8'))
        i = m.hexdigest().upper()

        if len(e) != 8:
            AS = "479BB4B7254C150"
            CP = "7E0AC8874BB0985"
            return AS, CP
        n = i[0:5]
        a = i[-5:]
        s = ''
        r = ''
        for o in range(5):
            s += n[o] + e[o]
            r += e[o + 3] + a[o]
        AS = 'A1' + s + e[-3:]
        CP = e[0:3] + r + 'E1'
        return AS, CP

    def get_response(self, uid, mid, max_behot_time):
        AS, CP = self.getASCP()
        uid = int(uid)
        media_dia = int(mid)
        data = {
            'max_behot_time': max_behot_time,
            'media_id': mid,
            'uid': uid,
            'page_type': '1',
            'count': '20',
            'version': '2',
            # 'callback': 'jsonp3',
            'output': 'json',
            'is_json': '1',
            'from': 'user_profile_app',
            'as': AS,
            'cp': CP,
        }
        #本次更新数据的时间戳，也就是下次更新停止的时间戳。
        self.next_over_time = max_behot_time

        # headers = random.choice(header)  #随机一个请头

        headers = {
            'authority': 'www.toutiao.com',
            'method': 'GET',
            'path': '/pgc/ma/?page_type=1&max_behot_time={}&uid={}&media_id={}&output=json&is_json=1&count=20&from=user_profile_app&version=2&as={}&cp={}&callback=jsonp3'.format(max_behot_time, uid, mid, AS, CP),
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=164f2e4566c8ed-0693c7885b105c-54103515-1fa400-164f2e4566d748; csrftoken=6d0fdf3691ff6e4ac1575d100ac867a3; uuid="w:29a5d9e754344060a20a90082ceb4599"; login_flag=d461fb3548072626676113b9bbf54942; sessionid=8eb83236138f04903d93d277c1a02e99; sid_tt=8eb83236138f04903d93d277c1a02e99; tt_webid=75434708680; tt_webid=75434708680; uid_tt=ff2345fc8b853b31a0a4080dc2b95d6e; sso_login_status=1; sid_guard="8eb83236138f04903d93d277c1a02e99|1533096712|15552000|Mon\054 28-Jan-2019 04:11:52 GMT"; __utma=24953151.1361631348.1533097169.1533097169.1533097169.1; __utmc=24953151; __utmz=24953151.1533097169.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ba=BA0.2-20180801-51234-IzEK6feRUqnELW5bhqGi; __tasessionId=tmav31gev1533109967006; cp={}; CNZZDATA1259612802=481932984-1533078471-https%253A%252F%252Fwww.baidu.com%252F%7C1533105485'.format(CP),
            'referer': 'https://m.toutiao.com/profile/{}/'.format(uid),
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36',
            # 'user-agent': self.UserAgent.random,
        }
        # start_urls = self.url.format(max_behot_time, uid, media_dia, AS, CP)#拼接地址
        start_urls = 'https://www.toutiao.com/pgc/ma/?' + urlencode(data)
        print('请求地址：', start_urls)

        ip = self.redis_cli.srandmember('IP')#代理池获取ip
        print('请求IP:', ip)
        proxies = {
            "https": "https://{}".format(ip),
        }
        time.sleep(random.randint(1, 2) / 4)
        try:
            res = requests.get(start_urls, headers=headers, proxies=proxies, timeout=3, verify=False)
            rjson = res.json()['data']
            self.parse(rjson, uid, mid)
        except Exception as e:
            if self.count<2:
                self.count += 1
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',e)
                self.redis_cli.srem("IP", ip)
                self.get_response(uid=uid, mid=media_dia,max_behot_time=max_behot_time)
            else:
                return

    def parse(self,data,uid,mid):
        now1 = 0

        for data2 in data:
            title = data2['title']
            url = data2['source_url']
            create = data2['datetime']
            author = data2['source']
            # 关键字
            try:
                keywords = data2['keywords']
            except:
                keywords = '[]'
            # 标签
            try:
                label = data2['label']
            except:
                label = '[]'
            # 分类
            try:
                category = data2['tag']
            except:
                category = '[]'
            # 站外阅读数
            try:
                external = data2['external_visit_count']
            except:
                external = 0
            # 站内阅读数
            try:
                internal = data2['internal_visit_count']
            except:
                internal = 0
            # 总阅读数
            try:
                totalRead = data2['total_read_count']
            except:
                totalRead = external + internal
            # 判断阅读数
            if external == 0:
                external = int(totalRead) - int(internal)

            if internal == 0:
                internal = int(totalRead) - int(external)
            # 评论数
            try:
                comment = data2['comment_count']
            except:
                comment = 0
            # 分享数
            try:
                share_count = data2['share_count']
            except:
                share_count = 0
            # 推荐数
            try:
                impression = data2['impression_count']
            except:
                impression = 0
            # 长尾词
            try:
                optional_data = data2['optional_data']['label3']
            except:
                optional_data = '[]'
            print('标题：', title)
            print('文章路径：', url)
            print('作者：', author)
            print('类别：', category)
            print('发布时间：', create)
            print('关键词：', keywords)
            print('标签：', label)
            print('长尾词：', optional_data)
            print('总阅读数：', totalRead)
            print('站外阅读：', external)
            print('站内阅读：', internal)
            print('评论数：', comment)
            print('分享数：', share_count)
            print('推荐量：', impression)
            pattern = re.compile(r'\d+')
            articleID = re.findall(pattern, url)[0]
            try:
                if data2['has_video']:
                    content = '["视频"]'

                elif data2['has_gallery']:
                    content = '["图集"]'

                else:
                    content = self.get_content(articleID)

            except:
                content = self.get_content(articleID)
                print(66666666)

            now = int(time.time())
            item = {
                "source_url": url,  # 建一个索引
                "media_id":mid,
                "user_id":uid,
                "category":category,
                "title": title,
                "author": author,
                "datetime":create,
                "keywords": keywords,
                "label": label,
                "total_read_count": totalRead,
                "internal_visit_count": internal,
                "external_visit_count": external,
                "comment_count": comment,
                "share_count": share_count,
                "impression_count": impression,
                "update_time":[now],
                "read_collection": [totalRead],          #阅读数集合更新时间戳
                "comment_collection":[comment],        #评论数集合更新时间戳
                "impression_collection":[impression],     #推荐数集合更新时间戳
                "article_content": content,
                "save_time": now,  # 存储时间在7天以内
                "is_cluster": "false",  # 是否导入集群
                "platfrom": "头条号",
            }
            rsp = 0
            for i in self.collection.find({"source_url":url}):
                rsp = i['source_url']
                print("------》》》》》》",rsp)
            if rsp:
                print(11111111)
                self.collection.update({"source_url":url},{"$push":{"update_time":now,"read_collection":totalRead,"comment_collection":comment,"impression_collection":impression}})
            else:
                print("你好——————")
                self.collection.insert(item)
            now1 = data2['behot_time']
            print(now1)
            if self.end_time==0:
                end_time = 1537520400
            else:
                end_time = self.end_time
            if int(now1) < end_time:  # 指定时间戳
                return
        else:
            self.start_request(uid, mid, now1)

    def get_content(self,articleID):
        print(articleID)
        url = "http://a6.pstatp.com/article/content/lite/14/1/{}/{}/1/".format(articleID, articleID)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        try:
            response = requests.get(url=url, headers=headers)
            con = response.json()["data"]["content"]
            if con == '该内容已删除':
                content = con
            else:
                r = re.sub(r'zip_src_path=".*?"', '', con)
                soup = BeautifulSoup(r, 'lxml')
                content = str(soup.select("article")[0])
        except:
            content = '[]'
        print(content,'\n')
        return content

    def run(self):
        while True:
            self.count = 0
            #获取当前时间戳
            now = int(time.time())
            # self.get_response(93763762777,1593464132882440,now)

            data = self.redis_cli.rpop('TouTiao')

            print(type(data), data)
            data = eval(data)
            uid = data['uid']
            mid = data['mid']
            # 本次访问的断点
            self.end_time =data['next_time']
            try:
                self.get_response(uid,mid,now)
                data1 = {}
                data1['next_time'] = now
                data1['uid'] = uid
                data1['mid'] = mid
                self.redis_cli.lpush('TouTiao',data1)
            except:
                continue

if __name__=="__main__":
    for i in range(5):
        c = title()
        work_thead2 = Thread(target=c.run)
        work_thead2.start()
