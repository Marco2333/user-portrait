# -*- coding: utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-09-07 20:18:27 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-07 20:18:27 
 '''
 
import nltk
import pickle
import random

from ... tools.function import get_stop_words
from ... tools.preprocess import preprocess, preprocess_postag
from ... config import PROJECT_PATH

stop_words = get_stop_words()
module_path = PROJECT_PATH + "portrayal/sentiment_classify/"

# 对一段文档建立特征
def word2features(document, word_features):
	features = {}
	words = preprocess(document)
		
	for w in word_features:
		features[w] = w in words
		
	return features


def training():
	# 加载语料库
	pos_corpus = open(project_path + "module_path/positive.txt", "r").read()
	neg_corpus = open(project_path + "module_path/negative.txt", "r").read()

	documents = []
	words_feature = []

	# J是代表形容词，R代表副词，V代表动词
	allowed_types = ['J']

	for p in pos_corpus.split("\n"):
		word_tags = preprocess_postag(p)
		
		if not word_tags:
			continue

		p_temp = ''

		# 形容词对情感影响较大，所以选取形容词为特征
		for item in word_tags:
			p_temp += item[0] + " "

			if item[1][0] in allowed_types:
				words_feature.append(item[0])
		
		if p_temp != '':
			documents.append((p_temp, "pos"))

	for p in neg_corpus.split("\n"):
		word_tags = preprocess_postag(p)
		
		if not word_tags:
			continue

		p_temp = ''

		for item in word_tags:
			p_temp += item[0] + " "

			if item[1][0] in allowed_types:
				words_feature.append(item[0])
		
		if p_temp != '':
			documents.append((p_temp, "neg"))

	# 将处理好的文档持久化
	save_documents = open(module_path + "pickle/documents.pickle","wb")
	pickle.dump(documents, save_documents)
	save_documents.close()
	print("处理完成的文档已保存!")

	words_feature = nltk.FreqDist(words_feature)
	words_feature = words_feature.keys()

	# 将特征属性持久化
	feature_file = open(module_path + "pickle/words_feature.pickle", "wb")
	pickle.dump(words_feature, feature_file)

	feature_file.close()
	print("特征属性已保存!")

	feature_sets = [(word2features(p, words_feature), category) for (p, category) in documents]

	print feature_sets

	return
	# 打乱，为了抽取训练集和测试集
	random.shuffle(feature_sets)
	print("共有数据集: ")
	print len(feature_sets)

	testing_set = feature_sets[10000:]
	print("测试集:659条")
	training_set = feature_sets[:10000]
	print("训练集:10000条")

	# 分类器选择
	# 朴素贝叶斯-nltk自带分类器
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	print("朴素贝叶斯分类精度:")
	print(nltk.classify.accuracy(classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/naivebayes.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()

	# 多项式分类器-sklearn
	MNB_classifier = SklearnClassifier(MultinomialNB())
	MNB_classifier.train(training_set)
	print("多项式分类器分类精度:")
	print(nltk.classify.accuracy(MNB_classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/MNB_classifier.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()

	# 伯努利分类器-sklearn
	BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
	BernoulliNB_classifier.train(training_set)
	print("伯努利分类器分类精度：")
	print(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/BernoulliNB_classifier.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()

	# 逻辑回归分类-sklearn
	LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
	LogisticRegression_classifier.train(training_set)
	print("逻辑回归分类器分类精度:")
	print(nltk.classify.accuracy(LogisticRegression_classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/LogisticRegression_classifier.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()

	# 线性支持向量机分类器-sklearn
	LinearSVC_classifier = SklearnClassifier(LinearSVC())
	LinearSVC_classifier.train(training_set)
	print("线性支持向量机分类精度:")
	print(nltk.classify.accuracy(LinearSVC_classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/LinearSVC_classifier.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()

	# 梯度下降分类器-sklearn
	SGDC_classifier = SklearnClassifier(SGDClassifier())
	SGDC_classifier.train(training_set)
	print("梯度下降分类精度：")
	print(nltk.classify.accuracy(SGDC_classifier,testing_set))
	# 分类器持久化
	save_classifier = open("pickle_algos/SGDC_classifier.pickle","wb")
	pickle.dump(classifier,save_classifier)
	save_classifier.close()
