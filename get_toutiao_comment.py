# -*- coding:utf-8 -*-

import requests
import json
from urllib.parse import urlencode
import time
import sys
import redis
from threading import Thread
import hashlib
from fake_useragent import UserAgent
import random

#设置递归深度
sys.setrecursionlimit(100000)

class Comment(object):
    def __init__(self):
        self.offset = 0
        self.count = 2 #IP失效次数(）
        self.redis_cli = redis.Redis(host='127.0.0.1', port=6379, db=0, password='123456', charset='utf8', decode_responses=True)

    def get_comment(self, item_id, group_id, save_time):
        ua = UserAgent()
        ts = int(time.time())
        param_data = {
            'offset': self.offset,
            'group_id': group_id,
            'aggr_type': 1,
            'count': 50,
            'item_id': item_id,
            'ts': ts
        }
        comment_url = 'http://is-hl.snssdk.com/article/v4/tab_comments/?' + urlencode(param_data)
        headers = {
            'Host':'is-hl.snssdk.com',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-A8000 Build/MMB29M) NewsArticle/7.0.3 cronet/TTNetVersion:a729d5c3',
        }
        ip = self.redis_cli.srandmember('IP')
        print('请求IP:', ip)
        if ip == None:
            print('ip is None')
            time.sleep(10)
            ip = self.redis_cli.srandmember('IP')
        proxies = {
            "http": "http://{}".format(ip),
        }
        time.sleep(random.randint(1, 2) / 4)
        try:
            response = requests.get(comment_url, headers=headers, proxies=proxies, timeout=3)
            total_number = response.json()['total_number']
            data = response.json()['data']
            time.sleep(random.randint(1, 2) / 32)
            print('data: ', data)
            if data == []:
                now = int(time.time())
                space_time = now - save_time
                if space_time < 43200: #12小时的时间戳
                    item = {'item_id':item_id,'group_id':group_id,'save_time':save_time}
                    self.redis_cli.sadd('spider_toutiao_comment_id',str(item))
                    print('insert item success！！！')
                return
            self.parse_comment(data,item_id,group_id,total_number)
        except:
            try:
                now = int(time.time())
                space_time = now - save_time
                if space_time < 43200:  # 12小时的时间戳
                    item = {'item_id': item_id, 'group_id': group_id, 'save_time': save_time}
                    self.redis_cli.sadd('spider_toutiao_comment_id', str(item))
                    print('insert item success！！！')
            except Exception as e:
                print('insert item wrong', e)
            print('something is wrong!!!')
            self.redis_cli.srem("IP", ip)

    def parse_comment(self,comments,item_id,group_id,total_number):
        for comment in comments:
            # 当前请求Unix时间戳
            mt = int(time.time())
            # API签名字符串
            para = 'b#28ac3c1abc' + 'juejinchain.com' + str(mt)
            sign = hashlib.md5(para.encode(encoding='UTF-8')).hexdigest()
            #文章url
            url = 'http://toutiao.com/item/' + str(item_id)
            #回复唯一标识ID
            id = comment['comment']['id']
            #评论用户名称
            user_name = comment['comment']['user_name']
            #评论用户头像链接
            user_img_url = comment['comment']['user_profile_image_url']
            #评论内容text
            text = comment['comment']['text']
            #评论时间
            create_time = comment['comment']['create_time']
            #评论内容点赞数
            digg_count = comment['comment']['digg_count']
            #评论回复数
            reply_count = comment['comment']['reply_count']

            print('text: ', text)
            print('total_number: ', total_number)

            #获取回复comment
            reply_list = []
            if reply_count > 0:
                offset_reply = 0
                self.get_reply_comment(id, reply_list, offset_reply)

            items = {
                'mt': mt,
                'sign': sign,
                'arc_url': url,
                'nickname': user_name,
                'avatar': user_img_url,
                'content': text,
                'reply': reply_count,
                'fabulous': digg_count,
                'comment_time': create_time,
                'reply_list': json.dumps(reply_list),
            }

            # 文章评论信息存储
            try:
                url = 'http://dev.api.juejinchain.cn/index/spider/toutiao_comment'
                requests.post(url, data=items)
                jjb_url = 'http://api.juejinchain.com/index/spider/toutiao_comment'
                requests.post(jjb_url, data=items)
                print('ok!!!!')
            except Exception as e:
                print('insert db wrong!!!!', e)

        else:
            if total_number <= 50:
                return
            self.offset += 50
            if self.offset > 50:
                return
            base_time = 1544612400 #随便一个小于当前时间点一天的时间戳
            self.get_comment(item_id,group_id,base_time)

    def get_reply_comment(self, id, reply_list, offset_reply):
        param_data = {
            'id': id,
            'count': 50,
            'offset': offset_reply
        }
        ua = UserAgent()
        headers = {
            'Host': 'lf-hl.snssdk.com',
            'User-Agent': ua.random,
        }
        time.sleep(random.randint(1, 2) / 32)
        try:
            reply_url = 'http://lf-hl.snssdk.com/2/comment/v3/reply_list/?' + urlencode(param_data)
            response = requests.get(reply_url, headers=headers,timeout=3)
            soup = response.json()
            print(soup)
            self.parse_reply_comment(soup,id,reply_list,offset_reply)
        except Exception as e:
            print('reply_comment is wrong', e)

    def parse_reply_comment(self,response,id,reply_list,offset_reply):
        #判断是否有下一页
        has_more = response['data']['has_more']
        comments = response['data']['data']
        for comment in comments:
            print('-------reply comment---------')
            #回复内容text
            text = comment['text']
            #回复时间
            create_time = comment['create_time']
            #点赞数
            digg_count = comment['digg_count']
            #用户名
            try:
                user_name = comment['user']['name']
            except:
                user_name = comment['user']['screen_name']
            #用户头像链接
            avatar_url = comment['user']['avatar_url']
            #回复的回复内容reply_to_comment
            try:
                reply_to_text = comment['reply_to_comment']['text']
                reply_to_user = comment['reply_to_comment']['user_name']
                try:
                    large_image_list = comment['reply_to_comment']['large_image_list']
                    url_img_list = []
                    for url_list in large_image_list:
                        url_img_list.append(url_list['url'])
                except:
                    url_img_list = []
                reply_to_comment = {
                    'reply_to_text': reply_to_text,
                    'reply_to_user': reply_to_user,
                    'url_img_list': url_img_list
                }
            except:
                reply_to_comment = {}

            print('reply_text: ', text)

            items = {
                'nickname': user_name,
                'avatar': avatar_url,
                'content': text,
                'fabulous': digg_count,
                'comment_time': create_time,
                'reply_to_comment': reply_to_comment
            }
            reply_list.append(items)

        else:
            if has_more:
                print('111111')
                offset_reply += 50
                self.get_reply_comment(id,reply_list, offset_reply)

    def run(self):
        while True:
            data = self.redis_cli.spop('spider_toutiao_comment_zero_id')
            print(type(data), data)
            if data == None:
                time.sleep(600)
                print('data is None')
                continue
            data = eval(str(data))  #str转成dict
            item_id = data['item_id']
            group_id = data['group_id']
            save_time = data['save_time']

            try:
                self.get_comment(item_id,group_id,save_time)
            except:
                continue

if __name__ == "__main__":
    for i in range(5):
        t = Comment()
        work_thread = Thread(target=t.run)
        work_thread.start()