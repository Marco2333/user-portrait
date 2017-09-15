# coding=utf-8
'''
 * @Author: Marco 
 * @Date: 2017-09-10 22:54:55 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-09-10 22:54:55 
'''
import re
import os
import math
import pickle

from collections import Counter
from nltk.stem import WordNetLemmatizer

from .. tools.preprocess import preprocess_postag

from .. config import PROJECT_PATH

module_path = PROJECT_PATH + "portrayal/interest_extract/"
data_path = module_path + "data/"
pickle_path = module_path + "pickle/"

corpus = None

def generate_pickle():
	files = os.listdir(data_path + 'corpus')
	corpus_list = []

	for f in files:
		text = ''
		corpus_set = set()
		file = open(data_path + 'corpus/' + f, "r").read()
		for p in file.split("\n"):
			text += p

		word_tags = preprocess_postag(text)	

		if not word_tags:
			continue

		for word in word_tags:
			if word[1][0] == 'N':
				corpus_set.add(word[0])

		corpus_list.append(corpus_set)

	file = open(pickle_path + "corpus.pickle", 'w')
	pickle.dump(corpus_list, file)
	file.close()

	return corpus_list


def import_corpus():
	global corpus
	if not corpus:
		if not os.path.exists(pickle_path + "corpus.pickle"):
			corpus = generate_pickle()
		else:
			file = open(pickle_path + "corpus.pickle", 'r')
			corpus = pickle.load(file)
			file.close()


def generate_candidate(word_tags):
	if len(word_tags) < 1:
		return []
	
	candidate_list = []
	phrase_list = []
	
	lemmatizer = WordNetLemmatizer()

	for item in word_tags:
		if item[1][0] == 'N':
			word = lemmatizer.lemmatize(item[0], 'n')
			candidate_list.append(word)
		
	if len(word_tags) == 2 and (word_tags[0][1][0] == 'J' or word_tags[0][1][0] == 'V') and word_tags[1][1][0] == 'N':
		if word_tags[0][1][0] == 'J':
			pos_type = 'a'
		
		if word_tags[0][1][0] == 'V':
			pos_type = 'v'
		
		phrase_list.append(lemmatizer.lemmatize(word_tags[0][0], pos_type) + " " + lemmatizer.lemmatize(word_tags[1][0], 'n'))

	i = 0
	while(i < len(word_tags) - 2):
		if word_tags[i][1][0] == 'V' and (word_tags[i + 1][1][0] == 'N' or (word_tags[i + 1][1][0] == 'J' and word_tags[i + 2][1][0] == 'N')):
			if word_tags[i + 1][1][0] == 'J':
				suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'a') + " "
				suffix += lemmatizer.lemmatize(word_tags[i + 2][0], 'n')
				phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'v') + " " + suffix)
				i += 3
			else:
				phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'v') + " " + lemmatizer.lemmatize(word_tags[i + 1][0], 'n'))
				i += 2	
		elif word_tags[i][1][0] == 'J' and word_tags[i + 1][1][0] == 'N':
			phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'a') + " " + lemmatizer.lemmatize(word_tags[i + 1][0], 'n'))
			i += 2
		else:
			i += 1

	if i != 0 and i == len(word_tags) - 2 and word_tags[i + 1][1][0] == 'N':
		if word_tags[i][1][0] == 'J':
			phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'a') + lemmatizer.lemmatize(word_tags[i + 1][0], 'n'))
		
		if word_tags[i][1][0] == 'V':
			phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'v') + lemmatizer.lemmatize(word_tags[i + 1][0], 'n'))
	
	return candidate_list + phrase_list
				

def calc_tf_idf(candidate_list):
	if corpus == None:
		import_corpus()

	count = Counter(candidate_list)
	common_word = count.most_common(150)
	
	tf_idf = {}
	corpus_len = len(corpus)
	for item in common_word:
		n = 1
		for corpus_set in corpus:
			if item[0] in corpus_set:
				n += 1

		idf = math.log(corpus_len * 1.0 / n, 10)
		tf_idf[item[0]] = item[1] * idf

	candidate_list = sorted(tf_idf.iteritems(), key = lambda item: item[1], reverse = True)

	return candidate_list[:100]


def extract_tags(text, description = '', count = 30):
	candidate_list = generate_candidate(preprocess_postag(description + text + description))

	candidate_tags = calc_tf_idf(candidate_list)
	interset_tags = map(lambda tag: tag[0], candidate_tags)

	res_tags = []
	filter_set = set()

	for item in interset_tags:
		if len(res_tags) >= count:
			break

		word_list = item.split(' ')

		if len(word_list) == 1:
			if item not in filter_set:
				res_tags.append(item)
				filter_set.add(item)
		else:
			for word in word_list:
				if word.strip() != '':
					filter_set.add(word)
					if word in res_tags:
						res_tags.remove(word)
			
			res_tags.append(item)
	
	return re.sub(r'label(\w+)label', r'#\1' , ','.join(res_tags[:count]))	