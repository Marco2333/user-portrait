import os

from statistics import mode
from classify import classify
from sentiment_dict import calc_sentiment_score

from ... config import PROJECT_PATH
from .. tools.function import split_tweets_same_time, split_tweets_same_count

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"

def sentiment_with_time(tweets, classify_type = 0, time_span = 1):
	tweets_list = split_tweets_same_time(tweets, time_span)

	sequence1 = []
	sequence2 = []
	for tts in tweets_list:
		text = ''

		for tweet in tts:
			text += tweet['text'] + ' '
		
		if classify_type == 0 or classify_type == 1:
			res = classify(text)
			if res == 'pos':
				sequence1.append(1)
			if res == 'neg':
				sequence1.append(-1)

		if classify_type == 0 or classify_type == 2:
			score = calc_sentiment_score(text)

			if score != None:
				sequence2.append(score)

	if classify_type == 0 or classify_type == 1:
		try:
			final_sentiment = mode(sequence1)
		except:
			final_sentiment = 0

	else:
		count = 0
		for item in sequence2:
			if item > 0:
				count += 1
			else:
				count -= 1

		if count > 0:
			final_sentiment = 1
		
		if count < 0:
			final_sentiment = -1
		
		else:
			final_sentiment = 0

	return final_sentiment, sequence1, sequence2


def sentiment_with_count(tweets, classify_type = 0, count = 80):
	tweets_list = split_tweets_same_count(tweets, count)

	sequence1 = []
	sequence2 = []
	for tts in tweets_list:
		text = ''

		for tweet in tts:
			text += tweet['text'] + ' '
		
		if classify_type == 0 or classify_type == 1:
			res = classify(text)
			if res == 'pos':
				sequence1.append(1)
			if res == 'neg':
				sequence1.append(-1)

		if classify_type == 0 or classify_type == 2:
			score = calc_sentiment_score(text)
			sequence2.append(score)

	return sequence1, sequence2