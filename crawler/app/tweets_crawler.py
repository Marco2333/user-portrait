# -*- coding:utf-8 -*-
import time
import threading

from config import THREAD_NUM
from twitter import error
from api import Api, API_COUNT
from database import MongoDB


class TweetsCrawler:
	get_api = Api().get_api
		
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

		return  self.get_api().GetUserTimeline(user_id = user_id,	screen_name = screen_name, 
											   since_id = since_id, max_id = max_id, count = count,
											   include_rts = include_rts, trim_user = trim_user,
											   exclude_replies = exclude_replies)


	def get_user_all_timeline(user_id = None,
						  	  screen_name = None, 
						  	  collect_name = "tweets",
						  	  include_rts = True, 
						  	  exclude_replies = False):

		if users == None and screen_name == None:
			return None

		flag = True
		tweets = [0]
		sleep_count = 0
	
		db = MongoDB().connect()
		collect = db[collect_name]
		get_api = self.get_api

		while len(tweets) > 0:
			try:
				if flag:
					tweets = get_api().GetUserTimeline(user_id = user_id, screen_name = screen_name, 
													   include_rts = include_rts, exclude_replies = exclude_replies,
							  	  					   trim_user = True, count = 200)
					flag = False

				else:
					tweets = get_api().GetUserTimeline(user_id = user_id, screen_name = screen_name,
													   include_rts = include_rts, exclude_replies = exclude_replies,
							 						   trim_user = True, count = 200, max_id = tweets[-1].id - 1)

			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == API_COUNT:
						print "sleeping..."
						sleep_count = 0
						time.sleep(600)
					continue
				else:
					break
			except Exception as e:	
				break
				
			for tt in tweets:
				tweet = {
					'coordinates': tt.coordinates,  # Coordinates
					'created_at': tt.created_at, # String
					'favorite_count': tt.favorite_count, # int
					'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
					'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
					'_id': tt.id_str, # String
					# 'in_reply_to_screen_name': tt.in_reply_to_screen_name,
					'in_reply_to_status_id': tt.in_reply_to_status_id,
					'in_reply_to_user_id': tt.in_reply_to_user_id,
					'lang': tt.lang, # String
					# 'media': tt.media,
					'place': tt.place, # Place
					'possibly_sensitive': tt.possibly_sensitive, # Boolean
					'retweet_count': tt.retweet_count, # int
					'source': tt.source, # String
					'text': tt.text, # String
					# 'truncated': tt.truncated,
					# 'urls': tt.urls, # []
					'user_id': tt.user.id, # int
					'user_mentions': map(lambda x: x.id, tt.user_mentions), # []
					'withheld_copyright': tt.withheld_copyright, # Boolean
					'withheld_in_countries': tt.withheld_in_countries, # Array of String
					'withheld_scope': tt.withheld_scope, #String
				}
				try:
					collect.insert_one(tweet)
				except Exception as e:
					continue
	
	
	def get_user_all_timeline_temp(self, 
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
					tweets = get_api().GetUserTimeline(user_id = user_id, screen_name = screen_name, 
													   include_rts = include_rts, exclude_replies = exclude_replies,
								  	  				   trim_user = True, count = 200)
					flag = False

				else:
					tweets = get_api().GetUserTimeline(user_id = user_id, screen_name = screen_name,
												   include_rts = include_rts, exclude_replies = exclude_replies,
							 					   trim_user = True, count = 200, max_id = tweets[-1].id - 1)

			except error.TwitterError as te:
				if hasattr(te.message, 'code') and te.message['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(600)
					continue
				else:
					break
			except Exception as e:
				print e
				break

			for tt in tweets:
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
				try:
					tweet_list.append(tweet)
				except Exception as e:
					continue

		return tweet_list


	def get_all_users_timeline(user_list = None,
							   collect_name = "tweets",
							   search_type = "user_id",
							   include_rts = True, 
							   exclude_replies = False):		

		if len(user_list) == 0:
			return

		i = 0
		thread_pool = []
		per_thread = length / THREAD_NUM

		while i < threadNum:
			if i + 1 == threadNum:
				craw_thread = threading.Thread(target = self.get_users_timeline_thread, 
					args = (user_list[i * per_thread : ], collect_name, search_type, include_rts, exclude_replies,))
			else:
				craw_thread = threading.Thread(target = self.get_users_timeline_thread, 
					args = (user_list[i * per_thread : (i + 1) * per_thread], collect_name, search_type, include_rts, exclude_replies,))
			
			craw_thread.start()
			thread_pool.append(craw_thread)

			i += 1

		for thread in thread_pool:
			thread.join()


	def get_users_timeline_thread(self,
								  user_list = [], 
								  collect_name = "tweets", 
								  search_type = "user_id", 
								  include_rts = True, 
								  exclude_replies = False):
	
		while len(user_list) > 0:
			user_id = user_list.pop(0)

			if search_type == "screen_name":
				self.get_user_all_timeline(screen_name = user_id,
									       collect_name = collect_name,
						  	  		       include_rts = include_rts, 
						  	  	           exclude_replies = exclude_replies)
			else:
				self.get_user_all_timeline(user_id = user_id,
									       collect_name = collect_name,
						  	  		       include_rts = include_rts, 
						  	  	           exclude_replies = exclude_replies)
