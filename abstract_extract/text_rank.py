# -*- coding: utf-8 -*-    
import re
import time
import math
import nltk
import MySQLdb
import mpi4py.MPI as MPI

from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = {}

'''
读取停用词
'''
def read_stop_words():
	f = open("../data/stop_word.txt", "r")  
	for line in f:  
	    stop_words[line[0 : -1]] = 1

	f.close()  

'''
步骤一：数据预处理
分词-》去除停用词-》词性标注
'''
def preprocess(text):
	# clear @/#/http
	text = re.sub(r'[@|#][\d|\w|_]+|http[\w|:|.|/|\d]+|RT(.)+?:(.)+?(:.)?|\n',"",text)
	text = re.sub(r'new york|NEW YORK|New York',"NewYork",text)
	text = text.strip()
	if text == None or len(text) < 11:
		return [None, None] 

	_text = text
	text = text.lower()
	words_list = []
	words = word_tokenize(text),
	words = words[0]

	for word in words:
		if word not in stop_words:
			if len(word) > 2 and word.isalpha():
				words_list.append(word)

	if len(words_list) < 3:
		return [None, None] 

	try:
		pos = nltk.pos_tag(words_list)
	except Exception as e:
		print e
		pos = []

 	res = set()
	lemmatizer = WordNetLemmatizer()

	for w in pos:
		if w[1][0] == 'N':
			word = lemmatizer.lemmatize(w[0])  # 词形归并
			if word not in stop_words and len(word) < 15:
				res.add(word)

		elif w[1][0] == 'J':
			word = lemmatizer.lemmatize(w[0], 'a')  # 词形归并
			if word not in stop_words and len(word) < 15:
				res.add(word)

		elif w[1][0] == 'V':
			word = lemmatizer.lemmatize(w[0], 'v')  # 词形归并
			if word not in stop_words and len(word) < 15:
				res.add(word)

	if len(res) < 3:
		return [None, None] 

	return [res, _text]

'''
计算所有句子的相似度和共现窗口
'''
def calculate_similarity_cowindow(tweet_list):
	t1 = time.clock()
	length = len(tweet_list)
	similarity = [[0 for _ in range(length)] for _ in range(length)]
	co_window = [[] for _ in range(length)]

	for i in range(length):
		for j in range(i + 1, length):
			res = 0
			res = calc_similarity_sentence(tweet_list[i], tweet_list[j])
			if res >= 0.2:
				co_window[i].append(j)
				co_window[j].append(i)
				similarity[i][j] = res
				similarity[j][i] = res

	return [similarity, co_window]

'''
计算两个句子的相似度
'''
def calc_similarity_sentence(s1, s2):
	return len(s1 & s2) * 1.0 / (math.log(len(s1), 2) + math.log(len(s2), 2))

'''
计算共现窗口
'''
def get_tweet_cooccurrence1(tweet_list):
	co_window = []
	co_window_width = 10

	length = len(tweet_list)
	for index in range(length):
		lower_bound = (index - co_window_width) > 0 and index - co_window_width or 0
		upper_bound = (index + co_window_width) < length and index + co_window_width or length - 1  # 包含upper_bound

		co_window.append([lower_bound, upper_bound]) 

	return co_window

def get_tweet_cooccurrence(similarity):
	co_window = []
	# co_window_width = 10
	length = len(similarity)
	for index in range(length):
		win = []
		for j in range(length):
			if similarity[index][j] != 0:
				win.append(j)

		co_window.append(win)

	return co_window

'''
计算得分最高的句子作为摘要
'''
def get_topk_sentence(similarity, co_window, count = -1):
	max_iter = 1000000
	pre_item_score = [1] * len(similarity)

	i = 0
	d = 0.85
	length = len(similarity)

	while i < max_iter:
		i += 1
		item_score = {}

		for index in range(length):
			sum = 0
			for j in co_window[index]:
				denominator = 0
				for k in co_window[j]:
					denominator += similarity[k][j]

				sum += (similarity[index][j] * 1.0 / denominator) * pre_item_score[j]
			
			item_score[index] = d * sum + (1 - d)
			
		if calc_differ(pre_item_score, item_score) < 0.1:
			# print i
			break

		pre_item_score = item_score

	res = sorted(item_score.iteritems(), key = lambda v: v[1], reverse = True)

	if count == -1:
		return res

	return res[0 : count]

'''
计算两次迭代的得分差，判断终止条件
'''
def calc_differ(score1, score2):
	res = 0
	length = len(score1)

	for i in range(length):
		res += abs(score1[i] - score2[i])

	return res

'''
获得用户信息
'''
def get_user_info():
	db = MySQLdb.connect('127.0.0.1', 'root', '283319', 'twitter')
	db.set_character_set('utf8')
	cursor = db.cursor()

	sql = "select user_id from user_famous limit 1000"

	try:
		cursor.execute(sql)
		user_list = cursor.fetchall()
		user_list = map(lambda x: x[0], user_list)
	except Exception as e:
		print e

	return user_list

'''
执行
'''
def exe_process(tweet_list, k = -1):
	tweets_tp1 = []
	tweets_tp2 = []

	for tweet in tweet_list:
		out = preprocess(tweet)
		if out[0]:
			tweets_tp1.append(out[0])
			tweets_tp2.append(out[1])

	res = calculate_similarity_cowindow(tweets_tp1)
	similarity = res[0]
	co_window = res[1]

	out = get_topk_sentence(similarity, co_window, k)

	res = []
	for item in out:
		res.append(tweets_tp2[item[0]])
		
	return res


def main():
	read_stop_words()
	data = get_user_info()
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']
	collect = db['tweets']

	db = MySQLdb.connect('127.0.0.1', 'root', '283319', 'twitter')
	db.set_character_set('utf8')
	# db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="283319", db="twitter",  charset="utf8")
	cursor = db.cursor()

	for user_id in data:
		text = ""
		tweets = collect.find({'user_id': long(user_id)}, {"text": 1})
		tweet_list = []
		for tt in tweets:
			tweet_list.append(tt['text'])

		abstract = exe_process(tweet_list, 6)
		
		abs_res = ""
		for sentence in abstract:
			abs_res += sentence + "\n"

		sql = '''update user_interest1 set abstract = '%s' where user_id = '%s' ''' % (abs_res.replace("'","\\'").replace('"','\\"'), user_id)
		sql = sql.encode("utf-8").decode("latin1")
		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print e


if __name__ == '__main__':
	start = time.clock()
	main()
	end = time.clock()
	print end - start