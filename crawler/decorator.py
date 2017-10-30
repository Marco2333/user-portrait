# -*- coding:utf-8 -*-

import time

from twitter import error
from api import API_COUNT

'''
生成装饰器
'''
def generate_decorator(sleep_time = 700):

	# 处理Twitter异常装饰器
	def handle_exception(func):
		def wrapper(*args, **kw):
			sleep_count = 0

			while True:
				try:
					return func(*args, **kw)
				except error.TwitterError as te:
					try:
						if te.message[0]['code'] == 88:
							sleep_count += 1

							if sleep_count >= API_COUNT:
								print "sleeping..."
								sleep_count = 0
								time.sleep(sleep_time)
							continue

						else:
							print te
							return None
					except Exception as ee:
						print ee
						return None

				except Exception as e:
					print e
					return None

		return wrapper

	return handle_exception