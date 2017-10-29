# -*- coding: utf-8 -*- 
import re
# import nltk

from crawler.database import MongoDB
from portrayal.config import PROJECT_PATH
# from nltk.tokenize import word_tokenize
# from portrayal.tools import preprocess
# from portrayal.career_classify import training, classify
from portrayal.interest_extract import interest_extract
from portrayal.sentiment_classify import sentiment_classify
# from portrayal.tools import preprocess
# from portrayal.user_profile import user_profile

'''
职业领域分类
'''
def classify_career():
	db = MongoDB().connect()
	users = db['typical'].find()

	n = 0
	err_dict = {}
	for user in users:
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


'''
兴趣标签导出
'''
def extract_interset():
	db = MongoDB().connect()
	users = db['typical'].find()
	
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


'''
心理状态
'''
def calc_sentiment():
	db = MongoDB().connect()
	users = db['typical'].find()

	for user in users:
		try:
			final_sentiment, psy_with_time1, psy_with_time2, psy_with_count1, psy_with_count2 = sentiment_classify.exe_sentiment_classify(user['tweets'])
		except Exception as e:
			print user['_id']
			print e
			continue

		db['typical'].update({'_id': user['_id']}, {"$set": {"psy": final_sentiment, "psy_with_time1": psy_with_time1, "psy_with_time2": psy_with_time2, "psy_with_count1": psy_with_count1, "psy_with_count2": psy_with_count2}}) 


if __name__ == "__main__":
	calc_sentiment()