# -*- coding: utf-8 -*- 
# from app.database import MongoDB
# import nltk
# import re
# from nltk.tokenize import word_tokenize
# # from app.portrayal.career_classify import training, classify
# # from app.portrayal.tools import preprocess
# # from app.portrayal.career_classify import preprocess as training_preprocess
from app.portrayal.sentiment_classify import sentiment_dict
# from app.portrayal.interest_extract import interest_extract
# from app.portrayal.tools import preprocess
# from app.portrayal.user_profile import user_profile


def classify_career():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find({'category': 'Education'})

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


def profile():
	db = MongoDB().connect()
	users = db['typical'].find().limit(1)

	for user in users:
		temp = user_profile(user)
		del temp['tweets']
		print temp


if __name__ == "__main__":
	# extract_interset()
	# profile()
	# print nltk.word_tokenize("I h2ppy ha-hha hi i love lu")
	
	# print re.sub(r"(\w)\1{2,}", r"\1", "I’m in a hurrryyyyy")
	# print "I’m in a hurrryyyyy".replace("(.)\1{1,}", "\1\1")
	sentiment_dict.test()