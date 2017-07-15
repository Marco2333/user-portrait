import MySQLdb

from config import MYSQL
from pymongo import MongoClient

class Mysql:
	def connect(self):
		db = MySQLdb.connect(MYSQL['DB_HOST'], MYSQL['DB_USER'], MYSQL['DB_PASSWD'], MYSQL['DB_DATABASE'])
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
	def connect(self, db_name = 'twitter'):
		client = MongoClient('127.0.0.1', 27017)
		db = client[db_name]
		self.db = db

		return db

	# def close(self):

