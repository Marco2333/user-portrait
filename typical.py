# -*- coding: utf-8 -*- 
from app.database import MongoDB
from app.portrayal.career_classify import training, classify
from app.portrayal.tools import preprocess
from app.portrayal.career_classify import preprocess as training_preprocess

def classify_career():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find({'category': 'Education'})

	n = 0
	for user in users:
		print user['screen_name']
		tweets = user['tweets']

		text = user['description']
		for tweet in tweets:
			text += ' ' + tweet['text']
		
		res = classify.classify(preprocess.preprocess(text))

		print res
		if res[0] == user['category']:
			n += 1
		
	print n

if __name__ == "__main__":
	classify_career()
	# training.training()
	# training_preprocess.delete_ambiguity()