# -*- coding:utf-8 -*-
from twitter import Api
from config import APP_INFO

API_LIST = []
API_COUNT = len(APP_INFO)

for i in range(API_COUNT):
	API_LIST.append(Api(consumer_key = APP_INFO[i]['consumer_key'],
					  consumer_secret = APP_INFO[i]['consumer_secret'],
					  access_token_key = APP_INFO[i]['access_token_key'],
					  access_token_secret = APP_INFO[i]['access_token_secret']))

class Api:
	def __init__(self):
		self.api_index = 0

	'''
	获取 twitter app，每次调用返回一个新的 app
	'''
	def get_api(self):
		api_index = self.api_index
		api_index = (api_index + 1) % API_COUNT
		self.api_index = api_index

		return API_LIST[api_index]