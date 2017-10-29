# -*- coding:utf-8 -*-
import time
import threading

from twitter import error
from api import Api, API_COUNT
from decorator import generate_decorator

handle_exception = generate_decorator(720)

class RelationCrawler:
	get_api = Api().get_api
	

	'''
	Returns information about the relationship between the two users.

	Parameters:	
		source_id – The user_id of the subject user [Optional]
		source_screen_name – The screen_name of the subject user [Optional]
		target_id – The user_id of the target user [Optional]
		target_screen_name – The screen_name of the target user [Optional]
	Returns:	
		A Twitter Json structure.
	'''
	def show_friendship(self,
						source_user_id = None,
						source_screen_name = None,
						target_user_id = None,
						target_screen_name = None):

		if not source_user_id and not source_screen_name:
			return None

		if not target_user_id and not target_screen_name:
			return None

		return self.get_api().ShowFriendship(source_user_id,
											 source_screen_name,
											 target_user_id,
											 target_screen_name)


	'''
	获取用户关系信息，如果超时则会休眠800s，然后返回关系信息（参考 show_friendship ）
	'''
	def show_friendship_sleep(self,
							  source_user_id = None,
							  source_screen_name = None,
							  target_user_id = None,
							  target_screen_name = None):

		wrapper_func = handle_exception(self.show_friendship)
		relation = wrapper_func(source_user_id, source_screen_name, target_user_id, target_screen_name)
		
		return relation


	'''
	Fetch a sequence of user ids, one for each friend. Returns a list of all the given user’s friends’ IDs. 

	Parameters:
		user_id – The id of the user to retrieve the id list for. [Optional]
		screen_name – The screen_name of the user to retrieve the id list for. [Optional]
		cursor – Specifies the Twitter API Cursor location to start at. Note: there are pagination limits. [Optional]
		total_count – The total amount of UIDs to retrieve. Good if the account has many followers and you don’t want to get rate limited. 
	
	Returns:	
		A list of integers, one for each user id.
	'''
	def get_friendids(self,
					  user_id = None,
					  screen_name = None,
					  cursor = None,
					  total_count = 60000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriendIDs(user_id = user_id,
										   screen_name = screen_name,
										   cursor = cursor,
										   total_count = total_count)


	'''
	Make a cursor driven call to return the list of all friends
	The caller is responsible for handling the cursor value and looping to gather all of the data

	Parameters:	
		user_id – The twitter id of the user whose friends you are fetching. [Optional]
		screen_name – The twitter name of the user whose friends you are fetching. If not specified, defaults to the authenticated user. [Optional]
		cursor – Should be set to -1 for the initial call and then is used to control what result page Twitter returns.
		stringify_ids – if True then twitter will return the ids as strings instead of integers. [Optional]
		count – The number of user id’s to retrieve per API request. Please be aware that this might get you rate-limited if set to a small number. 
				By default Twitter will retrieve 5000 UIDs per call. [Optional]
	
	Returns:	
		next_cursor, previous_cursor, data sequence of twitter.User instances, one for each friend
	'''
	def get_friendids_paged(self,
							user_id = None,
							screen_name = None,
							cursor = -1,
							count = 5000,
							stringify_ids = False):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFriendIDsPaged(user_id = user_id,
												screen_name = screen_name,
												cursor = cursor,
												count = count,
												stringify_ids = stringify_ids)


	'''
	分页获取用户朋友id，如果超时则会休眠800s，然后返回朋友信息(参考 get_friendids_paged )
	'''
	def get_friendids_paged_sleep(self,
								  user_id = None,
								  screen_name = None,
								  cursor = -1,
								  stringify_ids = False,
								  count = 5000):

		wrapper_func = handle_exception(self.get_friendids_paged)
		friendids = wrapper_func(user_id = user_id,
								 screen_name = screen_name,
								 cursor = cursor,
								 stringify_ids = stringify_ids,
								 count = count)

		return friendids
	

	'''
	Fetch the sequence of twitter.User instances, one for each friend.
	If both user_id and screen_name are specified, this call will return the followers of the user specified by screen_name, 
	however this behavior is undocumented by Twitter and may change without warning.

	Parameters:	
		user_id – The twitter id of the user whose friends you are fetching. [Optional]
		screen_name – The twitter name of the user whose friends you are fetching. [Optional]
		cursor – Should be set to -1 for the initial call and then is used to control what result page Twitter returns.
		total_count – The upper bound of number of users to return.
		skip_status – If True the statuses will not be returned in the user items. [Optional]
		include_user_entities – When True, the user entities will be included. [Optional]
	
	Returns:	
		A sequence of twitter.User instances, one for each friend
	'''
	def get_friends(self,
					user_id = None,
					screen_name = None,
					cursor = None,
					total_count = 2500,
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
	分页获取用户朋友信息(参考 get_friends )
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
	# def get_all_friendids(self, 
	# 					  user_id = None, 
	# 					  screen_name = None):

	# 	cursor = -1
	# 	while cursor != 0:
	# 		out = self.get_friendids_paged_sleep(user_id = user_id,
	# 											 screen_name = screen_name, 
	# 											 cursor = cursor, 
	# 											 count = 5000)
	# 		if not out:
	# 			return None

	# 		cursor = out[0]
	# 		friend_list = out[2]
		

	'''
	Returns a list of twitter user id’s for every person that is following the specified user.

	Parameters:
		user_id – The id of the user to retrieve the id list for. [Optional]
		screen_name – The screen_name of the user to retrieve the id list for. [Optional]
		cursor – Specifies the Twitter API Cursor location to start at. Note: there are pagination limits. [Optional]
		total_count – The total amount of UIDs to retrieve. Good if the account has many followers and you don’t want to get rate limited. 

	Returns:
		A list of integers, one for each user id.
	'''
	def get_followerids(self,
						user_id = None,
						screen_name = None,
						cursor = None,
						total_count = 60000):

		if user_id == None and screen_name == None:
			return None

		return self.get_api().GetFollowerIDs(user_id = user_id,
											 screen_name = screen_name,
											 cursor = cursor,
											 total_count = total_count)


	'''
	Make a cursor driven call to return a list of one page followers.
	The caller is responsible for handling the cursor value and looping to gather all of the data

	Parameters:	
		user_id – The twitter id of the user whose followers you are fetching. [Optional]
		screen_name – The twitter name of the user whose followers you are fetching. [Optional]
		cursor – Should be set to -1 for the initial call and then is used to control what result page Twitter returns.
		stringify_ids – if True then twitter will return the ids as strings instead of integers. [Optional]
		count – The number of user id’s to retrieve per API request. Please be aware that this might get you rate-limited if set to a small number. 
				By default Twitter will retrieve 5000 UIDs per call. [Optional]
	
	Returns:	
		next_cursor, previous_cursor, data sequence of user ids, one for each follower
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
	分页获取用户粉丝id，如果超时则会休眠800s，然后返回粉丝信息（参考 get_followerids_page ）
	'''
	def get_followerids_paged_sleep(self,
									user_id = None,
									screen_name = None,
									cursor = -1,
									stringify_ids = False,
									count = 5000):

		wrapper_func = handle_exception(self.get_followerids_paged)
		followerids = wrapper_func(user_id = user_id,
								   screen_name = screen_name,
								   cursor = cursor,
								   stringify_ids = stringify_ids,
								   count = count)

		return followerids


	'''
	Fetch the sequence of twitter.User instances, one for each follower.
	If both user_id and screen_name are specified, this call will return the followers of the user specified by screen_name, 
	however this behavior is undocumented by Twitter and may change without warning.

	Parameters:	
		user_id – The twitter id of the user whose followers you are fetching. [Optional]
		screen_name – The twitter name of the user whose followers you are fetching. [Optional]
		cursor – Should be set to -1 for the initial call and then is used to control what result page Twitter returns.
		total_count – The upper bound of number of users to return, defaults to None.
		skip_status – If True the statuses will not be returned in the user items. [Optional]
		include_user_entities – When True, the user entities will be included. [Optional]

	Returns:	
		A sequence of twitter.User instances, one for each follower
	'''
	def get_followers(self,
					  user_id = None,
					  screen_name = None,
					  cursor = None,
					  total_count = 2500,
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
	分页获取用户粉丝信息（参考 get_followers ）
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
	# def get_all_followersids(self, 
	# 						 user_id = None, 
	# 						 screen_name = None):

	# 	cursor = -1
	# 	while cursor != 0:
	# 		out = self.get_followerids_paged_sleep(user_id = user_id,
	# 											   screen_name = screen_name, 
	# 											   cursor = cursor, 
	# 											   count = 5000)
	# 		if not out:
	# 			return None

	# 		cursor = out[0]
	# 		follower_list = out[2]


if __name__ == '__main__':
	rc = RelationCrawler()
	print rc.get_followers_paged(screen_name='mrmarcohan')