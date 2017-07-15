# -*- coding:utf-8 -*-
import time
import threading

from config import THREAD_NUM
from twitter import error
from api import Api, API_COUNT


class RelationCrawler:
	get_api = Api().get_api
	
	'''
	获取用户的关系信息
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
	保存用户关系的信息
	'''
	def save_friendship(self,
						source_user_id = None, 
						source_screen_name = None, 
						target_user_id = None, 
						target_screen_name = None):

		if not source_user_id and not source_screen_name:
			return None

		if not target_user_id and not target_screen_name:
			return None

		sleep_count = 0

		while True:
			try:
				relation = self.get_api().ShowFriendship(source_user_id, 
												 		source_screen_name, 
												 		target_user_id, 
												 		target_screen_name)
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
					return None

			except Exception as e:
				print e
				return None

			return relation


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


	def get_friendids_paged_sleep(self,
	                        	  user_id = None,
		                          screen_name = None,
		                          cursor = -1,
		                          stringify_ids = False,
		                          count = 5000):

		if user_id == None and screen_name == None:
			return None

		sleep_count = 0
		res = None

		while True:
			try:
				res = self.get_api().GetFriendIDsPaged(user_id = user_id,
								                       screen_name = screen_name,
								                       cursor = cursor,
								                       count = count,
								                       stringify_ids = stringify_ids)
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

			break

		return res

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


	def get_all_friendids(self, 
						  user_id = None, 
						  screen_name = None):

		if user_id == None and screen_name == None:
			return None

		cursor = -1
		sleep_count = 0

		api = self.api

		while cursor != 0:
			try:
				out = get_api().GetFriendIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == API_COUNT:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue

			except Exception as e:
				continue


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


	def get_all_followersids(self, user_id = None, screen_name = None):

		if user_id == None and screen_name == None:
			return None

		cursor = -1
		sleep_count = 0

		api = self.api

		while cursor != 0:
			try:
				out = get_api().GetFollowersIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]

			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue
			except Exception as e:
				continue