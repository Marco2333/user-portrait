# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-30 14:16:44 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-30 14:16:44 
'''
import re
import nltk
import MySQLdb

from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient

stop_words = set()

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

	for word in words:
		if len(word) > 2 and word.isalpha() and word not in stop_words:
			word_list.append(word)

	try:
		pos = nltk.pos_tag(word_list)
	except Exception as e:
		print e
		pos = []

 	res = set()
	lemmatizer = WordNetLemmatizer()

	for w in pos:
		if w[1][0] == 'N':
			word = lemmatizer.lemmatize(w[0])  # 词形归并
			if word not in stop_words:
				res.add(word)

		elif w[1][0] == 'J':
			word = lemmatizer.lemmatize(w[0], 'a')  # 词形归并
			if word not in stop_words:
				res.add(word)

		elif w[1][0] == 'V':
			word = lemmatizer.lemmatize(w[0], 'v')  # 词形归并
			if word not in stop_words:
				res.add(word)

	if len(res) < 3:
		return [None, None]


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
	
	return res




if __name__ == '__main__':
	client = MongoClient('127.0.0.1', 27017)
	db = client['dump']
	a = db['typical_temp'].find_one({'screen_name': 'BarackObama'}, {'tweets': 1})

	text = ''
	for item in a['tweets'][1:3]:
		text += item['text'] + ' '

	# generate_sentiment_dict()
	preprocess(text)
	# read_stop_words()
	# print stop_words