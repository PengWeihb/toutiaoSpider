# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from pymysql import *
import time
from binascii import a2b_base64
import hashlib
import os
import oss2

'''
今日头条用户头像图片下载(图片链接已经下载好）
'''

def md5(val):
    if type(val)!=bytes:
        val = val.encode('utf-8')
    return hashlib.md5(val).hexdigest()

def download_img(url, root_path='/tmp/img/', headers=None):
    try:
        if not url:
            return ''
        img_ext = 'png'
        filename = ''
        binary_data = b''
        if url[0:22]=='data:image/png;base64,':
            from binascii import a2b_base64
            data = bytes(url[22:], encoding='utf8')
            binary_data = a2b_base64(data)
            filename = md5(binary_data)
            img_ext = 'png'
            path = root_path + filename
            if not os.path.exists(root_path):
                os.makedirs(root_path)
            img_file = '%s.%s' % (path, img_ext, )
            if not os.path.exists(img_file):
                with open(img_file,'wb') as f:
                    f.write(binary_data)
        else:
            if url[0:2]=='//':
                url = 'https:'+url
            url = url.replace('\\','')
            r = requests.get(url, headers=headers, stream=True, timeout=3)
            time.sleep(0.2)
            filename = md5(url.split('/')[-1])
            img_ext = r.headers['Content-Type'].split('/')[1]
            path = root_path + filename
            if not os.path.exists(root_path):
                os.makedirs(root_path)
            img_file = '%s.%s' % (path, img_ext, )
            if not os.path.exists(img_file):
                with open(img_file,'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
        # end if
        return (img_file, img_ext)
    except TimeoutError as e:
        print(url)
    except Exception as e:
        print(url)
        raise e

def oss(subpath, url, headers=None, filename=False):
    if not url:
        return ''
    if url[0:4]=='http' or url[0:2]=='//' or url[0:22]=='data:image/png;base64,':
        (img_path, ext) = download_img(url, headers=headers)
    else:
        (img_path, ext) = (url, os.path.splitext(url)[1][1:])
        
    if filename:
        imgfile = '%s/%s.%s' % (subpath, str(filename), ext)
    else:
        imgfile = '%s/%s.%s' % (subpath, md5(url), ext)

    oss_config = {
        'accesskeyid': 'fhgfdsgsg',
        'accesskey': '35757587fhdfhjdh',
        'endpoint': 'oss-cn-guangzhou.aliyuncs.com',
        'bucket_name': 'hdfdwa',
    }

    accesskeyid = oss_config.get('accesskeyid')
    accesskey = oss_config.get('accesskey')
    endpoint = oss_config.get('endpoint')
    bucket_name = oss_config.get('bucket_name')
    ossid = oss_config.get('')
    auth = oss2.Auth(accesskeyid, accesskey)
    timeout = 3
    bucket = oss2.Bucket(auth, 'http://%s' % (endpoint,), bucket_name, connect_timeout=timeout)
    bucket.put_object_from_file(imgfile, img_path)
    return 'http://%s.%s/%s' % (bucket_name, endpoint, imgfile, )

def conn_sql():
    try:
        sql = """select id,uid,logo,flag from toutiao_image"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        flag = data[i][3]
        mlogostart = 'https://gghg3DAS'
        mlogo = data[i][2]
        if flag == '今日头条':
            if not mlogo.startswith(mlogostart, 0, 59):
                openid = data[i][1]
                msubpath = 'media_avatar'
                mlogo = oss(msubpath, mlogo, filename=openid)
                time.sleep(0.1)

                param = [mlogo, id]
                try:
                    sql = """update toutiao_image set logo = %s where id = %s"""
                    cursor.execute(sql, param)
                    db.commit()
                except:
                    db.rollback()

if __name__ == '__main__':
    db = connect(host='localhost', port=3306, db='spider', user='root', password='secret',charset='utf8')
    cursor = db.cursor()
    conn_sql()
    db.close()
