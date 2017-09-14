# -*- coding: utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-09-07 20:18:27 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-07 20:18:27 
 '''
import os
import nltk
import pickle
import random

from sklearn.svm import LinearSVC
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier

from .. tools.function import get_stop_words
from .. tools.preprocess import preprocess, preprocess_postag
from .. config import PROJECT_PATH

stop_words = get_stop_words()
module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


# 对一段文档建立特征
def word2features(document, word_features):
	features = {}
	words = word_tokenize(document, language='english')
		
	for w in word_features:
		features[w] = w in words
		
	return features


def save_feature_document():
	# 加载语料库
	pos_corpus = open(module_path + "data/positive.txt", "r").read()
	neg_corpus = open(module_path + "data/negative.txt", "r").read()

	documents = []
	words_feature = []

	# J是代表形容词，R代表副词，V代表动词
	allowed_types = ['J']

	n = 0
	p_temp = ''

	for p in pos_corpus.split("\n"):
		word_tags = preprocess_postag(p)
		
		if not word_tags:
			continue

		# 形容词对情感影响较大，所以选取形容词为特征
		for item in word_tags:
			p_temp += item[0] + " "

			if item[1][0] in allowed_types:
				words_feature.append(item[0])
		
		n += 1
		if n % 15 == 0:
			documents.append((p_temp, "pos"))
			p_temp = ''

	if n > 7:
		documents.append((p_temp, "pos"))
	
	n = 0
	p_temp = ''

	for p in neg_corpus.split("\n"):
		word_tags = preprocess_postag(p)
		
		if not word_tags:
			continue

		for item in word_tags:
			p_temp += item[0] + " "

			if item[1][0] in allowed_types:
				words_feature.append(item[0])
		
		n += 1
		if n % 15 == 0:
			documents.append((p_temp, "neg"))
			p_temp = ''

	if n > 7:
		documents.append((p_temp, "neg"))

	# 将处理好的文档持久化
	documents_file = open(pickle_path + "documents.pickle","wb")
	pickle.dump(documents, documents_file)
	documents_file.close()
	print "Documents saved!"

	# 统计
	words_feature = nltk.FreqDist(words_feature)
	words_feature_temp = sorted(words_feature.iteritems(), key = lambda i: i[1], reverse = True)

	words_feature = map(lambda tuple: tuple[0], words_feature_temp)
	words_feature = words_feature[0 : 5000]

	# 将特征属性持久化
	feature_file = open(pickle_path + "words_feature.pickle", "wb")
	pickle.dump(words_feature, feature_file)

	feature_file.close()
	print "words_feature saved!"

	feature_sets = [(word2features(p, words_feature), category) for (p, category) in documents]

	# 将特征属性持久化
	feature_file = open(pickle_path + "feature_sets.pickle", "wb")
	pickle.dump(feature_sets, feature_file)

	feature_file.close()
	print "feature_sets saved!"


def training():
	if not os.path.exists(pickle_path + "feature_sets.pickle"):
		save_feature_document()
		
	feature_file = open(pickle_path + "feature_sets.pickle")
	feature_sets = pickle.load(feature_file)

	# 打乱，为了抽取训练集和测试集
	random.shuffle(feature_sets)
	print "Length of feature_sets: "
	print len(feature_sets)

	testing_set = feature_sets[150:]
	print("testing: %d" % len(testing_set))
	training_set = feature_sets
	print("training: %d" % len(training_set))

	# 分类器选择
	# 朴素贝叶斯-nltk自带分类器
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	print "NaiveBayesClassifier accuracy:"
	print(nltk.classify.accuracy(classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "naivebayes.pickle", "wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()

	# 多项式分类器-sklearn
	mnb_classifier = SklearnClassifier(MultinomialNB())
	mnb_classifier.train(training_set)
	print "MultinomialNB accuracy:"
	print(nltk.classify.accuracy(mnb_classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "mnb_classifier.pickle", "wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()

	# 伯努利分类器-sklearn
	bnb_classifier = SklearnClassifier(BernoulliNB())
	bnb_classifier.train(training_set)
	print "BernoulliNB accuracy:"
	print(nltk.classify.accuracy(bnb_classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "bnb_classifier.pickle", "wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()

	# 逻辑回归分类-sklearn
	lr_classifier = SklearnClassifier(LogisticRegression())
	lr_classifier.train(training_set)
	print "LogisticRegression accuracy:"
	print(nltk.classify.accuracy(lr_classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "lr_classifier.pickle", "wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()

	# 线性支持向量机分类器-sklearn
	lsv_classifier = SklearnClassifier(LinearSVC())
	lsv_classifier.train(training_set)
	print "LinearSVC accuracy:"
	print(nltk.classify.accuracy(lsv_classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "lsv_classifier.pickle", "wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()

	# 梯度下降分类器-sklearn
	sgd_classifier = SklearnClassifier(SGDClassifier())
	sgd_classifier.train(training_set)
	print "SGDClassifier accuracy:"
	print(nltk.classify.accuracy(sgd_classifier, testing_set))
	# 分类器持久化
	classifier_file = open(pickle_path + "sgd_classifier.pickle","wb")
	pickle.dump(classifier, classifier_file)
	classifier_file.close()