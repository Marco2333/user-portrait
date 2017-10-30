# -*- coding:utf-8 -*-
import time
import threading

from config import THREAD_NUM
from twitter import error
from api import Api, API_COUNT
from database import MongoDB
from decorator import generate_decorator

handle_exception = generate_decorator(300)

class TweetsCrawler:
	get_api = Api().get_api


	'''
	Fetch the sequence of public Status messages for a single user.

	Parameters:	
		user_id (int, optional) – Specifies the ID of the user for whom to return the user_timeline.
				Helpful for disambiguating when a valid user ID is also a valid screen name.
		screen_name (str, optional) – Specifies the screen name of the user for whom to return the user_timeline.
				Helpful for disambiguating when a valid screen name is also a user ID.
		since_id (int, optional) – Returns results with an ID greater than (that is, more recent than) the specified ID. 
				There are limits to the number of Tweets which can be accessed through the API. If the limit of Tweets has 
				occurred since the since_id, the since_id will be forced to the oldest ID available.
		max_id (int, optional) – Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.
		count (int, optional) – Specifies the number of statuses to retrieve. May not be greater than 200.
		include_rts (bool, optional) – If True, the timeline will contain native retweets (if they exist) in addition to the standard stream of tweets.
		trim_user (bool, optional) – If True, statuses will only contain the numerical user ID only. Otherwise a full user object will be returned for each status.
		exclude_replies (bool, optional) – If True, this will prevent replies from appearing in the returned timeline. Using exclude_replies with the 
				count parameter will mean you will receive up-to count tweets - this is because the count parameter retrieves that many tweets 
				before filtering out retweets and replies. This parameter is only supported for JSON and XML responses.
	
	Returns:	
		A sequence of Status instances, one for each message up to count
	'''
	def get_user_timeline(self,
						  user_id = None,
						  screen_name = None,
						  since_id = None,
						  max_id = None,
						  count = None,
						  include_rts = True,
						  trim_user = True,
						  exclude_replies = False):

		if user_id == None and screen_name == None:
			return None

		return  self.get_api().GetUserTimeline(user_id = user_id,
											   screen_name = screen_name,
											   since_id = since_id,
											   max_id = max_id,
											   count = count,
											   include_rts = include_rts,
											   trim_user = trim_user,
											   exclude_replies = exclude_replies)


	'''
	获取用户所有推文信息，并保存在数据库(MongoDB)中（参考 get_user_timeline ）

	参数：
		collect_name：数据库集合名，默认 tweets_task
	'''
	def get_user_all_timeline(self,
							  user_id = None,
							  collect_name = "tweets_task",
							  screen_name = None,
							  include_rts = True,
							  exclude_replies = False):

		if user_id == None and screen_name == None:
			return None

		if user_id:
			user_id = long(user_id)
			
		flag = True
		tweets = [0]
		sleep_count = 0
	
		db = MongoDB().connect()
		collect = db[collect_name]
		get_api = self.get_api

		while len(tweets) > 0:
			try:
				if flag:
					tweets = get_api().GetUserTimeline(user_id = user_id,
													   screen_name = screen_name,
													   include_rts = include_rts,
													   exclude_replies = exclude_replies,
													   trim_user = True,
													   count = 200)
					flag = False

				else:
					tweets = get_api().GetUserTimeline(user_id = user_id,
													   screen_name = screen_name,
													   include_rts = include_rts,
													   exclude_replies = exclude_replies,
							 						   trim_user = True,
													   count = 200,
													   max_id = tweets[-1].id - 1)

			except error.TwitterError as te:
				try:
					if te.message[0]['code'] == 88:
						sleep_count += 1

						if sleep_count >= API_COUNT:
							print "sleeping..."
							sleep_count = 0
							time.sleep(300)
						continue

					else:
						print te
						break
				except Exception as ee:
					print ee
					break
			except Exception as e:
				break
				
			for tt in tweets:
				tweet = self.tweetobj_to_dict(tt)
				try:
					collect.insert_one(tweet)
				except Exception as e:
					continue
	

	'''
	获取用户所有推文信息，并返回（参考 get_user_timeline ）
	'''
	def get_user_all_timeline_return(self,
									 user_id = None,
									 screen_name = None,
									 include_rts = True,
									 exclude_replies = False):

		if user_id == None and screen_name == None:
			return None

		if user_id:
			user_id = long(user_id)

		flag = True
		tweets = [0]
		sleep_count = 0

		tweet_list = []

		get_api = self.get_api

		while len(tweets) > 0:
			try:
				if flag:
					tweets = get_api().GetUserTimeline(user_id = user_id,
													   screen_name = screen_name,
													   include_rts = include_rts,
													   exclude_replies = exclude_replies,
													   trim_user = True,
													   count = 200)
					flag = False

				else:
					tweets = get_api().GetUserTimeline(user_id = user_id,
													   screen_name = screen_name,
													   include_rts = include_rts,
													   exclude_replies = exclude_replies,
							 						   trim_user = True,
													   count = 200,
													   max_id = tweets[-1].id - 1)

			except error.TwitterError as te:
				try:
					if te.message[0]['code'] == 88:
						sleep_count += 1

						if sleep_count >= API_COUNT:
							print "sleeping..."
							sleep_count = 0
							time.sleep(300)
						continue

					else:
						print te
						break
				except Exception as ee:
					print ee
					break
			except Exception as e:
				print e
				break

			for tt in tweets:
				tweet = self.tweetobj_to_dict(tt)
				try:
					tweet_list.append(tweet)
				except Exception as e:
					continue

		return tweet_list


	'''
	获取所有用户推文信息

	参数：
		user_list (list, optional):
			存放用户 user_id / screen_name 的列表
		collect_name (str, optional):
			存储数据集合名，默认 tweets_task
		search_type (str, optional):
			抓取方式，如果为 screen_name ，则认为 user_list 中 存放的是用户 screen_name，
			否则认为 user_list 中 存放的是用户 user_id

	'''
	def get_all_users_timeline(self,
							   user_list = None,
							   collect_name = "tweets_task",
							   search_type = "user_id",
							   include_rts = True,
							   exclude_replies = False):

		if len(user_list) == 0:
			return

		i = 0
		thread_pool = []
		length = len(user_list)
		per_thread = length / THREAD_NUM

		while i < THREAD_NUM:
			if i + 1 == THREAD_NUM:
				crawler_thread = threading.Thread(target = self.get_all_users_timeline_thread, 
					args = (user_list[i * per_thread : ], collect_name, search_type, include_rts, exclude_replies,))
			else:
				crawler_thread = threading.Thread(target = self.get_all_users_timeline_thread, 
					args = (user_list[i * per_thread : (i + 1) * per_thread], collect_name, search_type, include_rts, exclude_replies,))
			
			crawler_thread.start()
			thread_pool.append(crawler_thread)

			i += 1

		for t in thread_pool:
			t.join()


	'''
	线程：获取多个用户推文信息（参考 get_all_users_timeline ）
	'''
	def get_all_users_timeline_thread(self,
									  user_list = [],
									  collect_name = "tweets_task",
									  search_type = "user_id",
									  include_rts = True,
									  exclude_replies = False):

		if search_type != "screen_name":
			while len(user_list) > 0:
				user_id = user_list.pop(0)

				self.get_user_all_timeline(user_id = user_id,
										   collect_name = collect_name,
										   include_rts = include_rts,
										   exclude_replies = exclude_replies)
		else:
			while len(user_list) > 0:
				screen_name = user_list.pop(0)

				self.get_user_all_timeline(screen_name = screen_name,
										   collect_name = collect_name,
										   include_rts = include_rts, 
										   exclude_replies = exclude_replies)


	'''
	Returns a single status message, specified by the status_id parameter.

	Parameters:	
		status_id – The numeric ID of the status you are trying to retrieve.
		trim_user – When set to True, each tweet returned in a timeline will include a user object including only the status authors numerical ID. 
				Omit this parameter to receive the complete user object. [Optional]
		include_entities – If False, the entities node will be disincluded. This node offers a variety of metadata about the tweet in a 
				discreet structure, including: user_mentions, urls, and hashtags. [Optional]
	
	Returns:	
		A twitter.Status instance representing that status message
	'''
	def get_status(self,
				   status_id, 
				   trim_user = True, 
				   include_entities = True):

		if status_id == None:
			return None

		return self.get_api().GetStatus(status_id = status_id,
										trim_user = trim_user,
										include_my_retweet = False,
										include_entities = include_entities)


	'''
	根据推文ID获取所有推文信息（参考 get_status ）

	参数：
		status_list (list, optional):
			存放tweet id 的列表
		collect_name (str, optional):
			存储数据集合名，默认 status
	'''
	def get_all_status(self,
					   status_list = [],
					   collect_name = 'status',
					   trim_user = True,
					   include_entities = True):

		if len(status_list) == 0:
			return

		i = 0
		thread_pool = []
		length = len(status_list)
		per_thread = length / THREAD_NUM

		while i < THREAD_NUM:
			if i + 1 == THREAD_NUM:
				crawler_thread = threading.Thread(target = self.get_all_status_thread, 
					args = (status_list[i * per_thread : ], collect_name, trim_user, include_entities,))
			else:
				crawler_thread = threading.Thread(target = self.get_all_status_thread, 
					args = (status_list[i * per_thread : (i + 1) * per_thread], collect_name, trim_user, include_entities,))
			
			crawler_thread.start()
			thread_pool.append(crawler_thread)

			i += 1

		for t in thread_pool:
			t.join()


	'''
	线程：根据推文ID获取所有推文信息（参考 get_all_status ）
	'''
	def get_all_status_thread(self,
							  status_list = [],
							  collect_name = 'status',
							  trim_user = True,
							  include_entities = True):

		wrapper_func = handle_exception(self.get_status)

		db = MongoDB().connect()
		collect = db[collect_name]

		while len(status_list) > 0:
			status_id = status_list.pop(0)
			status_obj = wrapper_func(status_id)

			status = self.tweetobj_to_dict(status_obj)

			if not status:
				continue

			try:
				collect.insert_one(status)
			except Exception as e:
				continue
	

	'''
	将推文对象转换为字典类型
	'''
	def tweetobj_to_dict(self, tt):
		if tt == None:
			return None

		tweet = {
			'coordinates': tt.coordinates,  # Coordinates
			'created_at': tt.created_at, # String
			'favorite_count': tt.favorite_count, # int
			'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
			'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
			'_id': tt.id_str, # String
			'in_reply_to_status_id': tt.in_reply_to_status_id,
			'in_reply_to_user_id': tt.in_reply_to_user_id,
			'lang': tt.lang, # String
			'place': tt.place, # Place
			'possibly_sensitive': tt.possibly_sensitive, # Boolean
			'retweet_count': tt.retweet_count, # int
			'source': tt.source, # String
			'text': tt.text, # String
			'user_id': tt.user.id, # int
			'user_mentions': map(lambda x: x.id, tt.user_mentions), # []
			'withheld_copyright': tt.withheld_copyright, # Boolean
			'withheld_in_countries': tt.withheld_in_countries, # Array of String
			'withheld_scope': tt.withheld_scope, #String
		}

		return tweet


if __name__ == '__main__':
	ts = TweetsCrawler()
	print ts.get_user_all_timeline(screen_name = 'mrmarcohan')