# -*- coding: utf-8 -*-  

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


text = 'a smart dog clever Bobby Moynihan Departing Saturday Night Live After 9 Seasons'
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
步骤2：兴趣词或短语生成候选集
兴趣词的模式为
单个词形式：Noun|Adjective|Verb (经测试效果不是很好，暂时选用名词Noun形式)
词组形式：(Verb?)(Adjective|Noun)Noun+ (词组形式暂时选用动词+名词 或  形容词+名词形式)
动词和名词先做词性还原
'''
def candidate_set_generate(pos):
	print pos
	if len(pos) < 1:
		return []

	candidate_set = []
	word_group = []
	single_pattern = ["N", "J", "V"]

	#词组形式/单个词形式
	i = 0
	while(i < len(pos) - 2):
		phase = ""

		# verb + adj + n or verb + n
		if (pos[i])[1][0] == 'V' and (pos[i + 1][1][0] == 'N' or (pos[i + 1][1][0] == "J" and pos[i + 2][1][0] == "N")):
			phase += pos[i][0] + " " + pos[i + 1][0]
			i = i + 2

			if pos[i + 1][1][0] == 'N':
				candidate_set.append(pos[i + 1][0])

			while(i < len(pos) and (pos[i])[1][0] == 'N'):
				phase += " " + pos[i][0]
				candidate_set.append(pos[i][0])
				i += 1

			word_group.append(phase)

		# adj + n+
		elif(pos[i][1][0] == "J" and pos[i + 1][1][0] == "N"):
			phase += pos[i][0] + " " + pos[i + 1][0]
			candidate_set.append(pos[i + 1][0])
			i += 2

			while(i < len(pos) and (pos[i])[1][0] == 'N'):
				phase += " " + pos[i][0]
				candidate_set.append(pos[i][0])
				i += 1

			word_group.append(phase)
	 
		else:
			i += 1

	if i == len(pos) - 2:
		if pos[i][1][0] == 'V' and pos[i + 1][1][0] == 'N':
			word_group.append(pos[i][0] + " " + pos[i + 1][0])
			candidate_set.append(pos[i + 1][0])

		elif pos[i][1][0] == "J" and pos[i + 1][1][0] == "N":
			word_group.append(pos[i][0] + " " + pos[i + 1][0])
			candidate_set.append(pos[i + 1][0])

	if len(word_group) != 0:
		candidate_set += word_group

	return candidate_set


if __name__ == '__main__':
	pos = preprocess(text)
	print candidate_set_generate(pos)
