# coding=utf-8
from py2neo import Graph, Node, Relationship
from crawler.database import Neo4j, MongoDB


'''
创建neo4j节点及关系
'''
def create_relation():
	graph = Neo4j().connect()
	mongo = MongoDB().connect()

	# 清空neo4j数据库
	# graph = graph.delete_all()

	tus = mongo['typical'].find({}, {'_id': 1})

	for item in tus:
		# 创建用户节点
		user = Node("Typical", user_id = item['_id'])
		graph.create(user)

	tus = mongo['relation'].find({}, {'_id': 1})
	user_list = map(lambda item: item['_id'], tus)

	# 创建用户节点之间的关系
	for user_id in user_list:
		friends = mongo['relation'].find_one({'_id': user_id})
		friends = set(friends['friends'])

		node1 = graph.find_one("Typical",
							   property_key = "user_id",
							   property_value = user_id)

		for user_id1 in user_list:
			if user_id1 == user_id:
				continue

			if user_id1 in friends:
				node2 = graph.find_one("Typical",
									   property_key = "user_id",
  									   property_value = user_id1)

				following = Relationship(node1, 'following', node2)
				graph.create(following)


'''
更新neo4j节点属性
'''
def update_attr():
	graph = Neo4j().connect()
	mongo = MongoDB().connect()

	tus = mongo['typical'].find({}, {'name': 1, 'category': 1, 'followers_count': 1, 'location': 1, 'utc_offset': 1, 
		'statuses_count': 1, 'description': 1, 'friends_count': 1, 'psy': 1, 'verified': 1, 'lang': 1, 'favourites_count': 1, 
		'screen_name': 1, 'influence_score': 1, 'created_at': 1, 'time_zone': 1, 'protected': 1, 'activity': 1})

	for item in tus:
		node = graph.find_one("Typical",
							  property_key = "user_id",
							  property_value = item['_id'])
		node['name'] = item['name']
		node['category'] = item['category']
		node['followers_count'] = item['followers_count']
		node['location'] = item['location']
		node['utc_offset'] = item['utc_offset']
		node['statuses_count'] = item['statuses_count']
		node['description'] = item['description']
		node['friends_count'] = item['friends_count']
		node['psy'] = item['psy']
		node['verified'] = item['verified']
		node['lang'] = item['lang']
		node['favourites_count'] = item['favourites_count']
		node['screen_name'] = item['screen_name']
		node['influence_score'] = item['influence_score']
		node['created_at'] = item['created_at']
		node['time_zone'] = item['time_zone']
		node['protected'] = item['protected']
		node['activity'] = item['activity']

		graph.push(node)


if __name__ == '__main__':
	# create_relation()
	update_attr()