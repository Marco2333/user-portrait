# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-29 15:48:56 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-29 15:48:56 
'''
import re
import math
import time
import datetime
from pymongo import MongoClient

def calc_time_differ(t1, t2):
	t1 = time.strptime(t1, "%Y-%m-%d %H:%M:%S")
	t2 = time.strptime(t2, "%Y-%m-%d %H:%M:%S")
	t1 = datetime.datetime(t1[0], t1[1], t1[2], t1[3], t1[4], t1[5])
	t2 = datetime.datetime(t2[0], t2[1], t2[2], t2[3], t2[4], t2[5])

	return abs((t2 - t1).days)

def split_tweets_by_month(tweets = [], period = 1):
	threshold = period * 30
	
	if len(tweets) == 0:
		return

	start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[0]['created_at'].replace('+0000 ','')))
	start_time_temp = start_time

	tts = []
	tweets_list = []

	for tweet in tweets:
		time_temp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'].replace('+0000 ','')))
		
		if calc_time_differ(time_temp, start_time_temp) <= threshold:
			tts.append(tweet)
		else:
			start_time_temp = time_temp
			tweets_list.append(tts)
			tts = []
			tts.append(tweet)

	if len(tts) != 0:
		tweets_list.append(tts)

	return tweets_list

def calc_parameters(tweets):
	origin_count = rt_count = 0  # 原创推文和转发推文
	origin_retweet_count = origin_retweet_average = origin_retweet_max = 0  # 原创推文转发 总数、平均值、最大值
	origin_favorite_count = origin_favorite_average = origin_favorite_max = 0 # 原创推文点赞 总数、平均值、最大值

	if len(tweets) == 0:
		return

	tweet_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[0]['created_at'].replace('+0000 ','')))
	tweet_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[-1]['created_at'].replace('+0000 ','')))

	for tweet in tweets:
		# 转推
		if re.match(r"^RT @[\w|\d|_]+", tweet["text"]) != None:
			rt_count += 1
		   
		# 非转推
		else:
			retweet_count = tweet["retweet_count"]
			favorite_count = tweet["favorite_count"]

			origin_count += 1
			origin_retweet_count += retweet_count
			origin_favorite_count += favorite_count

			if retweet_count > origin_retweet_max:
				origin_retweet_max = retweet_count
			
			if favorite_count > origin_favorite_max:
				origin_favorite_max = favorite_count
		
	origin_retweet_average =  origin_retweet_count * 1.0 / origin_count if origin_count else 0
	origin_favorite_average =  origin_favorite_count * 1.0 / origin_count if origin_count else 0

	return tweet_start_time, tweet_end_time, origin_count, rt_count, origin_retweet_count, \
	origin_retweet_average, origin_retweet_max, origin_favorite_count, origin_favorite_average, origin_favorite_max

def calc_parameters_4sequence(tweets):
	origin_count = rt_count = 0  # 原创推文和转发推文

	if len(tweets) == 0:
		return

	tweet_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[0]['created_at'].replace('+0000 ','')))
	tweet_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[-1]['created_at'].replace('+0000 ','')))

	for tweet in tweets:
		if re.match(r"^RT @[\w|\d|_]+", tweet["text"]) != None:
			rt_count += 1
		   
		else:
			origin_count += 1

	return tweet_start_time, tweet_end_time, origin_count, rt_count

'''
计算活跃度
'''
def calc_activity(origin_count, rt_count, time_span):
	time_span = time_span if time_span else 1
	rate =  1000.0 / time_span
	total = 0.65 * math.log(origin_count * rate + 1) + 0.35 * math.log(rt_count * rate + 1)

	return total

def calc_activity_sequence(tweets, period = 1):
	tweets_list = split_tweets_by_month(tweets, 1)

	res = []
	for tts in tweets_list:
		print len(tts)
		tweet_start_time, tweet_end_time, origin_count, rt_count = calc_parameters_4sequence(tts)
		time_span = calc_time_differ(tweet_start_time, tweet_end_time)

		activity = calc_activity(origin_count, rt_count, time_span)
		res.append(activity)

	return res if len(res) < 5 else res[0 : -1]

def calc_tweet_influence(origin_retweet_count, origin_retweet_average, origin_retweet_max, \
							  origin_favorite_count, origin_favorite_average, origin_favorite_max):
	retweet_rate = 0.45 * math.log(origin_retweet_count + 1) + 0.35 * math.log(origin_retweet_average + 1) + 0.2 * math.log(origin_retweet_max + 1)
	favorite_rate = 0.45 * math.log(origin_favorite_count + 1) + 0.35 * math.log(origin_favorite_average + 1) + 0.2 * math.log(origin_favorite_max + 1)

	return 0.6 * retweet_rate + 0.4 * favorite_rate

def calc_follower_influence(followers_count):
	return math.log(followers_count + 1)

def calculate_influence(followers_count, tweets):
	tweet_start_time, tweet_end_time, origin_count, rt_count, origin_retweet_count, origin_retweet_average, \
	origin_retweet_max, origin_favorite_count, origin_favorite_average, origin_favorite_max = calc_parameters(tweets)

	time_span = calc_time_differ(tweet_start_time, tweet_end_time)

	activity = calc_activity(origin_count, rt_count, time_span)
	tweet_influence = calc_tweet_influence(origin_retweet_count, origin_retweet_average, origin_retweet_max, \
												origin_favorite_count, origin_favorite_average, origin_favorite_max)

	follower_influence = calc_follower_influence(followers_count)

	print activity, tweet_influence, follower_influence
	return (0.5 * tweet_influence + 0.2 * activity + 0.3 * follower_influence) * 10


if __name__ == '__main__':
	client = MongoClient('127.0.0.1', 27017)
	db = client['dump']
	a = db['typical_temp'].find_one({'screen_name': 'BarackObama'})

	print calc_activity_sequence(a['tweets'])