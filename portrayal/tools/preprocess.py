# -*- coding:utf-8 -*-
import re
import sys
import nltk

from nltk.tokenize import word_tokenize

from function import get_stop_words, get_slang_set

reload(sys)
sys.setdefaultencoding('utf-8')

stop_words = get_stop_words()
slang_set = get_slang_set()

def data_cleaning(text):
	# clear @/#/链接/RT
	# 去除表达较口语化的语言时，经常使用重复的字符
	text = text.lower()
	text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
	text = re.sub(r"(..)\1{2,}", r"\1\1", text)
	text = re.sub(r'(rt)?\s?@\w+:?|#|(ht|f)tp[^\s]+', " ", text)
	text = text.replace('wanna', 'want to').replace('gonna', 'will').replace('gotta', 'must').replace('have to', 'haveto').replace('hungrryy', 'hungry')

	return text.strip()


def preprocess(text, return_type = "string"):
	text = text.lower()
	text = re.sub(r'rt @\w+:|@\w+|#|(ht|f)tp[^\s]+', " ", text)

	try:
		words = word_tokenize(text)
	except Exception as e:
		print e
		return None

	word_list = [w for w in words if w not in stop_words and w.isalpha()]

	return word_list if return_type == 'list' else ' '.join(word_list)


def preprocess_del_stopwords(text):
	try:
		words = word_tokenize(text)
	except Exception as e:
		print e
		return None

	word_list = [w for w in words if w not in stop_words and w.isalpha()]

	return word_list


def preprocess_postag(text):
	text = text.lower()
	text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
	text = re.sub(r"(..)\1{2,}", r"\1\1", text)
	text = re.sub(r'(rt)?\s?@\w+:?|#|(ht|f)tp[^\s]+', " ", text)

	try:
		words = word_tokenize(text)
		word_tags = nltk.pos_tag(words)
	except Exception as e:
		print e
		return None
	
	res = []
	for item in word_tags:
		if item[0] not in stop_words and item[0].isalpha():
			res.append(item)
	
	return res


def preprocess_postag_label(text):
	text = text.lower()
	text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
	text = re.sub(r"(..)\1{2,}", r"\1\1", text)
	text = re.sub(r'#(\w+)', "label\g<1>label ", text)
	text = re.sub(r'(rt)?\s?@\w+:?|#|hahah\w*|(ht|f)tp[^\s]+', " ", text)
	text = text.replace('new york', "newyork")

	try:
		words = word_tokenize(text)
		word_tags = nltk.pos_tag(words)
	except Exception as e:
		print e
		return None
	
	res = []
	for item in word_tags:
		if item[0] not in stop_words and item[0].isalpha() and item[0] not in slang_set:
			word = re.sub(r'label(\w+)label', r'#\1' , item[0])
			res.append((word, item[1]))

	return res