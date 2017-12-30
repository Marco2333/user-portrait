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

from .. tools.preprocess import preprocess_postag_label

from .. config import PROJECT_PATH

from .. tools.function import get_stop_words


module_path = PROJECT_PATH + "portrayal/interest_extract/"
data_path = module_path + "data/"
pickle_path = module_path + "pickle/"

corpus = None
stop_words = get_stop_words()

def generate_pickle():
	files = os.listdir(data_path + 'corpus')
	corpus_list = []

	for f in files:
		text = ''
		corpus_set = set()
		file = open(data_path + 'corpus/' + f, "r").read()
		for p in file.split("\n"):
			text += p

		word_tags = preprocess_postag_label(text)	

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
		if item[1][0] == 'N' or item[0][0] == '#':
			if item[0][0] == '#':
				candidate_list.append(item[0])

			else:
				word = lemmatizer.lemmatize(item[0], 'n')
				if word not in stop_words:
					candidate_list.append(word)
		
	if len(word_tags) == 2 and (word_tags[0][1][0] == 'J' or word_tags[0][1][0] == 'V') and word_tags[1][1][0] == 'N':
		if word_tags[0][1][0] == 'J':
			prefix = lemmatizer.lemmatize(word_tags[0][0], 'a')
		
		if word_tags[0][1][0] == 'V':
			prefix = lemmatizer.lemmatize(word_tags[0][0], 'v')
		
		suffix = lemmatizer.lemmatize(word_tags[1][0], 'n')

		if prefix not in stop_words and suffix not in stop_words:
			phrase_list.append(prefix + " " + suffix)

	i = 0
	while(i < len(word_tags) - 2):
		if word_tags[i][0][0] == '#':
			i += 1
			continue

		if word_tags[i + 1][0][0] == '#':
			i += 2
			continue

		if word_tags[i][1][0] == 'V' and (word_tags[i + 1][1][0] == 'N' or (word_tags[i + 1][1][0] == 'J' and word_tags[i + 2][1][0] == 'N')):
			if word_tags[i + 1][1][0] == 'J':
				suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'a') + " "
				suffix += lemmatizer.lemmatize(word_tags[i + 2][0], 'n')
				phrase_list.append(lemmatizer.lemmatize(word_tags[i][0], 'v') + " " + suffix)
				i += 3
			else:
				prefix = lemmatizer.lemmatize(word_tags[i][0], 'v')
				suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'n')

				if prefix not in stop_words and suffix not in stop_words:
					phrase_list.append(prefix + " " + suffix)
				
				i += 2

		elif word_tags[i][1][0] == 'J' and word_tags[i + 1][1][0] == 'N':
			prefix = lemmatizer.lemmatize(word_tags[i][0], 'a')
			suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'n')

			if prefix not in stop_words and suffix not in stop_words:
				phrase_list.append(prefix + " " + suffix)

			i += 2

		else:
			i += 1

	if i != 0 and i == len(word_tags) - 2 and word_tags[i + 1][1][0] == 'N':
		if word_tags[i][1][0] == 'J':
			prefix = lemmatizer.lemmatize(word_tags[i][0], 'a')
			suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'n')

			if prefix not in stop_words and suffix not in stop_words:
				phrase_list.append(prefix + " " + suffix)
		
		elif word_tags[i][1][0] == 'V':
			prefix = lemmatizer.lemmatize(word_tags[i][0], 'v')
			suffix = lemmatizer.lemmatize(word_tags[i + 1][0], 'n')

			if prefix not in stop_words and suffix not in stop_words:
				phrase_list.append(prefix + " " + suffix)
	
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

	return candidate_list[:90]


def calc_weight(tweets, candidates):
	weight_dict = {}

	length = len(candidates)

	for item in candidates:
		weight_dict[item] = {}

		for sub_item in candidates:
			if item != sub_item:
				weight_dict[item][sub_item] = 0

	for i in range(length):
		item = candidates[i]
		j = i + 1

		while j < length:
			sub_item = candidates[j]
			j += 1

			for tweet in tweets:
				text = tweet['text']

				if item in text and sub_item in text:
					weight_dict[item][sub_item] += 1
					weight_dict[sub_item][item] += 1

	o_vector = {}

	for item in candidates:
		o_vector[item] = 0

		for sub_item in candidates:
			if item != sub_item:
				o_vector[item] += weight_dict[item][sub_item]
		
	return weight_dict, o_vector


def text_rank(tweets, candidates_list):
	candidates = {}
	for item in candidates_list:
		candidates[item[0]] = item[1]

	weight_dict, o_vector = calc_weight(tweets, candidates.keys())

	alpha = 0.85
	score_vector = {}
	related_items = {}

	for item in candidates:
		score_vector[item] = 1
		related_items[item] = []

		for sub_item in candidates:
			if item != sub_item and weight_dict[item][sub_item] != 0:
				related_items[item].append(sub_item)

	i = 0
	while i < 88:
		score_vector_temp = {}

		for item in candidates:
			score_temp = (1 - alpha) * candidates[item]

			for sub_item in related_items[item]:
				score_temp += weight_dict[item][sub_item] * 1.0 / o_vector[sub_item] * score_vector[sub_item]

			score_vector_temp[item] = alpha * score_temp

		if calc_differ(score_vector, score_vector_temp) < 1:
			score_vector = score_vector_temp
			break

		score_vector = score_vector_temp

		i += 1

	return sorted(score_vector.iteritems(), key = lambda item: item[1], reverse = True)


def calc_differ(score_vector1, score_vector2):
	differ = 0

	for item in score_vector1:
		differ += abs(score_vector1[item] - score_vector2[item])

	return differ


def get_top_tags(candidate_tags, count, filter_set):
	interset_tags = map(lambda tag: tag[0], candidate_tags)

	res_tags = []

	for item in interset_tags:
		if len(res_tags) >= count:
			break

		item_temp = item.replace('#', '')
		word_list = item.split(' ')

		if len(word_list) == 1:
			if item_temp not in filter_set and len(item) > 2:
				res_tags.append(item)
				filter_set.add(item_temp)
		else:
			for word in word_list:
				if word.strip() != '':
					filter_set.add(word)
					if word in res_tags:
						res_tags.remove(word)
			
			res_tags.append(item)
	
	return res_tags[:count]


def join_top_tags(tfidf_tags, textrank_tags, count):
	final_set = tfidf_tags[:count * 3 / 5]

	for item in tfidf_tags[count * 3 / 5:]:
		if item[0] == '#':
			final_set.append(item)
		
	for item in textrank_tags:
		if item not in final_set:
			final_set.append(item)
	
	return final_set[:count]

def extract_tags(tweets, description = '', count = 36):
	text = ''
	for tweet in tweets:
		text += tweet['text'] + " , "

	word_tags = preprocess_postag_label(description + text + description)
	candidate_list = generate_candidate(word_tags)

	filter_set = set(["dis", "fuck", "hell", "damn", "shit", "bitch", "wow", "cool", "fun", "glad",
		"joy", "luck", "laugh", "bless", "appreciate", "wish", "hope", "play", "set", "close", "talk",
		"change", "join", "move", "watch", "meet", "post", "wait", "live", "deal", "eat", "call",
		"pick", "start", "end", "kid", "boy", "home", "tweet", "video", "bang", "dope",
		"year", "month", "hour", "minute", "second", "moment", "morning", "afternoon", "evening"])

	candidate_tags = calc_tf_idf(candidate_list)
	tfidf_tags = get_top_tags(candidate_tags, count, filter_set)
	
	candidate_tags = text_rank(tweets, candidate_tags)
	textrank_tags = get_top_tags(candidate_tags, count, filter_set)

	tfidf_tags = join_top_tags(tfidf_tags, textrank_tags, count)

	return ','.join(tfidf_tags)