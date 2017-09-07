# -*- coding:utf-8 -*-
import re
import sys
import nltk

from nltk.tokenize import word_tokenize

from function import get_stop_words

reload(sys)
sys.setdefaultencoding('utf-8')

stop_words = get_stop_words()

def preprocess(text, return_type = "string"):
	text = re.sub(r'^RT @\w+:|@\w+|#|(ht|f)tp[^\s]+', "", text)
	text = text.lower()

	try:
		words = word_tokenize(text)
	except Exception as e:
		print e
		return

	word_list = [w for w in words if w not in stop_words and w.isalpha()]

	return word_list if return_type == 'list' else ' '.join(word_list)


def preprocess_postag(text):
	text = re.sub(r'^RT @\w+:|@\w+|#|(ht|f)tp[^\s]+', "", text)
	text = text.lower()

	try:
		words = word_tokenize(text)
		word_tags = nltk.pos_tag(words)
	except Exception as e:
		print e
		return
	
	res = []
	for item in word_tags:
		if item[0] not in stop_words and item[0].isalpha():
			res.append(item)
	
	return res