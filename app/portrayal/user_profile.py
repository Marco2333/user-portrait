from sentiment_classify import sentiment_classify
from career_classify.classify import career_classify
from interest_extract.interest_extract import extract_tags
from influence.calculate_influence import calculate_influence, calc_activity_sequence


def user_profile(user):
	tweets = user['tweets']
	
	final_sentiment, list1, list2 = sentiment_classify.sentiment_with_time(tweets)
	user['psy'] = final_sentiment
	user['psy_with_time1'] = list1
	user['psy_with_time2'] = list2

	list1, list2 = sentiment_classify.sentiment_with_count(tweets)
	user['psy_with_count1'] = list1
	user['psy_with_count2'] = list2

	text = ''
	for tweet in tweets:
		text += tweet['text']

	category, categories_score = career_classify(text)
	user['category'] = category
	user['categories_score'] = categories_score

	user['interest_tags'] = extract_tags(text, user['description'])

	influence_score, activity = calculate_influence(user['followers_count'], tweets)
	user['influence_score'] = influence_score
	user['activity'] = activity

	user['activity_list'] calc_activity_sequence(tweets)

	return user