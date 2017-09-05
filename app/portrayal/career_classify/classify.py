# -*- coding: utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-09-05 16:18:19 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-05 16:18:19 
 '''
import math
import pickle

from ... config import PROJECT_PATH

module_path = PROJECT_PATH + "portrayal/career_classify/"
pickle_path = module_path + "pickle/"

categories_path = pickle_path + "categories.pickle"
count_vector_path = pickle_path + "count_vector.pickle"
tf_idf_transformer_path = pickle_path + "tf_idf_transformer.pickle"


def classify(text = ''):
	if text == "":
		return None
	
	text = [text]

	count_vector_file = open(count_vector_path)
	count_vector = pickle.load(count_vector_file)
	count_vector_file.close()

	count_feature_matrix = count_vector.transform(text)

	tf_idf_transformer_file = open(tf_idf_transformer_path)
	tf_idf_transformer = pickle.load(tf_idf_transformer_file)
	tf_idf_transformer_file.close()

	tf_idf_feature_matrix = tf_idf_transformer.transform(count_feature_matrix)

	# 分类器
	classifier_path = pickle_path + 'multi_classifier.pickle'

	# 分类
	multi_classifier_file = open(classifier_path)
	multi_classifier = pickle.load(multi_classifier_file)
	multi_classifier_file.close()

	categories_file = open(categories_path)
	target_names = pickle.load(categories_file)
	categories_file.close()

	category = target_names[multi_classifier.predict(tf_idf_feature_matrix.toarray())[0]]
	score_list = multi_classifier._joint_log_likelihood(tf_idf_feature_matrix.toarray())[0]

	min_value = min(score_list)
	min_value = math.floor(min_value)

	categories_score = {}
	for i in range(len(score_list)):
		categories_score[target_names[i]] = round((score_list[i] - min_value) * 25, 2)

	return category, categories_score