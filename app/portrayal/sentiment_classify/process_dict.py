# coding=utf-8
from .. config import PROJECT_PATH

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"
pickle_path = module_path + "pickle/"

sentiment_dict = None

def load_sentiment_dict():
	if not sentiment_dict:
		if not os.path.exists(pickle_path + "sentiment_dict.pickle"):
			sentiment_dict = generate_sentiment_dict()


def generate_new_dict():
	new_sentiment_dict = {}

	if not sentiment_dict:
		load_sentiment_dict()

	for item in sentiment_dict:
		sl = item.split("#")
		if(sl[1] == 'a' or sl[1] == 'v' or sl[1] == 'r') and sl[0].isalpha() and (sl[0] not in sentiment_dict):
			score = sentiment_dict[item] * 30 / 5

			if int(score) > 5 or int(score) < -5:
				print sl
				print score
			else:
				if abs(score) >= 1:
					new_sentiment_dict[sl[0]] = int(score)

				elif abs(score) > 0.66:
					if score < 0:
						new_sentiment_dict[sl[0]] = -1
					if score > 0:
						new_sentiment_dict[sl[0]] = 1

	senti_file = open(module_path + "data/sentiment_temp.txt", 'w')
	for item in new_sentiment_dict:
		senti_file.write(item + "\t" + str(new_sentiment_dict[item]) + "\n")

	return


def attr_change(word_tuple, score):
	word = word_tuple[0]
	
	if (word_tuple[1] == 'r' or word_tuple[1] == 'v') and (word + '#a' in sentiment_dict):
		score += sentiment_dict[word + '#a'] * rate
		print score
	elif (word_tuple[1] == 'n') and (word + '#v' in sentiment_dict):
		score += sentiment_dict[word + '#v'] * rate
		print score


def generate_sentiment_dict():
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