# -*- coding: utf-8 -*- 
from app.database import MongoDB
import nltk

from nltk.tokenize import word_tokenize
# from app.portrayal.career_classify import training, classify
# from app.portrayal.tools import preprocess
# from app.portrayal.career_classify import preprocess as training_preprocess

from app.portrayal.sentiment_classify import training as sentiment_training, sentiment_dict, sentiment_classify

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

		# print res
		if res[0] == user['category']:
			n += 1

	print err_dict	
	print n

if __name__ == "__main__":
	db = MongoDB().connect('dump')
	u = db['typical_temp'].find_one({"screen_name": 'SenTedCruz'}, {"tweets": 1})
	sentiment_classify.sentiment_with_time(u['tweets'])
	# print nltk.pos_tag(word_tokenize('i am boy'))