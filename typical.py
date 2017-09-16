# -*- coding: utf-8 -*- 
from app.database import MongoDB
# import nltk
import re
# from nltk.tokenize import word_tokenize
# # from app.portrayal.career_classify import training, classify
# # from app.portrayal.tools import preprocess
# # from app.portrayal.career_classify import preprocess as training_preprocess
# from app.portrayal.sentiment_classify import sentiment_classify
from app.portrayal.interest_extract import interest_extract
# from app.portrayal.tools import preprocess
# from app.portrayal.user_profile import user_profile
from app.portrayal.config import PROJECT_PATH

def classify_career():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find({'category': 'Bloomberg'})

	err_dict = {}
	n = 0
	for user in users:
		print user['screen_name']
		tweets = user['tweets']

		text = user['description']
		for tweet in tweets:
			text += ' ' + tweet['text']
		
		text = preprocess.preprocess(text)

		res = classify.exe_classify(text)
			
		if err_dict.has_key(res[0]):
			err_dict[res[0]] += 1
		else:
			err_dict[res[0]] = 1

		if res[0] == user['category']:
			n += 1

	print err_dict	
	print n

def extract_interset():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find({'screen_name': 'WWEDanielBryan'})
	
	for u in users:
		text = ''
		for item in u['tweets']:
			text += item['text'] + ' '

		try:
			tags = interest_extract.extract_tags(text, u['description'])
		except Exception as e:
			print u['_id']
			print e
			continue
	
		db['typical'].update({'_id': u['_id']}, {"$set": {"interest_tags": tags}})


def profile():
	db = MongoDB().connect()
	users = db['typical'].find().skip(3).limit(5)
	
	for user in users:
		temp = user_profile(user)
		del temp['tweets']
		print temp


def calc_sentiment():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find().skip(3).limit(1)

	for user in users:
		print sentiment_classify.exe_sentiment_classify(user['tweets'])

if __name__ == "__main__":
	# calc_sentiment()
	# sentiment_dict.test()

	# file = open(PROJECT_PATH + "portrayal/sentiment_classify/data/positive.txt").read()
	# print sentiment_classify.exe_sentiment_classify(tweets)

	extract_interset()
	
	# db = MongoDB().connect('dump')
	# user = db['typical_temp'].find_one({'screen_name': 'David_Cameron'})

	# for t in user['tweets']:
	# 	print t['text']