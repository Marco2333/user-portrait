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

from .. tools.function import split_tweets_same_time, calc_time_differ


'''
参数计算
'''
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


'''
参数计算：只返回原创推文数和转发推文数
'''
def calc_parameters_4sequence(tweets):
	origin_count = rt_count = 0  # 原创推文和转发推文

	if len(tweets) == 0:
		return

	for tweet in tweets:
		if re.match(r"^RT @\w+", tweet["text"]) != None:
			rt_count += 1
		   
		else:
			origin_count += 1

	return origin_count, rt_count


'''
计算活跃度
'''
def calc_activity(origin_count, rt_count, time_span):
	time_span = time_span if time_span else 1
	rate =  1000.0 / time_span
	total = 0.65 * math.log(origin_count * rate + 1) + 0.35 * math.log(rt_count * rate + 1)

	return total


'''
活跃度序列计算
参数：
	period：时间跨度，默认为 1，表示每一个月计算一次活跃度
'''
def calc_activity_sequence(tweets, period = 1):
	tweets_list = split_tweets_same_time(tweets, 1)

	res = []
	for tts in tweets_list:
		origin_count, rt_count = calc_parameters_4sequence(tts)

		activity = calc_activity(origin_count, rt_count, period * 30)
		res.append(activity)

	return res


'''
计算推文影响力
'''
def calc_tweet_influence(origin_retweet_count, origin_retweet_average, origin_retweet_max, \
							  origin_favorite_count, origin_favorite_average, origin_favorite_max):
	retweet_rate = 0.45 * math.log(origin_retweet_count + 1) + 0.35 * math.log(origin_retweet_average + 1) + 0.2 * math.log(origin_retweet_max + 1)
	favorite_rate = 0.45 * math.log(origin_favorite_count + 1) + 0.35 * math.log(origin_favorite_average + 1) + 0.2 * math.log(origin_favorite_max + 1)

	return 0.6 * retweet_rate + 0.4 * favorite_rate


'''
计算粉丝影响力
'''
def calc_follower_influence(followers_count):
	return math.log(followers_count + 1)


'''
影响力计算
'''
def calculate_influence(followers_count, tweets):
	tweet_start_time, tweet_end_time, origin_count, rt_count, origin_retweet_count, origin_retweet_average, \
	origin_retweet_max, origin_favorite_count, origin_favorite_average, origin_favorite_max = calc_parameters(tweets)

	time_span = calc_time_differ(tweet_start_time, tweet_end_time)

	activity = calc_activity(origin_count, rt_count, time_span)
	tweet_influence = calc_tweet_influence(origin_retweet_count, origin_retweet_average, origin_retweet_max, \
												origin_favorite_count, origin_favorite_average, origin_favorite_max)

	follower_influence = calc_follower_influence(followers_count)

	return (0.5 * tweet_influence + 0.2 * activity + 0.3 * follower_influence) * 10, activity