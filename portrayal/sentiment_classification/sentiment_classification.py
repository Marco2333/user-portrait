# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-30 14:16:44 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-30 14:16:44 
'''
import re
import nltk
import time
import datetime
import MySQLdb

from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient

stop_words = set()

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


def read_stop_words():
	f = open("f:\python\user-portrait\portrayal\sentiment_classification\stop_words.txt", "r")  
	for line in f:  
	    stop_words.add(line[0 : -1])

	f.close()  

def data_cleaning(text):
	# clear @/#/链接/RT
	return re.sub(r'^RT @\w+:|@\w+|#|(ht|f)tp[^\s]+', "", text)


def preprocess(text):
	read_stop_words()

	text = text.lower()
	text = re.sub(r'new york',"NewYork", text)

	word_list = []
	words = word_tokenize(text)

	try:
		pos = nltk.pos_tag(words)
	except Exception as e:
		print e
		pos = []

	for word in pos:
		if word[0].isalpha() and word[0] not in stop_words:
			word_list.append(word)

 	res = []
	# lemmatizer = WordNetLemmatizer()
	for word in word_list:
		if word[1][0] == 'N':
			# word = lemmatizer.lemmatize(word[0])  # 词形归并
			res.append((word[0], 'n'))

		elif word[1][0] == 'J':
			# word = lemmatizer.lemmatize(word[0], 'a')  # 词形归并
			res.append((word[0], 'a'))

		elif word[1][0] == 'V':
			# word = lemmatizer.lemmatize(word[0], 'v')  # 词形归并
			res.append((word[0], 'v'))

		elif word[1][0] == 'R':
			# word = lemmatizer.lemmatize(word[0], 'r')  # 词形归并
			res.append((word[0], 'r'))

	return res


def calc_sentiment_sequence(tweets):
	sentiment_dict = generate_sentiment_dict()
	tweets_list = split_tweets_by_month(tweets, 1)

	res = []
	# t_s = 0
	for tts in tweets_list:
		text = ''
		score = 0

		for tweet in tts:
			text += tweet['text'] + ' '
		
		word_list = preprocess(text)
		for word in word_list:
			key = word[0] + '#' + word[1]
			if key in sentiment_dict:
				score += sentiment_dict[key]
		
		# t_s += score
				
		res.append(score)

	# print t_s

	return res if len(res) < 5 else res[0 : -1]


def generate_sentiment_dict():
	sentiment_dict = {}
	file = open('f:\python\user-portrait\portrayal\sentiment_classification\SentiWordNet.txt')

	data = []
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break

		for line in lines:
			if line.strip().startswith("#"):
				continue
			else:
				data = line.split("\t")
				if len(data) != 6:
					print line
					print 'invalid data'
					continue

			word_type = data[0]
			synset_score = float(data[2]) - float(data[3])
			syn_terms_list = data[4].split(" ")

			for w in syn_terms_list:
				term_and_num = w.split("#")
				syn_term = term_and_num[0] + "#" + word_type
				term_num = int(term_and_num[1])

				if sentiment_dict.has_key(syn_term):
					sentiment_dict[syn_term].append((term_num, synset_score))
				
				else:
					sentiment_dict[syn_term] = []
					sentiment_dict[syn_term].append((term_num, synset_score))
	
	res = {}
	for key in sentiment_dict:
		score_sum = 0
		count = 0
		for word_tuple in sentiment_dict[key]:
			score_sum += word_tuple[1] * word_tuple[0]
			count += word_tuple[0]
		
		if score_sum / count != 0:
			res[key] = score_sum / count
	
	count = 0
	for item in res:
		if abs(res[item]) > 0.4:
			count += 1
			print item

	print count
	return res




if __name__ == '__main__':
	# client = MongoClient('127.0.0.1', 27017)
	# db = client['dump']
	# a = db['typical_temp'].find_one({'screen_name': 'philstockworld'}, {'tweets': 1})

	# calc_sentiment_sequence(a['tweets'])

	generate_sentiment_dict()
	# text = ''
	# for item in a['tweets']:
	# 	print item['text']
	# 	text += item['text'] + ' '

	# generate_sentiment_dict()
	# preprocess(text)
	# read_stop_words()
	# print stop_words