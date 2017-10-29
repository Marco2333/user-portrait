#coding=utf-8
'''
 * @Author: Marco 
 * @Date: 2017-09-09 14:29:43 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-09 14:29:43 
'''
import os
import pickle
import training
from statistics import mode

from .. tools.preprocess import preprocess_del_stopwords
from .. config import PROJECT_PATH


module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


class VotingClassifier:
	classifier_list = []
	words_feature = None

	def init(self):
		self.load_classifier()
	

	def load_classifier(self):
		classifier_names = [
			'naivebayes',
			'mnb_classifier',
			'bnb_classifier',
			'lr_classifier',
			'lsv_classifier',
			'sgd_classifier'
		]

		# 加载之前保存的训练好的分类器模型
		for name in classifier_names:
			if not os.path.exists(pickle_path + name + ".pickle"):
				training.training()

			classifier_file = open(pickle_path + name + ".pickle", "rb")
			classifier = pickle.load(classifier_file)
			classifier_file.close()

			self.classifier_list.append(classifier)
		

	def classify(self, tts):
		text = ''
		for item in tts:
			text += item['text'] + ' '

		if len(self.classifier_list) == 0:
			self.load_classifier()
		
		feature = self.word2features(text)

		if not feature:
			return None

		votes = []
		for classifier in self.classifier_list:
			vote = classifier.classify(feature)
			votes.append(vote)
		
		try:
			res= mode(votes)
		except Exception as e:
			print e
			return 0
		
		return res

	def word2features(self, document):
		if not self.words_feature:
			feature_file = open(pickle_path + "words_feature.pickle")
			self.words_feature = pickle.load(feature_file)
			feature_file.close()

		word_list = set(preprocess_del_stopwords(document))
		
		if not word_list:
			return None
		
		feature = {}
		for w in self.words_feature:
			feature[w] = w in word_list
		
		return feature


voting_classifier = VotingClassifier()


def classify(text):
	return voting_classifier.classify(text)