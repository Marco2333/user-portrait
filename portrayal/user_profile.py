from sentiment_classify import sentiment_classify
from career_classify.classify import exe_classify
from interest_extract.interest_extract import extract_tags
from influence.calculate_influence import calculate_influence, calc_activity_sequence


def user_profile(user):
	tweets = user['tweets']
	
	if not tweets or len(tweets) == 0:
		return user

	final_sentiment, psy_with_time1, psy_with_time2, psy_with_count1, psy_with_count2 = sentiment_classify.exe_sentiment_classify(tweets)
	user['psy'] = final_sentiment
	user['psy_with_time1'] = psy_with_time1
	user['psy_with_time2'] = psy_with_time2
	user['psy_with_count1'] = psy_with_count1
	user['psy_with_count2'] = psy_with_count2

	text = ''
	for tweet in tweets:
		text += tweet['text']

	category, categories_score = exe_classify(text)
	user['category'] = category
	user['category_score'] = categories_score

	user['interest_tags'] = extract_tags(tweets, user['description'])

	influence_score, activity = calculate_influence(user['followers_count'], tweets)
	user['influence_score'] = influence_score
	user['activity'] = activity

	user['activity_list'] = calc_activity_sequence(tweets)

	return user