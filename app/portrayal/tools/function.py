# -*- coding: utf-8 -*-
import time
import datetime

from .. config import PROJECT_PATH

slang = None
stop_words = None

'''
读取停用词
'''
def get_stop_words(file_path = PROJECT_PATH + "portrayal/resource/stop_words.txt"):
	global stop_words

	if not stop_words:
		stop_words = set()
	else:
		return stop_words

	file = open(file_path, "r")  
	for line in file:  
	    stop_words.add(line[0 : -1])

	file.close()  

	return stop_words


'''
读取俚语
'''
def get_slang(file_path = PROJECT_PATH + "portrayal/resource/slang.txt"):
	global slang

	if not slang:
		slang = {}
	else:
		return slang

	file = open(file_path, "r")  
	for line in file:  
		l_l = line.split(":")
		slang[l_l[0].strip()] = l_l[1]

	file.close()  

	return slang


'''
计算两个时间相差的天数
'''
def calc_time_differ(t1, t2):
	t1 = time.strptime(t1, "%Y-%m-%d %H:%M:%S")
	t2 = time.strptime(t2, "%Y-%m-%d %H:%M:%S")
	t1 = datetime.datetime(t1[0], t1[1], t1[2], t1[3], t1[4], t1[5])
	t2 = datetime.datetime(t2[0], t2[1], t2[2], t2[3], t2[4], t2[5])

	return abs((t2 - t1).days)


'''
将推文分割为按月为单位的推文列表
返回：
	二维推文列表
'''
def split_tweets_same_time(tweets = [], period = 1):
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

	return tweets_list if len(tweets_list[-1]) > 40 else tweets_list[0 : -1]


def split_tweets_same_count(tweets = [], count = 80):
	count = count if count <= 150 else 150
	count = count if count >= 60 else 60

	if len(tweets) < 1200:
		count = 60

	tts = []
	tweets_list = []

	i = 0
	for tweet in tweets:
		i += 1
		tts.append(tweet)

		if i > count:
			tweets_list.append(tts)
			tts = []
			i = 0

	if len(tts) > 40:
		tweets_list.append(tts)

	return tweets_list