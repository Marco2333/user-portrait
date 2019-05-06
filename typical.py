# -*- coding: utf-8 -*-
import re
# import nltk

from crawler.database import MongoDB
# from portrayal.config import PROJECT_PATH
# from nltk.tokenize import word_tokenize
# from portrayal.tools import preprocess
# from portrayal.career_classify import training, classify
# from portrayal.interest_extract import interest_extract
# from portrayal.sentiment_classify import sentiment_classify
# from portrayal.sentiment_classify import sentiment_dict as sentiment_dict_classifier
# from portrayal.tools import preprocess
# from portrayal.user_profile import user_profile

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import spline



# graph = Neo4j().connect()

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


def calc_sentiment_score():
	sentiment_dict = dict(map(lambda (k,v): (k,int(v)),
						[ line.split('\t') for line in open("portrayal/sentiment_classify/data/sentiment_words1.txt") ]))

	db = MongoDB().connect()
	users = db['typical'].find({'screen_name': 'EP_Agriculture'}).limit(1)

	for user in users:
		final_sentiment, psy_with_time1, psy_with_time2, psy_with_count1, psy_with_count2 = sentiment_classify.exe_sentiment_classify(user['tweets'])
		# print tags
		db['typical'].update({'_id': user['_id']}, {"$set": {"psy": final_sentiment, "psy_with_time1": psy_with_time1, "psy_with_time2": psy_with_time2, "psy_with_count1": psy_with_count1, "psy_with_count2": psy_with_count2}}) 


def sentiment_dict_test():
	# sentiment_dict = dict(map(lambda (k,v): (k,int(v)),
	# 					[ line.split('\t') for line in open("portrayal/sentiment_classify/data/sentiment_words1.txt") ]))
	text = sentiment_classify.replace_emotion([{'text': 'hope the er isnt to busy today but the nice weather doesnt keep people healthy or safe', 'created_at': '1'}])
	print text
	print sentiment_dict_classifier.calc_sentiment_score(text)
	return
	n = 0
	tts = []
	total = 0
	wrong = 0
	for line in open("portrayal/sentiment_classify/data/positive.txt"):
		n += 1
		tts.append({'text': line})

		if n % 1 == 0:
			score = sentiment_dict_classifier.calc_sentiment_score(tts)
			total += 1
			if score < 0:
				wrong += 1
				# print score
				# if wrong == 7:
				# 	print tts
				# 	break
			tts = []
	
	print wrong
	print total


def update_user_category():
	db = MongoDB().connect()
	users = db['typical'].find({}, {'_id': 1, 'screen_name': 1, 'category': 1, 'category_score': 1})

	count = 0
	category_name = ['Politics', 'Religion', 'Military', 'Economy', 'Technology', 'Education', 'Agriculture', 'Entertainment', 'Sports']

	users_temp = []

	for item in users:
		sorted_list = sorted(item['category_score'].iteritems(), key = lambda asd:asd[1], reverse = True)

		if sorted_list[0][1] > 2 * sorted_list[1][1] or sorted_list[0][1] - sorted_list[1][1] > 50:
			if sorted_list[0][0] != item['category']:
				count += 1
			continue

		score_differ = (2 * sorted_list[0][1] - sorted_list[1][1] - sorted_list[-1][1]) / 2

		relation_dict = {
			sorted_list[0][0]: 0,
			sorted_list[1][0]: 0,
			sorted_list[2][0]: 0,
			sorted_list[3][0]: 0
		}
		# for name in category_name:
		# 	relation_dict[name] = 0

		cql = '''MATCH(a{user_id:%s})-[:following]->(f) return distinct f.user_id as user_id''' % (item['_id'])
		res = graph.data(cql)

		for f in res:
			user = db['typical'].find_one({'_id': f['user_id']}, {'category_score': 1})
			category_score = user['category_score']
			max_category = max(category_score, key = lambda x: category_score[x])
			
			if max_category in relation_dict:
				relation_dict[max_category] += 1

		cql = '''MATCH(a{user_id:%s})<-[:following]-(f) return distinct f.user_id as user_id''' % (item['_id'])
		res = graph.data(cql)

		for f in res:
			user = db['typical'].find_one({'_id': f['user_id']}, {'category_score': 1})
			category_score = user['category_score']
			max_category = max(category_score, key = lambda x: category_score[x])

			if max_category in relation_dict:
				relation_dict[max_category] += 1
		
		relation_total = 0

		for ri in relation_dict:
			relation_total += relation_dict[ri]

		if relation_total < 10:
			if sorted_list[0][0] != item['category']:
				count += 1
			continue

		for ri in relation_dict:
			item['category_score'][ri] += round(score_differ * relation_dict[ri] / relation_total, 2)
		
		users_temp.append({'_id':item['_id'], "category_score": item['category_score']})

		s1 = sorted_list[0][0]

		sorted_list = sorted(item['category_score'].iteritems(), key = lambda asd:asd[1], reverse = True)

		# if sorted_list[0][0] == item['category'] and s1 != item['category']:
		# 	print item['screen_name']

		if sorted_list[0][0] != item['category']:
			count += 1
		
		print count
	
	for item in users_temp:
		db['typical'].update({'_id': item['_id']}, {"$set": {"category_score": item['category_score']}}) 





if __name__ == "__main__":
	# update_user_category()
	# db = MongoDB().connect()
	# users = db['typical'].find_one({'_id': 4418090668})

	# for t in users['tweets']:
	# 	try:
	# 		print t['text']
	# 	except Exception as e:
	# 		continue
	# count = 0
	# for user in users:
	# 	# tags = interest_extract.extract_tags(user['tweets'], user['description'])
	# 	# print tags
		
	# 	max_score = sorted(user['category_score'].iteritems(), key = lambda asd:asd[1], reverse=True)
	# 	# print 
	# 	if user['category'] != max_score[0][0]:
	# 		# print max_score[0][0]
	# 		count += 1
	# 		print user['screen_name']
	# 	# break
	# print count
	# 	for tt in user['tweets']:
	# 		print tt['text']
	# extract_interset()
	# calc_sentiment()
	# calc_sentiment_score()
	# sentiment_dict_test()

	# try:
	# 	words = word_tokenize("What a beautiful sunday . happy")
	# 	print nltk.pos_tag(words)
	# except Exception as e:
	# 	print e
	db = MongoDB().connect()
	users = db['typical'].find()

	count = 1
	data_set = {
		'retweet_favorite_rate': [],
		'fans_retweet_rate': [],
		'fans_favorite_rate': []
	}
	for user in users:
		tweets = user['tweets']
		fans = user['followers_count']

		# if fans > 2000000:
		# 	continue
		count += 1

		if count > 150:
			break
		tweet_count = 0
		retweet_count = 0
		favorite_count = 0
		for tweet in tweets:
			if 'RT @' not in tweet['text']:
				tweet_count += 1.

				retweet_count += tweet['retweet_count']
				favorite_count += tweet['favorite_count']
		
		fans_retweet_rate = fans / (retweet_count / tweet_count)
		if fans_retweet_rate > 600000 or fans_retweet_rate < 50:
			continue
		
		fans_favorite_rate = fans / (favorite_count / tweet_count)
		if fans_favorite_rate > 600000 or fans_favorite_rate < 50:
			continue
		
		retweet_favorite_rate = (retweet_count / tweet_count) / (favorite_count / tweet_count)
		# print fans, tweet_count, retweet_count, retweet_count / tweet_count
		if fans_retweet_rate < 0:
			print user['_id']
		data_set['retweet_favorite_rate'].append(retweet_favorite_rate)
		data_set['fans_retweet_rate'].append(fans_retweet_rate)
		data_set['fans_favorite_rate'].append(fans_favorite_rate)

	x_axix = range(len(data_set['retweet_favorite_rate']))
	x_axix = np.array(x_axix)
	x_axix_new = np.linspace(x_axix.min(), x_axix.max(), 4000)

	y_axix = data_set['retweet_favorite_rate']
	y_axix_new = spline(x_axix ,y_axix, x_axix_new)

	plt.plot(x_axix_new, y_axix_new, color='green', label='Retweet Favorite Rate')

	y_axix = data_set['fans_retweet_rate']
	y_axix_new = spline(x_axix ,y_axix, x_axix_new)

	plt.plot(x_axix_new, y_axix_new, color='red', label='Fans Retweet Rate')

	# y_axix = data_set['fans_favorite_rate']
	# y_axix_new = spline(x_axix, y_axix, x_axix_new)
	plt.plot(x_axix, y_axix, color='blue', label='Fans Retweet Rate')
	# plt.plot(x_axix, train_pn_dis,  color='skyblue', label='PN distance')
	# plt.plot(x_axix, thresholds, color='blue', label='threshold')
	plt.legend() # 显示图例

	# # print y_axix, x_axix_new
	# for i in x_axix_new:
	# 	print i
	plt.xlabel('Users')
	plt.ylabel('Rate')
	plt.show()

	