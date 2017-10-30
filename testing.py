#coding=utf-8
from crawling import get_user_all_info
from portrayal.user_profile import user_profile


def main():
	# pass
	user = get_user_all_info(screen_name = 'David_Cameron')
	user = user_profile(user)
	del user['tweets']
	print user



if __name__ == '__main__':
	main()