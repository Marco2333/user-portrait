# from crawler.extension import main
from pymongo import MongoClient
from crawler.app.relation_crawler import RelationCrawler
from crawler.app.tweets_crawler import TweetsCrawler

relation_crawler = RelationCrawler()
tweets_crawler = TweetsCrawler()


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


if __name__ == '__main__':
	print tweets_crawler.get_user_timeline(screen_name = 'mrmarcohan')[0]