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
import math
import nltk
import pickle


from classify import classify
from nltk.tokenize import word_tokenize

from .. config import PROJECT_PATH
from .. tools.preprocess import preprocess_postag
from .. tools.function import get_stop_words
from .. tools.function import get_slang

reload(sys)
sys.setdefaultencoding('utf-8')

slang = get_slang()
stop_words = get_stop_words()

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"


class SentimentDict:
	sentiment_dict = None

	def preprocess(self, tweets):
		tweets = [{"text": tweets}]
		res = []
		but_words = set(["but", "however"])
		hope_words = set(["hope", "wish"])
		deny_words = set(['not', "n't", 'no', 'never', 'none', 'hardly'])
		degree_words = set(["fairly", "pretty", "quite", "very", "much", "too", "greatly", "highly", "really", "extremely", "so"])

		for tweet in tweets:
			text = tweet['text']
			text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
			text = re.sub(r"(..)\1{2,}", r"\1\1", text)
			text = re.sub(r'(rt)?\s?@\w+:?|#|(ht|f)tp[^\s]+', " ", text).lower()

			text = text.replace('wanna', 'want to')
			text = text.replace('gonna', 'will')
			text = text.replace('gotta', 'must')
			text = text.replace('have to', 'haveto')
			text = text.replace('haha', 'happy')
			text = text.replace('hungrryy', 'hungry')
			try:
				words = word_tokenize(text)

				for i in range(len(words)):
					if words[i] in slang:
						words[i] = slang[words[i]]

				word_tags = nltk.pos_tag(words)

			except Exception as e:
				print e
				continue
			
			deny = False
			degree = False
			but = False
			hope = False

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
					flag = True

					while j >= 0 and (flag or word_tags[j][0].isalpha()):
						if not word_tags[j][0].isalpha() or i - j > 2:
							flag = False

						w_t = word_tags[j][0]
						t_t = word_tags[j][1][0]
						if w_t not in stop_words:
							flag = False
							if t_t == 'J':
								res.append(("FOT_" + w_t, 'a'))
							elif t_t == 'V':
								res.append(("FOT_" + w_t, 'v'))
							elif t_t == 'R':
								res.append(("FOT_" + w_t, 'r'))
							elif t_t == 'N':
								res.append(("FOT_" + w_t, 'n'))
							
						j -= 1
					continue
				elif word in degree_words:
					degree = True
					continue
				elif word in hope_words:
					hope = True
					continue

				if not word.isalpha():
					deny = False
					degree = False
					hope = False

					if i == 0 or word_tags[i - 1] not in but_words:
						but = False

				elif word not in stop_words:
					prefix = ""
					if deny:
						prefix += "NOT_"
					if hope:
						prefix += "HOP_"
					if degree and item[1][0] == 'J':
						prefix += "TWO_"

					if item[1][0] == 'J':
						res.append((prefix + word, 'a'))
					elif item[1][0] == 'V':
						res.append((prefix + word, 'v'))
					elif item[1][0] == 'R':
						res.append((prefix + word, 'r'))
					elif item[1][0] == 'N':
						res.append((prefix + word, 'n'))

		return res


	def calc_sentiment_score(self, tweets):
		if not self.sentiment_dict:
			if not os.path.exists(pickle_path + "sentiment_dict.pickle"):
				self.generate_sentiment_dict()

			file = open(pickle_path + "sentiment_dict.pickle")
			self.sentiment_dict = pickle.load(file)
			file.close()
	
		# print self.sentiment_dict['inextinguishable#a']
		# return

		# if not self.sentiment_dict:
		senti_file = open(module_path + "data/senti_wrods.txt").read()
		sentiment_dict = {}

		for line in senti_file.split("\n"):
			sp = line.split("\t")
			sentiment_dict[sp[0].strip()] = int(sp[1])

		print len(self.sentiment_dict)
		print self.sentiment_dict['sad#a']
		for item in self.sentiment_dict:
			sl = item.split("#")
			if(sl[1] == 'a' or sl[1] == 'v' or sl[1] == 'r') and sl[0].isalpha() and (sl[0] not in sentiment_dict):
				score = self.sentiment_dict[item] * 30 / 5

				if int(score) > 5 or int(score) < -5:
					print sl
					print score
				else:
					if abs(score) >= 1:
						sentiment_dict[sl[0]] = int(score)

					elif abs(score) > 0.66:
						if score < 0:
							sentiment_dict[sl[0]] = -1
						if score > 0:
							sentiment_dict[sl[0]] = 1
						
				

		senti_file = open(module_path + "data/temp.txt", 'w')
		for item in sentiment_dict:
			senti_file.write(item + "\t" + str(sentiment_dict[item]) + "\n")
		return

		score = 0
		word_list = self.preprocess(tweets)

		if not word_list:
			return None

		for word_tuple in word_list:
			rate = 1
			word = word_tuple[0]
			
			print word

			if "FOT_" in word:
				rate *= -0.9
				word = word.replace("FOT_", '')

			if "NOT_" in word:
				if "TWO_" in word:
					rate *= 0.4
					word = word.replace("TWO_", '')
				else:
					rate *= -0.7

				if "HOP_" in word:
					rate *= -0.5
					word = word.replace("HOP_", '')
				
				word = word.replace("NOT_", '')
			else:
				if "TWO_" in word:
					rate *= 1.8
					word = word.replace("TWO_", '')

			key = word
			# key = word  + '#' + word_tuple[1]
			if key in self.sentiment_dict:
				score += self.sentiment_dict[key] * rate
				print score
			# elif (word_tuple[1] == 'r' or word_tuple[1] == 'v') and (word + '#a' in self.sentiment_dict):
			# 	score += self.sentiment_dict[word + '#a'] * rate
				# print score
			# elif (word_tuple[1] == 'n') and (word + '#v' in self.sentiment_dict):
			# 	score += self.sentiment_dict[word + '#v'] * rate
				# print score

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
	calc_sentiment_score('''the lead actors share no chemistry or engaging charisma . we don't even like their characters .  . some writer dude , i think his name was , uh , michael zaidan , was supposed to have like written the screenplay or something , but , dude , the only thing that i ever saw that was written down were the zeroes on my paycheck.  . the movie doesn't generate a lot of energy . it is dark , brooding and slow , and takes its central idea way too seriously .  . this feature is about as necessary as a hole in the head . the cinematic equivalent of patronizing a bar favored by pretentious , untalented artistes who enjoy moaning about their cruel fate.  . spectators will indeed sit open-mouthed before the screen , not screaming but yawning .  . it feels like very light errol morris , focusing on eccentricity but failing , ultimately , to make something bigger out of its scrapbook of oddballs .  . a period story about a catholic boy who tries to help a jewish friend get into heaven by sending the audience straight to hell .  . the premise itself is just sooooo tired . pair that with really poor comedic writing . . . and you've got a huge mess .  . proves a lovely trifle that , unfortunately , is a little too in love with its own cuteness .  . did we really need a remake of " charade ? " . some movies can get by without being funny simply by structuring the scenes as if they were jokes : a setup , delivery and payoff . stealing harvard can't even do that much . each scene immediately succumbs to gravity and plummets to earth .  . the only fun part of the movie is playing the obvious game . you try to guess the order in which the kids in the house will be gored .  . i spied with my little eye . . . a mediocre collection of cookie-cutter action scenes and occasionally inspired dialogue bits . entertains not so much because of its music or comic antics , but through the perverse pleasure of watching disney scrape the bottom of its own cracker barrel .  . the satire is just too easy to be genuinely satisfying .  . bearable . barely .  . less funny than it should be and less funny thanit thinks it is .  . an " o bruin , where art thou ? " -style cross-country adventure . . . it has sporadic bursts of liveliness , some so-so slapstick and a fewear-pleasing songs on its soundtrack .  . a feeble tootsie knockoff .  . an awful movie that will only satisfy the most emotionally malleable of filmgoers .  . 鍗糷e story is far-flung , illogical , and plain stupid .  . the very simple story seems too simple and the working out of the plot almost arbitrary .  . an allegory concerning the chronically mixed signals african american professionals get about overachieving could be intriguing , but the supernatural trappings only obscure the message .  . a very familiar tale , one that's been told by countless filmmakers about italian- , chinese- , irish- , latin- , indian- , russian- and otherhyphenate american young men struggling to balance conflicting cultural messages .  . one key problem with these ardently christian storylines is that there is never any question of how things will turn out .  . essentially , the film is weak on detail and strong on personality . a relentless , bombastic and ultimately empty world war ii action flick .  . [hell is] looking down at your watch and realizing serving sara isn't even halfway through .  . too long , and larded with exposition , this somber cop drama ultimately feels as flat as the scruffy sands of its titular community .  . ''')
 	return
	file = open(module_path + 'data1/negative.txt').read()

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
			if score > 0:
				print text
				y += 1
			
			text = ''
	
	print x
	print y
