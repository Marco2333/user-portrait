# -*- coding: utf-8 -*- 
# from app.database import MongoDB
import nltk
# import re
from nltk.tokenize import word_tokenize
# from app.portrayal.career_classify import training, classify
# from app.portrayal.tools import preprocess
# from app.portrayal.career_classify import preprocess as training_preprocess
from app.portrayal.sentiment_classify import sentiment_dict
# from app.portrayal.interest_extract import interest_extract
# from app.portrayal.tools import preprocess
# from app.portrayal.user_profile import user_profile


def classify_career():
	db = MongoDB().connect('dump')
	users = db['typical_temp'].find({'category': 'Education'})

	err_dict = {}
	n = 0
	for user in users:
		print user['screen_name']
		tweets = user['tweets']

		text = user['description']
		for tweet in tweets:
			text += ' ' + tweet['text']
		
		text = preprocess.preprocess(text)

		res = classify.exe_classify(text)
			
		if err_dict.has_key(res[0]):
			err_dict[res[0]] += 1
		else:
			err_dict[res[0]] = 1

		if res[0] == user['category']:
			n += 1

	print err_dict	
	print n

def extract_interset():
	db = MongoDB().connect()
	users = db['typical'].find()

	for u in users:
		text = ''
		for item in u['tweets']:
			text += item['text'] + ' '

		try:
			tags = interest_extract.extract_tags(text, u['description'])
		except Exception as e:
			print u['_id']
			print e
			continue

		db['typical'].update({'_id': u['_id']}, {"$set": {"interest_tags": tags}})


def profile():
	db = MongoDB().connect()
	users = db['typical'].find().limit(1)

	for user in users:
		temp = user_profile(user)
		del temp['tweets']
		print temp


if __name__ == "__main__":
	# extract_interset()
	# profile()
	sentiment_dict.test()
# 	print nltk.pos_tag(word_tokenize(''' i can't wait for christina to kiss me thru tha phone tomorrow. :)  Then we'll be back to our sarcasm and odd inside jokes. :) My little man, all of 4, bought
# his first CD: Johnny Cash.   i'll be super excited if dumating sila.. :p will you watch the David's concert?? :) @yijingman I can't tell you how many t
# imes that one has come up for me. Hah! The boss isn't here today, unless I am he. Hmmm... :) @elorahhh let's do them again!! :D @jordanknight OH SNAP!!!! I'm on to you Jordan - I know what u mean when u say TINK - hit me up and I will tell
# ya :) WOOT WOOT How does it feel      =) i agree. RT serenadethedead @iamlauren Martin Nievera sucked. :| :D Only thing I liked was his ear piece thing. XD @tiffamand
# er knee jerk reaction to mac-n-talk voiced persons... sorry  :) Just got off the phone with my girlie in Cali. She says I have a different love language than others.
# I love it! =) Gnite TweetPeeps. ready for a nice relaxing week! No school and no work! :-) @KatrinaMichelle  Lol very nice .. well i am going to go it later her in Al
# berta .. cya later :) @SohanaB Yeah, I've seen those. :) I have friends in Houston that are Shia, and I think from your sect. Not sure though. Cool piano music to sta
# rt the day: Honky Tonk Train Blues http://tinyurl.com/c53n39 - I admit, I need to clean the storage room :-) I am not enjoyingthe new PGA Golf Tour Callenge. Golden T
# ee is much better :) @DonnieWahlberg Oh 4got to say I am in Christchurch, New Zealand :) is bed.... feeling really good about my exam tomorrow :D @Cfitz002 it had its
#  moments haha. My they are cute when they've just hatched like that. What a sweet, little @Luvrte66.  Awwww. :) Follow Love!'''))
	# preprocess.preprocess_postag(text.replace('\n',' '))