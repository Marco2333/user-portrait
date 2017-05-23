# -*- coding: utf-8 -*-    
import re
import time
import nltk
import MySQLdb
import mpi4py.MPI as MPI

from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

twitter_stop_words = ["after", "be", "do", "find", "new", "take", "know", "need", "first", "good", "use", "big", "come", "see", "great", "more", "look", "make", "get","have", "from","TO","to","https","RT","URL","in","re","thank","thanks","today","yesterday","tomorrow","night","tonight","day","year","last","oh","yeah","amp"]

stop_words = {}

def read_stop_words():
	f = open("stop_word.txt", "r")  
	for line in f:  
	    stop_words[line[0 : -1]] = 1

	f.close()  

'''
步骤一：数据预处理
分词-》去除停用词-》词性标注
'''
def preprocess(text):
	# clear @/#/http
	text = re.sub(r'[@|#][\d|\w|_]+|http[\w|:|.|/|\d]+',"",text)
	if text == "" or text == None:
		return [] 

	text = text.lower()
	words_list = []
	words = word_tokenize(text),
	words = words[0]

	for word in words:
		# if word not in (stopwords.words("english") and twitter_stop_words):  # clear stopwords
		if word not in stop_words:
			if len(word) > 2 and word.isalpha():
				words_list.append(word)
	try:
		pos = nltk.pos_tag(words_list)
	except Exception as e:
		print e
		pos = []

 	res = []
	lemmatizer = WordNetLemmatizer()
	# single_pattern = ["N", "J", "V"]

	for w in pos:
		if w[1][0] == 'N':
			word = lemmatizer.lemmatize(w[0])  # 词形归并
			if word not in stop_words and len(word) < 13:
				res.append(word)

			# res.append((word, w[1]))

		elif w[1][0] == 'J':
			word = lemmatizer.lemmatize(w[0], 'a')  # 词形归并
			if word not in stop_words and len(word) < 13:
				res.append(word)

			# res.append((word, w[1]))

		elif w[1][0] == 'V':
			word = lemmatizer.lemmatize(w[0], 'v')  # 词形归并
			if word not in stop_words and len(word) < 13:
				res.append(word)

			# res.append((word, w[1]))

	return res


def get_word_cooccurrence(word_list):
	co_window = {}
	co_window_width = 6

	for w in word_list:
		co_window[w] = None

	length = len(word_list)
	for index in range(length):
		w = word_list[index]
		related_set = None
		if not co_window[w]:
			related_set = set()
			co_window[w] = related_set
		else:
			related_set = co_window[w]

		lower_bound = (index - co_window_width) > 0 and index - co_window_width or 0
		upper_bound = (index + co_window_width) < length and index + co_window_width or length - 1  # 包含upper_bound

		i = lower_bound
		while i <= upper_bound:
			related_set.add(word_list[i])
			i += 1

	for w in co_window:
		co_window[w].remove(w)

	return co_window


def get_topk_word(co_window, k = -1):
	max_iter = 1000000
	pre_item_score = {}

	for w in co_window:
		pre_item_score[w] = 1

	i = 0
	d = 0.85
	while i < max_iter:
		i += 1
		item_score = {}

		for w in co_window:
			sum = 0
			for item in co_window[w]:
				sum += (1.0 / len(co_window[item])) * pre_item_score[item]
				
			item_score[w] = d * sum + (1 - d)
		
		if calc_differ(pre_item_score, item_score) < 0.1:
			break

		pre_item_score =  item_score

	res = sorted(item_score.iteritems(), key = lambda v: v[1], reverse = True)

	if k == -1:
		return res

	return res[0 : k]


def calc_differ(score1, score2):
	res = 0
	for item in score1:
		res += abs(score1[item] - score2[item])

	return res


def get_user_info():
	db = MySQLdb.connect('127.0.0.1', 'root', '283319', 'twitter')
	db.set_character_set('utf8')
	cursor = db.cursor()

	sql = "select user_id from user_famous limit 4"

	try:
		cursor.execute(sql)
		user_list = cursor.fetchall()
		user_list = map(lambda x: x[0], user_list)
	except Exception as e:
		print e

	return user_list


def data_distribution():
	comm = MPI.COMM_WORLD
	comm_rank = comm.Get_rank()
	comm_size = comm.Get_size()
	# print comm_size
	data = []
	
	if comm_rank == 0:
		user_list = get_user_info()
		size_per_node = len(user_list) / comm_size

		for i in range(1, comm_size):
			if i == comm_size - 1:
				comm.send(user_list[i * size_per_node : ], dest = i)
			else:
				comm.send(user_list[i * size_per_node : (i + 1) * size_per_node], dest = i)

		data = user_list[0 : size_per_node]

	else:
		data = comm.recv(source = 0)

	return data


def exe_process(text, k = -1):
	pos = preprocess(text)
	coo = get_word_cooccurrence(pos)
	res = get_topk_word(coo, k)

	return res


def main():
	read_stop_words()
	data = data_distribution()
	
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']
	collect = db['tweets']

	db = MySQLdb.connect('127.0.0.1', 'root', '283319', 'twitter')
	db.set_character_set('utf8')
	cursor = db.cursor()

	for user_id in data:
		text = ""
		tweets = collect.find({'user_id': long(user_id)}, {"text": 1})

		for tt in tweets:
			text += tt['text']

		topk = exe_process(text, 30)
		text = ""
		for w in topk:
			text += w[0] + " "

		sql = "insert into user_interest(user_id, user_interest) values('%s', '%s')" % (user_id, text)
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