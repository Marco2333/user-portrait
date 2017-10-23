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
	db = client['dump']

	collect1 = db['typical']
	collect2 = db['typical_temp']

	tus = collect1.find({}, {'category': 1})

	res = []

	file = open('output/output.txt', 'w')
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


def setSame():
	client = MongoClient('127.0.0.1', 27017)
	db = client['dump']

	collect1 = db['typical']
	collect2 = db['typical_temp']

	tus = collect1.find({}, {'category': 1})

	for item in tus:
		collect2.update({'_id':item['_id']},{"$set": {'category':item['category']}})


def getSpecialCategory():
	client = MongoClient('127.0.0.1', 27017)
	db = client['dump']

	collect1 = db['typical']

	tus = collect1.find({"$or": [{'category': 'Politics'}, {'category': 'Military'}, 
		{'category': 'Religion'}], 'friends_count': {"$lt": 200}}, {'_id': 1, 'friends_count': 1})

	file = open('output/output.txt', 'w')
	for item in tus:
		file.write(str(item['_id']))
		file.write("\n")


def deleteRepeat(user_list):
	ml = list(set(user_list))
	print len(ml)

	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']
	collect1 = db['twitter_tt']

	res = collect1.find({}, {"screen_name": 1})
	res_t = []
	for item in res:
		res_t.append(item['screen_name'])

	print len(res_t)

	res_t = set(res_t)

	file = open('file/m_o.txt', 'w')
	for item in ml:
		if item not in res_t:
			file.write(item + "\n")
		else:
			print item


def portrait_new_users(user_list):
	client = MongoClient('127.0.0.1', 27017)
	db = client['twitter']

	collect = db['typical_new_1']
	collect1 = db['typical']

	for item in user_list:
		print item
		s = collect1.find_one({'screen_name': item})
		if s != None:
			continue

		user = crawler.get_user_all_info(screen_name = item)
		user = UserProfile.UserProfileFromDic(user)

		user['_id'] = long(user['user_id'])
		del user['user_id']

		try:
			collect.insert_one(user)
		except Exception as e:
			print e
			continue



if __name__ == '__main__':
	file = open('file/tx.txt')

	user_list = []
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break
		for line in lines:
			user_list.append(line.strip())

	user_list = list(set(user_list))
	portrait_new_users(user_list)