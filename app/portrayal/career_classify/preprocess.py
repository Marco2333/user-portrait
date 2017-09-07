# -*- coding: utf-8 -*- 
import os
import pickle

from nltk.tokenize import word_tokenize

from .. tools.preprocess import preprocess
from ... config import PROJECT_PATH


module_path = PROJECT_PATH + "portrayal/career_classify"
data_dir = module_path + '/data/'
data_processed_dir = module_path + '/data_processed/'
statistics_dir = module_path + '/statistics/'
data_pruned_dir = module_path + '/data_pruned/'

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


def get_ambiguity_words(category_pair = None, count = 28):
	if not category_pair:
		category_pair = [
			("Entertainment", "Sports", 68),
			("Economy", "Agriculture", 68),
			("Politics", "Religion", 58),
			("Military", "Politics", 56),
			("Education", "Technology",),
			("Education", "Politics", 28),
			("Education", "Entertainment", 66),
			("Technology", "Entertainment", 60),
			("Economy", "Technology", 48),
			("Economy", "Politics", 48)
		]

	min_count = {}
	for pair in category_pair:
		if min_count.has_key(pair[0]):
			if pair[2] < min_count[pair[0]]:
				min_count[pair[0]] = pair[2]
				
		else:
			min_count[pair[0]] = pair[2]
		
		if min_count.has_key(pair[1]):
			if pair[2] < min_count[pair[1]]:
				min_count[pair[1]] = pair[2]
				
		else:
			min_count[pair[1]] = pair[2]


	top_words_dict = {}

	category_dirs = os.listdir(statistics_dir)

	for category in category_dirs:
		top_words = set()

		file = open(statistics_dir + category)
		count_dict = pickle.load(file)
		
		for item in count_dict:
			if item[1] >= count:
				top_words.add(item[0])
			
			else:
				break
			
		top_words_dict[category.split(".")[0]] = top_words

	delete_set = set()
	for cp in category_pair:
		delete_set |= top_words_dict[cp[0]] & top_words_dict[cp[1]]
	
	print len(delete_set)
	return delete_set


def delete_ambiguity(category_pair = None, count = 28):
	ambiguity_words = get_ambiguity_words(category_pair, count)

	category_dirs = os.listdir(data_processed_dir)

	for item in category_dirs:
		if not os.path.exists(data_pruned_dir + item):
			os.makedirs(data_pruned_dir + item) 

		cat_files = os.listdir(data_processed_dir + item)

		for cat_file in cat_files:
			file = open(data_processed_dir + item + "/" + cat_file)
			file_pruned = open(data_pruned_dir + item + "/" + cat_file, 'w')

			for line in file:
				if line.strip() == '':
					continue
				
				word_list = line.strip().split(" ")
				word_list = [w for w in word_list if w not in ambiguity_words]
				 
				try:
					file_pruned.write(' '.join(word_list) + '\n')
				except:
					continue


if __name__ == "__main__":
	process_training_data()