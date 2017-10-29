# coding=utf-8
import os
import nltk

from statistics import mode
from classify import classify
from nltk.tokenize import word_tokenize
from sentiment_dict import calc_sentiment_score

from .. config import PROJECT_PATH
from .. tools.preprocess import data_cleaning
from .. tools.function import split_tweets_same_time, split_tweets_same_count

module_path = PROJECT_PATH + "portrayal/sentiment_classify/"

def replace_emotion(tweets):
	tweets_temp = []
	emotion = {
		"^_^": "happy",
		":-)": "happy",
		":)": "happy",
		"(:": "happy",
		"(-:": "happy",
		"<3": "happy",
		":*": "happy",
		":-D": "happy",
		":D": "happy",
		"X-D": "happy happy",
		"XD": "happy happy",
		"xD": "happy happy",
		";-)": "happy",
		";)": "happy",
		";-D": "happy",
		";D": "happy",
		"(;": "happy",
		"(-;": "happy",
		":-(": "unhappy",
		":((": "sad",
		":(": "unhappy",
		"(:": "unhappy",
		"(-:": "unhappy",
		":,(": "sad",
		":'(": "sad",
		":”(": "sad"
	}

	for tweet in tweets:
		text = tweet['text']

		for item in emotion:
			text = text.replace(item, emotion[item])
		
		text = data_cleaning(text)

		tweets_temp.append({
			'text': text,
			'created_at': tweet['created_at']
		})

	return tweets_temp


def sentiment_with_time(tweets, time_span = 1):
	tweets_list = split_tweets_same_time(tweets, time_span)

	sequence1 = []
	sequence2 = []
	for tts in tweets_list:
		res = classify(tts)

		if res == 'pos':
			sequence1.append(1)
		elif res == 'neg':
			sequence1.append(-1)
		else:
			sequence1.append(0)
	
		score = calc_sentiment_score(tts)

		if not score:
			sequence2.append(0)
		else:
			sequence2.append(score)
		
	return sequence1, sequence2


def sentiment_with_count(tweets, count = 66):
	tweets_list = split_tweets_same_count(tweets, count)

	sequence1 = []
	sequence2 = []
	for tts in tweets_list:
		res = classify(tts)
		
		if res == 'pos':
			sequence1.append(1)
		elif res == 'neg':
			sequence1.append(-1)
		else:
			sequence1.append(0)
	
		score = calc_sentiment_score(tts)

		if not score:
			sequence2.append(0)
		else:
			sequence2.append(score)

	return sequence1, sequence2


def exe_sentiment_classify(tweets):
	tweets = replace_emotion(tweets)

	psy_with_time1, psy_with_time2 = sentiment_with_time(tweets)
	psy_with_count1, psy_with_count2 = sentiment_with_count(tweets)

	count = 0
	for item in psy_with_time2:
		if item > 0:
			count += 1
		else:
			count -= 1

	if count > 0:
		final_sentiment = 1
	
	elif count < 0:
		final_sentiment = -1
	
	else:
		final_sentiment = 0

	return final_sentiment, psy_with_time1, psy_with_time2, psy_with_count1, psy_with_count2