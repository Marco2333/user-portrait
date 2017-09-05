from app.database import MongoDB
from app.portrayal.career_classify import training, classify

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
	# db = MongoDB().connect('dump')

	# users = db['typical_temp'].find({'category': 'Education'})

	# # file = open('education.txt', 'w')

	# n = 0
	# for user in users:
	# 	print user['screen_name']
	# 	tweets = user['tweets']

	# 	text = user['description']
	# 	for tweet in tweets:
	# 		text += ' ' + tweet['text']

	# 	text = re.sub(r'^RT @\w+:|@\w+|#|(ht|f)tp[^\s]+', "", text)
	# 	res = classify.classify(text)

	# 	print res
	# 	if res[0] == user['category']:
	# 		n += 1
	# 		# try:
	# 		# 	file.write(text + '\n')
	# 		# except:
	# 		# 	continue

	# print n
	training.training()