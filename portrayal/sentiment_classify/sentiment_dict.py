# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-30 14:16:44 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-30 14:16:44 
'''
import re
import os
import sys
import math
import nltk
import pickle

from classify import classify
from nltk.tokenize import word_tokenize

from .. config import PROJECT_PATH
from .. tools.preprocess import preprocess_postag
from .. tools.function import get_stop_words
from .. tools.function import get_slang

reload(sys)
sys.setdefaultencoding('utf-8')

slang = get_slang()
stop_words = get_stop_words()

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


class SentimentDict:
	sentiment_dict = None

	def preprocess(self, tweets):
		res = []
		but_words = set(["but", "however"])
		hope_words = set(["hope", "wish"])
		deny_words = set(['not', "n't", 'no', 'never', 'none', 'hardly', 'isnt', 'doesnt'])
		degree_words = set(["fairly", "pretty", "quite", "very", "much", "too", "greatly", "highly", "really", "extremely", "so"])
		filter_set = set(['affected', 'allow', 'allows', 'backed', 'backing', 'backs', 'best', 'better', 'big', 'certain', 'clear', 'clearly', 'good', 'greetings', 'ha', 'haa', 'hah', 'haha', 'hahaa', 'help', 'hid', 'hopefully', 'ignored', 'importance', 'important', 'kind', 'like', 'liked', 'lmao', 'matter', 'miss', 'novel', 'please', 'sorry', 'substantially', 'thk', 'thx', 'thank', 'thanks', 'thanx', 'thaanks', 'true', 'unfortunately', 'useful', 'usefully', 'usefulness', 'want', 'welcome', 'woohoo', 'yeah', 'yeahh', 'yes'])

		for tweet in tweets:
			text = tweet['text'].lower()

			if text == '':
				continue

			try:
				words = word_tokenize(text)

				for i in range(len(words)):
					if words[i] in slang:
						words[i] = slang[words[i]]

				word_tags = nltk.pos_tag(words)

			except Exception as e:
				print e
				continue
			
			deny = False
			degree = False
			but = False
			hope = False

			length = len(word_tags)
			
			for i in range(length):
				item = word_tags[i]
				word = item[0]
				
				if word in deny_words:
					deny = True
					degree = False
					continue
				elif word in but_words:
					but = True
					j = i - 1
					flag = True

					while j >= 0 and (flag or word_tags[j][0].isalpha()):
						if not word_tags[j][0].isalpha() or i - j > 2:
							flag = False

						w_t = word_tags[j][0]
						t_t = word_tags[j][1][0]
						if w_t not in stop_words:
							flag = False
							if t_t == 'J' or t_t == 'V' or t_t == 'R' or t_t == 'N':
								res.append("FOT_" + w_t)

						j -= 1
					continue
				elif word in degree_words:
					degree = True
					continue
				elif word in hope_words:
					hope = True
					continue

				if not word.isalpha() and not (item[1][0] == 'J' or item[1][0] == 'V' or item[1][0] == 'R' or item[1][0] == 'N'):
					deny = False
					degree = False
					hope = False

					if i == 0 or word_tags[i - 1] not in but_words:
						but = False

				elif word not in stop_words or word in filter_set:
					prefix = ""
					if deny:
						prefix += "NOT_"
					if hope:
						prefix += "HOP_"
					if degree and item[1][0] == 'J':
						prefix += "TWO_"

					if not word.isalpha():
						temp_list = word.split(" ")
						for item_temp in temp_list:
							if item_temp.isalpha() and (item_temp not in stop_words or item_temp in filter_set):
								res.append(prefix + item_temp)

					elif item[1][0] == 'J' or item[1][0] == 'V' or item[1][0] == 'R' or item[1][0] == 'N':
						res.append(prefix + word)
		
		return res


	def calc_sentiment_score(self, tweets):
		if not self.sentiment_dict:
			self.sentiment_dict = {}

			senti_file = open(module_path + "data/sentiment_words1.txt").read()

			for line in senti_file.split("\n"):
				sp = line.split("\t")
				self.sentiment_dict[sp[0].strip()] = int(sp[1])

		score = 0
		word_list = self.preprocess(tweets)

		if not word_list:
			return None

		for word in word_list:
			rate = 1

			if "FOT_" in word:
				rate *= -0.9
				word = word.replace("FOT_", '')

			if "NOT_" in word:
				if "TWO_" in word:
					rate *= -0.3
					word = word.replace("TWO_", '')
				else:
					rate *= -0.8

				if "HOP_" in word:
					rate *= -0.4
					word = word.replace("HOP_", '')
				
				word = word.replace("NOT_", '')
			else:
				if "TWO_" in word:
					rate *= 1.8
					word = word.replace("TWO_", '')

				if "HOP_" in word:
					rate *= 0.6
					word = word.replace("HOP_", '')

			if word in self.sentiment_dict:
				score += self.sentiment_dict[word] * rate

		return score


sentiment_dict = SentimentDict()

def calc_sentiment_score(tts):
	return sentiment_dict.calc_sentiment_score(tts)