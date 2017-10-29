# -*- coding:utf-8 -*-

import MySQLdb

from config import MYSQL, MONGO_DB, NEO4J
from pymongo import MongoClient

class Mysql:
	def connect(self):
		db = MySQLdb.connect(MYSQL['DB_HOST'], MYSQL['DB_USER'], MYSQL['DB_PASSWORD'], MYSQL['DB_DATABASE'])
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		return db

	def execute(self, sql):
		self.cursor.execute(sql)
		self.db.commit()

	def fetchall(self, sql):
		self.cursor.execute(sql)
		res = self.cursor.fetchall()

		return res

	def close(self):
		self.db.close()


class MongoDB:
	def connect(self, db_name = MONGO_DB['DB_DATABASE']):
		client = MongoClient(MONGO_DB['DB_HOST'], MONGO_DB['DB_PORT'])
		db = client[db_name]
		db.authenticate(MONGO_DB['DB_USER'], MONGO_DB['DB_PASSWORD'])
		self.db = db

		return db


class Neo4j:
	def connect(self):
		graph = Graph(NEO4J['DB_HOST'], 
					 username = NEO4J['DB_USER'], 
					 password = NEO4J['DB_PASSWORD'])

		return graph