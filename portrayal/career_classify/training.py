# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-09-05 14:07:32 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-05 14:07:32 
 */
'''
import os
import pickle

from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier
from .. config import PROJECT_PATH

module_path = PROJECT_PATH + "portrayal/career_classify/"

'''
BCC: business/entertainment/politics/sport/technology
CNN: agriculture/economy/education/entertainment/military/politics/religion/sports/technology

data: BCC新闻数据集 + 维基词条文章 + 部分CNN文本
'''
def training(dataset_path = module_path + "data_processed", pickle_path = module_path + "pickle/"):
	print "读入训练数据..."
	training_dataset = datasets.load_files(dataset_path)

	# 类别标签
	categories = training_dataset.target_names
	print categories
	categories_path = pickle_path + "categories.pickle"
	categories_file = open(categories_path, "wb")
	pickle.dump(categories, categories_file)
	categories_file.close()

	# 词频统计
	count_vector = CountVectorizer(stop_words = "english", decode_error = "ignore")
	count_feature_matrix = count_vector.fit_transform(training_dataset.data)

	count_vector_path = pickle_path + "count_vector.pickle"
	count_vector_file = open(count_vector_path, "wb")
	pickle.dump(count_vector, count_vector_file)
	count_vector_file.close()

	# 计算词频-逆文档频率
	tf_idf_transformer = TfidfTransformer().fit(count_feature_matrix)

	# 持久化 tf_idf_transformer
	tf_idf_transformer_path = pickle_path + "tf_idf_transformer.pickle"
	tf_idf_transformer_file = open(tf_idf_transformer_path, "wb")
	pickle.dump(tf_idf_transformer, tf_idf_transformer_file)
	tf_idf_transformer_file.close()
	print "词频-逆文档频率已保存"

	tf_idf_feature_matrix = tf_idf_transformer.transform(count_feature_matrix)

	# 多项式贝叶斯分类器分类
	# multi_classifier = MultinomialNB()
	# bagging = BaggingClassifier(base_estimator=MultinomialNB(),max_sample=0.5,max_features=0.5,n_estimators=60,n_jobs=-1)
	# bagging_classifier = bagging.fit(tf_idf_feature_matrix, training_dataset.target)
	# print "Bagging 学习器完成"
	multi_classifier = MultinomialNB().fit(tf_idf_feature_matrix, training_dataset.target)
	print "多项式贝叶斯分类器训练完成"

	multi_classifier_path = pickle_path + "multi_classifier.pickle"
	multi_classifier_file = open(multi_classifier_path, "wb")
	pickle.dump(multi_classifier, multi_classifier_file)
	multi_classifier_file.close()
	print "多项式分类器已保存"


def training_special_category(category_list, dataset_path = module_path + "data_category/", pickle_path = module_path + "pickle_category/"):
	category_list.sort()

	dir_name = ''
	for item in category_list:
		dir_name += '_' + item

	dir_name = dir_name[1 : ]

	pickle_category_path = pickle_path + dir_name + "/"

	if not os.path.exists(pickle_category_path):
		os.makedirs(pickle_category_path) 
	
	training(dataset_path + dir_name, pickle_category_path)