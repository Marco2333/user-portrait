# -*- coding:utf-8 -*-
import time
import threading

from config import THREAD_NUM
from twitter import error
from api import Api, API_COUNT
from database import Mysql


class BasicinfoCrawler:
	get_api = Api().get_api
	mysql = Mysql()
	mysql.connect()

	'''
	获取与term相关的用户信息
	'''
	def get_user_search(self, 
						term = None, 
						page = 1, 
						count = 20, 
						include_entities = True):

		if term == None:
			return None

		return self.get_api().GetUsersSearch(term = term, 
											 page = page, 
											 count = count, 
											 include_entities = include_entities)

	


	'''
	获取单个用户的信息
	'''
	def get_user(self,
				 user_id = None, 
				 screen_name = None, 
				 include_entities = True):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetUser(user_id = user_id,	
									  screen_name = screen_name, 
									  include_entities = include_entities)


	'''
	获取单个用户的信息并保存
	'''
	def get_user_save(self,
					  user_id = None, 
					  table_name = "user_task",
					  screen_name = None, 
					  include_entities = True):

		if user_id == None and screen_name == None:
			return None

		sleep_count = 0

		while True:
			try:
				user = self.get_api().GetUser(user_id = user_id,	
			  						   		  screen_name = screen_name, 
			  						   		  include_entities = include_entities)

			except error.TwitterError as te:
				print te
				if te.message[0]['code'] == 88:
					sleep_count += 1

					if sleep_count == API_COUNT:
						print "sleeping..."
						sleep_count = 0
						time.sleep(500)						
					continue

				else:
					print te
					return None

			except Exception as e:
				print e
				return None

			break

		self.save_user(user, table_name)

	'''
	获取多个用户的信息，并存入数据库中
	'''
	def get_all_users(self, 
					  user_list = None, 
					  table_name = "user", 
					  search_type = "user_id"):		

		if len(user_list) == 0:
			return None

		i = 0
		thread_pool = []
		length = len(user_list)

		per_thread = length / THREAD_NUM
		
		while i < THREAD_NUM:
			if i + 1 == THREAD_NUM:
				craw_thread = threading.Thread(target = self.get_users_thread, args = (user_list[i * per_thread : ], table_name, search_type,))
			else:
				craw_thread = threading.Thread(target = self.get_users_thread, args = (user_list[i * per_thread : (i + 1) * per_thread], table_name, search_type,))
			
			craw_thread.start()
			thread_pool.append(craw_thread)

			i += 1

		for thread in thread_pool:
			thread.join()


	def get_users_thread(self, user_list = None, table_name  = "user_task", search_type = "user_id"):
		sleep_count = 0

		get_api = self.get_api

		while len(user_list) > 0:
			user_id = user_list[0]

			try:
				if search_type == "screen_name":
					user = get_api().GetUser(screen_name = user_id)
				else:
					user = get_api().GetUser(user_id = user_id)

			except error.TwitterError as te:
				print te
				if te.message[0]['code'] == 88:
					sleep_count += 1

					if sleep_count == API_COUNT:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					print te
					user_list.pop(0)
					continue
			except Exception as e:
				print e
				user_list.pop(0)	
				continue

			user_list.pop(0)

			self.save_user(user, table_name)

		mysql.close()


	'''
	保存用户信息
	'''
	def save_user(self, user, table_name = "user_task"):
		try:
			is_translator = 0
			if hasattr(user, "is_translator"):
				is_translator = 1 if user.is_translator else 0

			name = user.name.replace("'","\\'")
			location = user.location.replace("'","\\'") if user.description else ''
			description = user.description.replace("'","\\'") if user.description else ''
			protected = 1 if user.protected else 0
			verified = 1 if user.verified else 0
			geo_enabled = 1 if user.geo_enabled else 0
			listed_count = user.listed_count if user.listed_count else 0
			default_profile_image = 1 if user.default_profile_image else 0 

			sql =  """INSERT INTO %s (user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
					followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
					is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
					('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
					'%s', '%s', '%s', '%s')""" % (table_name, user.id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
					user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
					user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
					user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

			sql = sql.encode("utf-8").decode("latin1")
		except Exception as e:
			print e
			return

		try:
			self.mysql.execute(sql)
		except Exception as e:
			print e
			return