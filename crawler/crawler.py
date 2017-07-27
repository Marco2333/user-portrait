# -*- coding: utf-8 -*-
import threading

from app.database import Mysql, MongoDB
from app.basicinfo_crawler import BasicinfoCrawler
from app.tweets_crawler import TweetsCrawler
# from app.relation_crawler import RelationCrawler

basicinfo_crawler = BasicinfoCrawler()
tweets_crawler = TweetsCrawler()
# relation_crawler = RelationCrawler()


'''
获取所有用户的基础信息，存到 table_name 中
'''
def get_users_basicinfo(user_list, table_name = "user", search_type = "user_id"):
	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


'''
读取文件中的用户，抓取基础信息，存放到 table_name 中
'''
def get_users_basicinfo_from_file(file_name, table_name = "user", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


'''
读取数据库中的用户，抓取基础信息，存放到 table_name 中
'''
def get_users_basicinfo_from_db(sql, table_name = "user", search_type = "user_id"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


'''
获取所有用户的推文信息，存放到 collect_name 中
'''
def get_users_tweets(user_list, collect_name = "tweets", search_type = "user_id"):
	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


'''
读取文件中的用户，抓取推文信息，存放到 collect_name 中
'''
def get_users_tweets_from_file(file_name, collect_name = "tweets", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


'''
读取数据库中的用户，抓取推文信息，存放到 collect_name 中
'''
def get_users_tweets_from_db(sql, collect_name = "tweets", search_type = "screen_name"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def filter():
	db = MongoDB().connect()
	collect = db['typical']

	users = collect.find()

	res = []
	for item in users:
		u = basicinfo_crawler.get_user(user_id = item['_id'])
		collect.update({"_id": item['_id']}, {'$set': {'created_at': u.created_at, 'lang': u.lang, 
			'protected': u.protected, 'time_zone': u.time_zone, 'utc_offset': u.utc_offset,
			'listed_count': u.listed_count, 'default_profile_image': u.default_profile_image, 'profile_background_color': u.profile_background_color,
			'profile_image_url': u.profile_image_url, 'profile_banner_url': u.profile_banner_url}})

		
if __name__ == "__main__":
	# db = MongoDB().connect()
	# collect = db['typical']