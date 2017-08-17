from py2neo import Graph, Node, Relationship

from app.database import Neo4j, Mysql, MongoDB

def create_relation():
	graph = Neo4j().connect()
	mysql = Mysql().connect()
	mongo = MongoDB().connect()

	tus = mongo['typical'].find({}, {'_id': 1})

	for item in tus:
		user = Node(label = "TypicalUser", _id = item['_id'])
		graph.create(user)



	# relation = mysql.fetchall('select * from relation')



if __name__ == '__main__':
	create_relation()