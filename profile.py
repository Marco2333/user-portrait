from pymongo import MongoClient
from portrayal import UserProfile
from crawler import crawler


def restore():
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

	for item in [586671909]:
		print item
		
		if item in res_temp:
			continue

		
		user = crawler.get_user_all_info(user_id = item)
		user = UserProfile.UserProfileFromDic(user)

		user['_id'] = long(user['user_id'])
		del user['user_id']

		collect2.insert_one(user)


def comparison():
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']

	collect1 = db['typical']
	collect2 = db['typical_temp']

	tus = collect1.find({}, {'category': 1})

	res = []

	file = open('file/output.txt', 'w')
	for item in tus:
		user = collect2.find_one({'_id': item['_id']}, {'category': 1})
		if not user:
			continue

		if item['category'] != user['category']:
			res.append(item['_id'])
			file.write(str(item['_id']))
			file.write("\n")

	print res
	print len(res)


if __name__ == '__main__':
	comparison()