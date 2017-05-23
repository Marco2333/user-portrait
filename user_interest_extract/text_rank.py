# -*- coding: utf-8 -*-  
import re
import nltk
import MySQLdb

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


text = 'a smart clever clever Season dog clever Bobby Moynihan Departing Saturday Night clear smart Seasons Live After 9 Seasons'
twitter_stop_words = ["after", "from","TO","to","https","RT","URL","in","re","thank","thanks","today","yesterday","tomorrow","night","tonight","day","year","last","oh","yeah","amp"]

'''
步骤一：数据预处理
分词-》去除停用词-》词性标注
'''
def preprocess(text):
	# clear @/#/http
	text = re.sub(r'[@|#][\d|\w|_]+|http[\w|:|.|/|\d]+',"",text)

	if text == "" or text == None:
		return [] 

	wordslist = []
	words = word_tokenize(text),
	words = words[0]

	for word in words:
		word = word.lower()
		if word not in (stopwords.words("english") and twitter_stop_words):  # clear stopwords
			if len(word) > 2 and word.isalpha():
				wordslist.append(word)
	try:
		pos = nltk.pos_tag(wordslist)
	except Exception as e:
		print e
		pos = []

 	res = []
	lemmatizer = WordNetLemmatizer()
	single_pattern = ["N", "J", "V"]
	for w in pos:
		if word in (stopwords.words("english") and twitter_stop_words) or len(word) > 20:   # 删除停用词
			continue

		if w[1][0] == 'N':
			word = lemmatizer.lemmatize(w[0])  # 词形归并
			res.append((word, w[1]))

		elif w[1][0] == 'J':
			word = lemmatizer.lemmatize(w[0], 'a')  # 词形归并
			res.append((word, w[1]))

		elif w[1][0] == 'V':
			word = lemmatizer.lemmatize(w[0], 'v')  # 词形归并
			res.append((word, w[1]))

	return res

'''
获得特定属性单词的共现窗口
'''
def get_word_cooccurrence(pos):
	co_window = {}
	word_list = []
	co_window_width = 6

	for w in pos:
		if w[1][0] == 'N' or w[1][0] == 'J' or w[1][0] == 'V':
			word_list.append(w[0])

	word_set = set(word_list)

	for w in word_set:
		related_set = set()
		length = len(word_list)
		index_arr = find_all_index(word_list, w)

		for index in index_arr:
			lower_bound = (index - co_window_width) > 0 and index - co_window_width or 0
			upper_bound = (index + co_window_width) < length and index + co_window_width or length - 1  # 包含upper_bound
			i = lower_bound

			while i <= upper_bound:
				related_set.add(word_list[i])
				i += 1

		related_set.remove(w)
		co_window[w] = related_set

	return co_window


def find_all_index(arr, item):
	return  [i for i,a in enumerate(arr) if a == item]


def get_topk_word(co_window, k = -1):
	max_iter = 10000000
	pre_item_score = {}

	for w in co_window:
		pre_item_score[w] = len(co_window[w])

	i = 0
	d = 0.85
	while i < max_iter:
		i += 1
		item_score = {}

		for w in co_window:
			sum = 0
			for item in co_window[w]:
				sum += (1.0 / len(co_window[item])) * pre_item_score[item]
				
			item_score[w] = d * sum + (1 - d)
		
		if calc_differ(pre_item_score, item_score) < 0.0001:
			break

		pre_item_score =  item_score

	res = sorted(item_score.iteritems(), key = lambda v: v[1], reverse = True)

	if k == -1:
		return res

	return res[0 : k]


def calc_differ(score1, score2):
	res = 0
	for item in score1:
		res += abs(score1[item] - score2[item])

	return res


def get_user_info():
	db = MySQLdb.connect('127.0.0.1', 'root', '283319', 'twitter')
	db.set_character_set('utf8')
	cursor = db.cursor()

	sql = "select user_id from user_famous"

	try:
		cursor.execute(sql)
		user_list = cursor.fetchall()
		user_list = map(lambda x: x[0], user_list)
	except Exception as e:
		print e

	return user_list


def exe_process(text, k):
	pos = preprocess(text)
	coo = get_word_cooccurrence(pos)
	res = get_topk_word(coo, k)

def main():
	pos = preprocess(text)
	coo = get_word_cooccurrence(pos)
	res = get_topk_word(coo)
	print res
	# user_list = get_user_info()

	# client = MongoClient('127.0.0.1', 27017)
	# db = client['twitter']
	# collect = db['tweets']

	# for user_id in user_list:
	# 	text = ""
	# 	tweets = collect.find({'user_id': long(user_id)}, {text: 1})
	# 	for tt in tweets:
	# 		text += tt['text']

	# 	exe_process(text)



if __name__ == '__main__':
	main()