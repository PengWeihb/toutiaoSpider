#coding:utf-8

from urllib import request
import http.cookiejar

'''
获取服务器返回的cookie
'''

def get_cookie():
    
    #url = 'https://www.toutiao.com/i6560652557499236877/'
    #url = 'https://www.toutiao.com/'
    #url = 'https://www.toutiao.com/c/user/84270793100/'
    url = 'https://m.toutiao.com/'

    header = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36')]

    #req = request.Request(url)
    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    opener.addheaders = header
    opener.open(url)
    cookieStr = ""
    for item in cj:
        print(item)
        cookieStr = cookieStr + item.name + "=" + item.value + ";"
    print(cookieStr[:-1])

if __name__ == "__main__":
    get_cookie()
