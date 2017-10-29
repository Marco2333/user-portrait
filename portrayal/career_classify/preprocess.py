# -*- coding: utf-8 -*- 
import os
import pickle

from nltk.tokenize import word_tokenize

from .. tools.preprocess import preprocess
from .. config import PROJECT_PATH


module_path = PROJECT_PATH + "portrayal/career_classify"
data_dir = module_path + '/data/'
data_processed_dir = module_path + '/data_processed/'
statistics_dir = module_path + '/statistics/'
data_category_dir = module_path + '/data_category/'

def process_training_data():
	category_dirs = os.listdir(data_dir)

	for item in category_dirs:
		if not os.path.exists(data_processed_dir + item):
			os.makedirs(data_processed_dir + item) 

		cat_files = os.listdir(data_dir + item)

		for cat_file in cat_files:
			file = open(data_dir + item + "/" + cat_file)
			file_processed = open(data_processed_dir + item + "/" + cat_file, 'w')

			for line in file:
				if line.strip() == '':
					continue
				
				line = preprocess(line.strip())
			
				try:
					file_processed.write(line + '\n')
				except:
					continue


def word_count():
	count_dict = {}
	category_dirs = os.listdir(data_processed_dir)

	for item in category_dirs:
		cat_files = os.listdir(data_processed_dir + item)

		for cat_file in cat_files:
			file_processed = open(data_processed_dir + item + "/" + cat_file, 'r')

			for line in file_processed:
				word_list = line.split(" ")

				for word in word_list:
					word = word.strip()

					if count_dict.has_key(word):
						count_dict[word] += 1
					
					else:
						count_dict[word] = 1

		count_dict = sorted(count_dict.iteritems(), key = lambda i: i[1], reverse = True)

		file = open(statistics_dir + item + ".pickle", 'wb')		
		pickle.dump(count_dict, file)
		file.close()

		count_dict = {}


# def get_ambiguity_words(category_pair = None):
# 	if not category_pair:
# 		category_pair = [
# 			("Entertainment", "Sports", 40),
# 			("Economy", "Agriculture", 40),
# 			("Politics", "Religion", 40),
# 			("Military", "Politics", 40),
# 			("Education", "Technology", 40),
# 			("Education", "Politics", 40),
# 			("Education", "Entertainment", 40),
# 			("Education", "Agriculture", 40),
# 			("Technology", "Entertainment", 40),
# 			("Economy", "Technology", 40),
# 			("Economy", "Politics", 40)
# 		]

# 	delete_set = set()
# 	for pair in category_pair:
# 		top_words0 = set()

# 		file = open(statistics_dir + pair[0] + ".pickle")
# 		count_dict = pickle.load(file)

# 		for item in count_dict:
# 			if item[1] >= pair[2]:
# 				top_words0.add(item[0])
			
# 			else:
# 				break

# 		top_words1 = set()

# 		file = open(statistics_dir + pair[1] + ".pickle")
# 		count_dict = pickle.load(file)

# 		for item in count_dict:
# 			if item[1] >= pair[2]:
# 				top_words1.add(item[0])
			
# 			else:
# 				break

# 		delete_set |= top_words0 & top_words1

# 	print len(delete_set)
# 	return delete_set


# def delete_ambiguity(category_pair = None):
# 	ambiguity_words = get_ambiguity_words(category_pair)

# 	category_dirs = os.listdir(data_processed_dir)

# 	for item in category_dirs:
# 		if not os.path.exists(data_pruned_dir + item):
# 			os.makedirs(data_pruned_dir + item) 

# 		cat_files = os.listdir(data_processed_dir + item)

# 		for cat_file in cat_files:
# 			file = open(data_processed_dir + item + "/" + cat_file)
# 			file_pruned = open(data_pruned_dir + item + "/" + cat_file, 'w')

# 			for line in file:
# 				if line.strip() == '':
# 					continue
				
# 				word_list = line.strip().split(" ")
# 				word_list = [w for w in word_list if w not in ambiguity_words]
				 
# 				try:
# 					file_pruned.write(' '.join(word_list) + '\n')
# 				except:
# 					continue


def get_ambiguity_words(category_list, count = 20):
	delete_set = None

	for category in category_list:
		top_words = set()
		
		file = open(statistics_dir + category + ".pickle")
		count_dict = pickle.load(file)
		file.close()

		for item in count_dict:
			if item[1] >= count:
				top_words.add(item[0])
			
			else:
				break
		print len(top_words)
		if not delete_set:
			delete_set = top_words
		else:
			delete_set &= top_words

	print len(delete_set)
	return delete_set


def delete_ambiguity(category_list, count = 20):
	category_list.sort()
	
	ambiguity_words = get_ambiguity_words(category_list)

	dir_name = ''
	for item in category_list:
		dir_name += '_' + item

	dir_name = dir_name[1 : ]

	category_path = data_category_dir + dir_name + "/"

	if not os.path.exists(category_path):
		os.makedirs(category_path) 

	for category in category_list:

		if not os.path.exists(category_path + category):
			os.makedirs(category_path + category) 

		cat_files = os.listdir(data_processed_dir + category)

		for cat_file in cat_files:
			file = open(data_processed_dir + category + "/" + cat_file)
			file_category = open(category_path + category + "/" + cat_file, 'w')

			for line in file:
				if line.strip() == '':
					continue
				
				word_list = line.strip().split(" ")
				word_list = [w for w in word_list if w not in ambiguity_words]
				 
				try:
					file_category.write(' '.join(word_list) + '\n')
				except:
					continue