# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-30 14:16:44 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-30 14:16:44 
'''
import os
import pickle

from classify import classify
from ... config import PROJECT_PATH
from .. tools.preprocess import preprocess_postag


module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


class SentimentDict:
	sentiment_dict = None

	def preprocess(self, text):
		word_list = preprocess_postag(text)

		if not word_list:
			return None

		res = []
		for word in word_list:
			if word[1][0] == 'N':
				res.append((word[0], 'n'))

			elif word[1][0] == 'J':
				res.append((word[0], 'a'))

			elif word[1][0] == 'V':
				res.append((word[0], 'v'))

			elif word[1][0] == 'R':
				res.append((word[0], 'r'))

		return res


	def calc_sentiment_score(self, text):
		if not self.sentiment_dict:
			if not os.path.exists(pickle_path + "sentiment_dict.pickle"):
				self.generate_sentiment_dict()

			file = open(pickle_path + "sentiment_dict.pickle")
			self.sentiment_dict = pickle.load(file)

		score = 0
		word_list = self.preprocess(text)

		if not word_list:
			return None

		for word in word_list:
			key = word[0] + '#' + word[1]
			if key in self.sentiment_dict:
				score += self.sentiment_dict[key]

		return score


	def generate_sentiment_dict(self):
		sentiment_dict = {}
		file = open(module_path + 'data/sentiment_words.txt')

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
		
		# count = 0
		# for item in res:
		# 	if abs(res[item]) > 0.4:
		# 		count += 1
		# 		print item

		# print count

		file = open(pickle_path + "sentiment_dict.pickle", 'w')
		pickle.dump(res, file)
		file.close()
		
		return res


sentiment_dict = SentimentDict()

def calc_sentiment_score(text):
	return sentiment_dict.calc_sentiment_score(text)