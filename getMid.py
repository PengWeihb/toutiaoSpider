# -*- coding:utf-8 -*-

import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from MySQLdb import *

def get_mid(usr_id,d):
	url = 'https://www.toutiao.com/c/user/' + str(usr_id) + '/'

	driver = webdriver.PhantomJS()
	driver.get(url)
	time.sleep(1)
	driver.refresh()
	new_url = driver.current_url
	print new_url
	pattern = re.compile(r'\d+')
	response = re.findall(pattern,new_url)
	if len(response)==2:
		data = response[1]
	else:
		data = '[]'
	data = str(data)
	print data
	d = str(d)
	Update_mid(data,d)
	driver.quit()


def Update_mid(mid,n):
	params = [mid,n]
	db = connect(host="secret", port=3306, db="Spider", user="root", passwd="secret", charset="utf8")
	conn = db.cursor()

	try:
		sql = """update Media6 set mid =%s WHERE iid=%s"""
		print 'ok!!!'
		user_mid = conn.execute(sql,params)
		db.commit()
	except:
		db.rollback()
	db.close()

if __name__ == '__main__':
	db = connect(host="secret", port=3306, db="Spider", user="root", passwd="secret", charset="utf8")
	conn = db.cursor()
	try:
		sql = 'SELECT userId FROM Media6'
		MainUrl = conn.execute(sql)
		data = conn.fetchall()
		db.commit()
	except:
		db.rollback()

	for i in range(len(data)):
		usr_id = data[i][0]
		d = i + 1
		get_mid(usr_id,d)
	db.close()
