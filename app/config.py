# -*- coding:utf-8 -*-

PROJECT_PATH = "F:/python/user-portrait/app/"

# MySQL配置
MYSQL = {
	'DB_USER': 'root',
	'DB_PASSWORD': 'aliyunmysql@',
	# 'DB_PASSWORD': '283319',
	'DB_HOST': '127.0.0.1',
	'DB_DATABASE': 'twitter',
	'DB_CHARSET': 'utf8mb4'
}

# MongoDB配置
MONGO_DB = {
	'DB_HOST': '127.0.0.1',
	'DB_PORT': 27017,
	'DB_DATABASE': 'flask_crawler'
}

# Neo4j配置
NEO4J = {
	'DB_USER': 'neo4j',
	'DB_PASSWORD': 'aliyunneo4j@',
	'DB_HOST': 'http://localhost:7474',
}