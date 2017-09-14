# -*- coding:utf-8 -*-
'''
 * @Author: Marco 
 * @Date: 2017-08-30 14:16:44 
 * @Last Modified by: Marco 
 * @Last Modified time: 2017-08-30 14:16:44 
'''
import re
import os
import sys
import nltk
import pickle


from classify import classify
from nltk.tokenize import word_tokenize

from .. config import PROJECT_PATH
from .. tools.preprocess import preprocess_postag
from .. tools.function import get_stop_words

reload(sys)
sys.setdefaultencoding('utf-8')


stop_words = get_stop_words()

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


class SentimentDict:
	sentiment_dict = None

	def preprocess(self, tweets):
		tweets = [{"text": tweets}]
		res = []
		but_words = set(["but", "however"])
		deny_words = set(['not', "n't", 'no', 'never', 'none', 'hardly'])
		degree_words = set(["fairly", "pretty", "quite", "very", "much", "too", "greatly", "highly", "really", "extremely", "so"])

		for tweet in tweets:
			text = tweet['text']
			text = text.replace('wanna', 'want to')
			text = text.replace('gonna', 'will')
			text = re.sub(r'(rt)?\s@\w+:?|#|(ht|f)tp[^\s]+', " ", text).lower()
			try:
				words = word_tokenize(text)
				word_tags = nltk.pos_tag(words)
			except Exception as e:
				print e
				continue
			
			deny = False
			degree = False
			but = False

			length = len(word_tags)
			
			for i in range(length):
				item = word_tags[i]

				word = item[0]
				
				if word in deny_words:
					deny = True
					continue
				elif word in but_words:
					but = True
					j = i - 1
					
					while j >= 0 and word_tags[j][0].isalpha():
						w_t = word_tags[j][0]
						t_t = word_tags[j][1][0]
						if w_t not in stop_words:
							# if t_t == 'N':
							# 	# res.append((prefix + word, 'n'))
							# 	pass
							if t_t == 'J':
								res.append(("FOT_" + w_t, 'a'))
							elif t_t == 'V':
								res.append(("FOT_" + w_t, 'v'))
							elif t_t == 'R':
								res.append(("FOT_" + w_t, 'r'))
							
						j -= 1
					continue
				elif word in degree_words:
					degree = True
					continue

				if not word.isalpha():
					deny = False
					degree = False

					if i == 0 or word_tags[i - 1] not in but_words:
						but = False

				elif word not in stop_words:
					prefix = ""
					if deny:
						prefix += "NOT_"
					if degree and item[1][0] == 'J':
						prefix += "TWO_"

					# if item[1][0] == 'N':
					# 	# res.append((prefix + word, 'n'))
					# 	pass
					if item[1][0] == 'J':
						res.append((prefix + word, 'a'))
					elif item[1][0] == 'V':
						res.append((prefix + word, 'v'))
					elif item[1][0] == 'R':
						res.append((prefix + word, 'r'))
			
		return res


	def calc_sentiment_score(self, tweets):
		if not self.sentiment_dict:
			if not os.path.exists(pickle_path + "sentiment_dict.pickle"):
				self.generate_sentiment_dict()

			file = open(pickle_path + "sentiment_dict.pickle")
			self.sentiment_dict = pickle.load(file)
			file.close()

		score = 0
		word_list = self.preprocess(tweets)

		if not word_list:
			return None

		for word_tuple in word_list:
			rate = 1
			word = word_tuple[0]
			
			print word + "#" + word_tuple[1]
			if "NOT_" in word and "TWO_" not in word:
				rate *= -0.7
				word = word.replace("NOT_", '')
			if "FOT_" in word:
				rate *= -1
				word = word.replace("FOT_", '')
			if "TWO_" in word and "NOT_" not in word:
				rate *= 2
				word = word.replace("TWO_", '')
			if "TWO_" in word and "NOT_" in word:
				rate *= -0.6
				word = word.replace("TWO_", '').replace("NOT_", '')

			key = word  + '#' + word_tuple[1]
			if key in self.sentiment_dict:
				score += self.sentiment_dict[key] * rate
				print score
			elif (word_tuple[1] == 'r' or word_tuple[1] == 'v') and (word + '#a' in self.sentiment_dict):
				score += self.sentiment_dict[word + '#a'] * rate
				print score
			
		return score


	def generate_sentiment_dict(self):
		sentiment_dict = {}
		file = open(module_path + 'data/sentiment_words.txt')

		data = []
		while 1:
			lines = file.readlines(100000)
			if not lines:
				break

			for line in lines:
				if line.strip().startswith("#"):
					continue
				else:
					data = line.split("\t")
					if len(data) != 6:
						print line
						print 'invalid data'
						continue

				word_type = data[0]
				synset_score = float(data[2]) - float(data[3])
				syn_terms_list = data[4].split(" ")

				for w in syn_terms_list:
					term_and_num = w.split("#")
					syn_term = term_and_num[0] + "#" + word_type
					term_num = int(term_and_num[1])

					if sentiment_dict.has_key(syn_term):
						sentiment_dict[syn_term].append((term_num, synset_score))
					
					else:
						sentiment_dict[syn_term] = []
						sentiment_dict[syn_term].append((term_num, synset_score))
		
		res = {}
		for key in sentiment_dict:
			score_sum = 0
			count = 0
			for word_tuple in sentiment_dict[key]:
				score_sum += word_tuple[1] * word_tuple[0]
				count += word_tuple[0]
			
			if score_sum / count != 0:
				res[key] = score_sum / count

		file = open(pickle_path + "sentiment_dict.pickle", 'w')
		pickle.dump(res, file)
		file.close()
		
		return res


sentiment_dict = SentimentDict()

def calc_sentiment_score(text):
	return sentiment_dict.calc_sentiment_score(text)


def test():
	calc_sentiment_score('''helou have just sent him an email &amp; gave him your url. he's in Iran in October for a few weeks &amp; then again in March - you never know :) . Only 1 more day of school! WOO! :D . @lickmycup
cakes and then you and Shann could do a set together. And i could shoot it :D . @veganrunningmom yes garage band.  I will do your test no problem.  :) . @maskedfool Wow Kacie, a bit of a Merlin r
ant there :D Colin is adorable. May I just add, here, for the third time, BETA JAPS. XD . @ejmatthews Wow, go in for it! Thanks. :) . #hoppusday is the best day ever :) . @steven_gehrke LOL Doubt
less you meant what I think you meant by that remark about having all the right stuff in the right places! :-) . Shooting photos today it looks like... any models interested, let me know =) . @sa
rasmile13 I am!!! Good morning. :) . Future for ambulances? http://news.bbc.co.uk/1/hi/health/7986460.stm i want one! :D . @RachelMcAdams_  - LMAO! ur such a dork :) . @timmeh Certainly no fun th
ere. Hopefully if you keep smiling you'll be back to 110% in no time! :) . is back in the USA and couldnt be happier :) . off to study for geography :) . @oh_mondieu cool. did you go say hi or ta
ke a picture? :D . anyway, goodnight twitterberries, i think i'm heading off to bed for the day.  Have a wonderful day, since most of you are just waking up :) . @OfficialJagex Mod Ajd will you b
e there tonight? :) . REBEKAH GIBNEY WON THE GOLD LOGIE :D !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! . Welcome to the VIP Chauffeur Twitter Stream :) . Hi @HalElrod Tks and look forward to reading yr tweet
s. I just subscribed to your 'Miracle Morning' audio too :) . @supercoolkp haha! At least it wasn't my finger on my lip again  :D . Want to cut my hair as Lightning :D . True friend - someone who
 sings you to sleep. :) . @MISSMYA ...Miss Mya u gotta get sleep. ...come on, just 2 hours ...jus do it :-) . Swine flu on Twitter! :D #atchoink #failpig #swineflu #grippeporcine #porkfever #hamt
hrax #bacontherapy (URL: http://tinyurl.com/c7oc5f ) . @cmykdorothy I've had the dream once where my teeth fell out; lol re: women's conference :) . @imogenfreeland You're not alone luvvie! This
is like like high school ALL over again :) . thirty one days...now counting weekends :) . is mixing a song called &quot; Tempo17&quot; and well.. it's tough. :D .''')
 	return
	file = open(module_path + 'data/positive.txt').read()

	n = 0
	text = ''
	x = 0
	y = 0
	for p in file.split('\n'):
		n += 1
		text += p + ' . '
		if n % 30 == 0:
			x += 1
			score = calc_sentiment_score(text)
			print score
			if score < 0:
				print text
				y += 1
			
			text = ''
	
	print x
	print y