# -*- coding:utf-8 -*-
import time
import threading

from config import THREAD_NUM
from twitter import error
from api import Api, API_COUNT
from decorator import generate_decorator

class RelationCrawler:
	get_api = Api().get_api
	handle_exception = generate_decorator(800)
	

	'''
	获取用户关系信息
	'''
	def show_friendship(self,
						source_user_id, 
						source_screen_name, 
						target_user_id, 
						target_screen_name):

		if not source_user_id and not source_screen_name:
			return None

		if not target_user_id and not target_screen_name:
			return None

		return self.get_api().ShowFriendship(source_user_id, 
											 source_screen_name, 
											 target_user_id, 
											 target_screen_name)


	'''
	获取用户关系信息，如果超时则会休眠800s，然后返回关系信息
	'''
	def show_friendship_sleep(self,
							  source_user_id = None, 
							  source_screen_name = None, 
							  target_user_id = None, 
							  target_screen_name = None):

		wrapper_func = self.handle_exception(self.show_friendship)
		relation = wrapper_func(source_user_id, source_screen_name, target_user_id, target_screen_name)
		
		return relation


	'''
	获取用户朋友id
	'''
	def get_friendids(self,
                      user_id = None,
                      screen_name = None,
                      cursor = None,
                      total_count = 30000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriendIDs(user_id = user_id,
					                       screen_name = screen_name,
					                       cursor = cursor,
					                       total_count = total_count)


	'''
	分页获取用户朋友id
	'''
	def get_friendids_paged(self,
	                        user_id = None,
	                        screen_name = None,
	                        cursor = -1,
	                        stringify_ids = False,
	                        count = 5000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriendIDsPaged(user_id = user_id,
						                        screen_name = screen_name,
						                        cursor = cursor,
						                        count = count,
						                        stringify_ids = stringify_ids)


	'''
	分页获取用户朋友id，如果超时则会休眠800s，然后返回朋友信息
	'''
	def get_friendids_paged_sleep(self,
	                        	  user_id = None,
		                          screen_name = None,
		                          cursor = -1,
		                          stringify_ids = False,
		                          count = 5000):

		wrapper_func = self.handle_exception(self.get_friendids_paged)
		friendids = wrapper_func(user_id = user_id,
								screen_name = screen_name,
								cursor = cursor,
								stringify_ids = stringify_ids,
								count = count)

		return friendids
	

	'''
	获取用户朋友基础信息
	'''
	def get_friends(self,
                    user_id = None,
                    screen_name = None,
                    cursor = None,
                    total_count = None,
                    skip_status = True,
                    include_user_entities = True):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriends(user_id = user_id,
				                         screen_name = screen_name,
				                  	     cursor = cursor,
				                  	     total_count = total_count,
				                  	     skip_status = skip_status,
				                  	     include_user_entities = include_user_entities)
		
	'''
	分页获取用户朋友基础信息
	'''
	def get_friends_paged(self,
                   		  user_id = None,
                          screen_name = None,
                          cursor = -1,
                          count = 200,
                          skip_status = True,
                          include_user_entities = True):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriendsPaged(user_id = user_id,
					                       	  screen_name = screen_name,
					                       	  cursor = cursor,
					                       	  count = count,
					                       	  skip_status = skip_status,
					                       	  include_user_entities = include_user_entities)

	'''
	获取用户所有朋友的id，并保存
	'''
	def get_all_friendids(self, 
						  user_id = None, 
						  screen_name = None):

		cursor = -1
		while cursor != 0:
			out = self.get_friendids_paged_sleep(user_id = user_id,
												 screen_name = screen_name, 
												 cursor = cursor, 
												 count = 5000)
			if not out:
				return None

			cursor = out[0]
			friend_list = out[2]
		

	'''
	获取用户粉丝id
	'''
	def get_followerids(self,
	                    user_id = None,
	                    screen_name = None,
	                    cursor = None,
	                    total_count = 30000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFollowerIDs(user_id = user_id,
											 screen_name = screen_name,
											 cursor = cursor,
											 total_count = total_count)


	'''
	分页获取用户粉丝id
	'''
	def get_followerids_paged(self,
		                      user_id = None,
		                      screen_name = None,
		                      cursor = -1,
		                      stringify_ids = False,
		                      count = 5000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFollowerIDsPaged(user_id = user_id,
							                 	  screen_name = screen_name,
							                 	  cursor = cursor,
							                 	  count = count,
							                 	  stringify_ids = stringify_ids)


	'''
	分页获取用户粉丝id，如果超时则会休眠800s，然后返回粉丝信息
	'''
	def get_followerids_paged_sleep(self,
	                        	    user_id = None,
		                            screen_name = None,
		                            cursor = -1,
		                            stringify_ids = False,
		                            count = 5000):

		wrapper_func = self.handle_exception(self.get_followerids_paged)
		followerids = wrapper_func(user_id = user_id,
								   screen_name = screen_name,
								   cursor = cursor,
								   stringify_ids = stringify_ids,
								   count = count)

		return followerids


	'''
	获取用户粉丝基础信息
	'''
	def get_followers(self,
	                  user_id = None,
	                  screen_name = None,
	                  cursor = None,
	                  total_count = None,
	                  skip_status = True,
	                  include_user_entities = True):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFollowers(user_id = user_id,
					                       screen_name = screen_name,
					                       cursor = cursor,
					                       total_count = total_count,
					                       skip_status = skip_status,
					                       include_user_entities = include_user_entities)


	'''
	分页获取用户粉丝基础信息
	'''
	def get_followers_paged(self,
	                   		user_id = None,
	                        screen_name = None,
	                        cursor = -1,
	                        count = 200,
	                        skip_status = True,
	                        include_user_entities = True):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFollowersPaged(user_id = user_id,
						                        screen_name = screen_name,
						                        cursor = cursor,
						                        count = count,
						                        skip_status = skip_status,
						                        include_user_entities = include_user_entities)


	'''
	获取用户所有粉丝的id，并保存
	'''
	def get_all_followersids(self, 
							 user_id = None, 
							 screen_name = None):

		cursor = -1
		while cursor != 0:
			out = self.get_followerids_paged_sleep(user_id = user_id,
												   screen_name = screen_name, 
												   cursor = cursor, 
												   count = 5000)
			if not out:
				return None

			cursor = out[0]
			follower_list = out[2]