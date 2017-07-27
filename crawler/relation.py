# -*- coding: utf-8 -*-
import threading

from app.database import Mysql, MongoDB
# from app.basicinfo_crawler import BasicinfoCrawler
# from app.tweets_crawler import TweetsCrawler
from app.relation_crawler import RelationCrawler

# basicinfo_crawler = BasicinfoCrawler()
# tweets_crawler = TweetsCrawler()
relation_crawler = RelationCrawler()


'''
获取列表中所有用户的相互关系
'''
def get_users_relationship(user_list):
	# 去重
	user_list = list(set(user_list))
	length = len(user_list)

	if length <= 1:
		return None

	# 去重部分（数据库中之前已经存在一部分关系）
	mysql = Mysql()
	mysql.connect()

	sql = "select * from relation"

	try:
		cur_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	s = set()
	for term in cur_list:
		s.add(term[0] + " " + term[1])


	# 开始获取用户之间的相互关系
	thread_num = 2
	per_thread = length / thread_num

	i = 0
	thread_pool = []
	
	while i < thread_num:
		if i + 1 == thread_num:
			crawler_thread = threading.Thread(target = get_users_relation_thread, 
							args = (user_list[i * per_thread : ], user_list, i * per_thread, s, ))
		else:
			crawler_thread = threading.Thread(target = get_users_relation_thread, 
							args = (user_list[i * per_thread : (i + 1) * per_thread], user_list, i * per_thread, s, ))
		
		crawler_thread.start()
		thread_pool.append(crawler_thread)

		i += 1

	for thread in thread_pool:
		thread.join()


'''
线程：获取列表中所有用户的相互关系 （show_friendship_sleep）
'''
def get_users_relation_thread(user_list, all_users, start_index, s):
	length = len(user_list)
	all_length = len(all_users)
	table_name = 'relation'

	mysql = Mysql()
	mysql.connect()

	i = 0
	for i in range(length):
		for j in range(start_index + i + 1, all_length):

			if user_list[i] + " " + all_users[j] in s:
				continue

			try:
				relation = relation_crawler.show_friendship_sleep(source_user_id = user_list[i], target_user_id = all_users[j])
				fb = relation['relationship']['source']['followed_by']
				fl = relation['relationship']['source']['following']
			except Exception as e:
				print e
				continue

			sql = """INSERT INTO %s (source_user_id, target_user_id, followed_by, following) VALUES ('%s', '%s', \
			'%s', '%s')""" % (table_name, user_list[i], all_users[j], str(fb), str(fl)) 

			try:
				mysql.execute(sql)
			except Exception as e:
				print e
				continue


'''
获取所有用户的所有朋友id
'''
def get_all_users_friends(user_list):
	thread_num = 3  # 线程数量
	length = len(user_list)

	i = 0
	thread_pool = []
	per_thread = length / thread_num

	while i < thread_num:
		if i + 1 == thread_num:
			crawler_thread = threading.Thread(target = get_all_users_friends_thread, 
				args = (user_list[i * per_thread : ],))
		else:
			crawler_thread = threading.Thread(target = get_all_users_friends_thread, 
				args = (user_list[i * per_thread : (i + 1) * per_thread],))
		
		crawler_thread.start()
		thread_pool.append(crawler_thread)

		i += 1

	for t in thread_pool:
		t.join()


'''
线程：获取所有用户的所有朋友的id
'''
def get_all_users_friends_thread(user_list):
	for user_id in user_list:
		get_user_all_friends_and_save(user_id)


'''
获取用户所有朋友id并保存
'''
def get_user_all_friends_and_save(user_id):
	cursor = -1
	collect_name = "user_portrayal"
	db = MongoDB().connect()
	collect = db[collect_name]

	while cursor != 0:
		out = relation_crawler.get_friendids_paged_sleep(user_id = user_id,
														 cursor = cursor, 
														 count = 5000)
		if not out:
			return None

		cursor = out[0]
		friend_list = out[2]

		if cursor == -1:
			collect.update({"_id": long(user_id)}, {'$set': {'friends': friend_list}})
		
		else:
			for f in friend_list:
				collect.update({"_id": long(user_id)}, {'$push': {'friends': f}})