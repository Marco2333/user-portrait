# -*- coding: utf-8 -*-
import time
import threading

from app.database import Mysql, MongoDB
from app.basicinfo_crawler import BasicinfoCrawler
from app.tweets_crawler import TweetsCrawler
# from app.relation_crawler import RelationCrawler

basicinfo_crawler = BasicinfoCrawler()
tweets_crawler = TweetsCrawler()
# relation_crawler = RelationCrawler()


'''
获取用户基础信息和推文信息，以字典形式返回
'''
def get_user_all_info(user_id = None, screen_name = None):
	user = basicinfo_crawler.get_user(user_id = user_id, screen_name = screen_name)
	tweets = tweets_crawler.get_user_all_timeline_return(user_id = user_id, screen_name = screen_name)

	return {
		'user_id': long(user.id),
		'screen_name': user.screen_name,
		'name': user.name,
		'verified': user.verified,
		'friends_count': user.friends_count,
		'description': user.description,
		'crawler_date': time.strftime('%Y-%m-%d',time.localtime(time.time())),
		'followers_count': user.followers_count,
		'location': user.location,
		'statuses_count': user.statuses_count,
		'favourites_count': user.favourites_count,
		'lang': user.lang,
		'utc_offset': user.utc_offset,
		'protected': user.protected,
		'profile_background_color': user.profile_background_color,
		'default_profile_image': user.default_profile_image,
		'created_at': user.created_at,
		'profile_banner_url': user.profile_banner_url,
		'time_zone': user.time_zone,
		'profile_image_url': user.profile_image_url,
		'listed_count': user.listed_count,
		'tweets': tweets
	}


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


'''
根据推文ID抓取推文，存放在数据库中（推文 id 存放在file_name中，每行一条）
'''
def get_tweet_list_by_statusids(file_name):
	file = open(file_name)

	tweet_list = []
	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        tweet_list.append(line.strip())

	tweets_crawler.get_all_status(tweet_list, 'tweets_100w')
		


if __name__ == "__main__":
	get_tweet_list_by_statusids('./file/tweet_150w.txt')