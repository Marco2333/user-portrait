from pymongo import MongoClient
from portrayal import UserProfile
from crawler import crawler

if __name__ == '__main__':
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']

	collect1 = db['typical']
	collect2 = db['typical_temp']

	tus = collect1.find({}, {'_id': 1})
	tus_temp = collect2.find({}, {'_id': 1})

	res_temp = set()
	for item in tus_temp:
		res_temp.add(item['_id'])

	res = []
	for item in tus:
		res.append(item['_id'])

	for item in res:
		print item
		
		if item in res_temp:
			continue

		try:
			user = crawler.get_user_all_info(user_id = item)
			user = UserProfile.UserProfileFromDic(user)

			user['_id'] = long(user['user_id'])
			del user['user_id']

			collect2.insert_one(user)
		except Exception as e:
			print e
			continue