from pymongo import MongoClient
from crawler.tweets_crawler import TweetsCrawler
from crawler.relation_crawler import RelationCrawler

tweets_crawler = TweetsCrawler()
relation_crawler = RelationCrawler()


'''
获取用户基础信息和推文信息，以字典形式返回
'''
def get_user_all_info(user_id = None, screen_name = None):
	user = basicinfo_crawler.get_user(user_id = user_id, screen_name = screen_name)
	tweets = tweets_crawler.get_user_all_timeline_return(user_id = user_id, screen_name = screen_name)

	return {
		'user_id': long(user.id),
		'screen_name': user.screen_name,
		'name': user.name,
		'verified': user.verified,
		'friends_count': user.friends_count,
		'description': user.description,
		'crawler_date': time.strftime('%Y-%m-%d',time.localtime(time.time())),
		'followers_count': user.followers_count,
		'location': user.location,
		'statuses_count': user.statuses_count,
		'favourites_count': user.favourites_count,
		'lang': user.lang,
		'utc_offset': user.utc_offset,
		'protected': user.protected,
		'profile_background_color': user.profile_background_color,
		'default_profile_image': user.default_profile_image,
		'created_at': user.created_at,
		'profile_banner_url': user.profile_banner_url,
		'time_zone': user.time_zone,
		'profile_image_url': user.profile_image_url,
		'listed_count': user.listed_count,
		'tweets': tweets
	}

	
# 同步典型人物的关系信息
def get_friends():
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']

	collect1 = db['typical']
	collect2 = db['relation']

	tus = collect1.find({}, {'_id': 1})

	user_list = []
	for item in tus:
		user_list.append(item['_id'])

	relation_list = []
	tur = collect2.find({}, {'_id': 1})

	for item in tur:
		if item['_id'] not in user_list:
			collect2.delete_one({'_id': item['_id']})

		else:
			relation_list.append(item['_id'])

	for user_id in user_list:

		if user_id in relation_list:
			continue

		cursor = -1
		friends = []

		while cursor != 0:
			out = relation_crawler.get_friendids_paged_sleep(user_id = user_id,
															 cursor = cursor, 
															 count = 5000)
			if not out:
				break
			
			friends = friends + out[2]
			cursor = out[0]

		collect2.insert_one({
			'_id': user_id,
			'friends': friends
		})
	

# 获取所有用户的朋友信息
def get_all_users_friends(user_list):
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']

	collect = db['1020_friends']

	for user_id in user_list:

		cursor = -1
		friends = []

		while cursor != 0:
			out = relation_crawler.get_friendids_paged_sleep(user_id = user_id,
															 cursor = cursor, 
															 count = 5000)
			if not out:
				break
			
			friends = friends + out[2]
			cursor = out[0]

		collect.insert_one({
			'_id': user_id,
			'friends': friends
		})