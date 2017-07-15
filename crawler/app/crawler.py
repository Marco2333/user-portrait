from database import Mysql
from basicinfo_crawler import BasicinfoCrawler
from tweets_crawler import TweetsCrawler

basicinfo_crawler = BasicinfoCrawler()
tweets_crawler = TweetsCrawler()


def get_users_basicinfo(user_list, table_name = "user", search_type = "user_id"):
	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_basicinfo_from_file(file_name, table_name = "user", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_basicinfo_from_db(sql, table_name = "user", search_type = "user_id"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_tweets(user_list, collect_name = "tweets", search_type = "user_id"):
	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def get_users_tweets_from_file(file_name, collect_name = "tweets", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def get_users_tweets_from_db(sql, collect_name = "tweets", search_type = "screen_name"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)

		
if __name__ == "__main__":
	# name_list = ['YESBANK', 'TheOfficialSBI', 'NYSE', 'wrausahamandiri', 'kickstarter']