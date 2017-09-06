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


def delete_ambiguity():
	top_words_dict = {}

	category_dirs = os.listdir(statistics_dir)

	for item in category_dirs:
		top_words = set()

		file = open(statistics_dir + item)
		count_dict = pickle.load(file)
		
		for item in count_dict:
			if item[1] >= 20:
				top_words.add(item[0])
			
			else:
				break
			
		print len(top_words)
		top_words_dict[item] = top_words


if __name__ == "__main__":
	process_training_data()