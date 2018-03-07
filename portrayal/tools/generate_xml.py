# -*- coding:utf-8 -*-
import sys
import xml.dom.minidom

from .. config import PROJECT_PATH, XML_PATH

# reload(sys)
# sys.setdefaultencoding('utf8')

# 获取DOM树实现对象
impl = xml.dom.minidom.getDOMImplementation()

# 生成用户的XML文件
def generate_user_xml(user):
	dom = impl.createDocument(None, 'TwitterUser', None)
	root = dom.documentElement

	# 创建子节点
	basic_info = dom.createElement('基础信息')
	implicit_info = dom.createElement('隐性属性')
	root.appendChild(basic_info)
	root.appendChild(implicit_info)


	# id
	id_ele = dom.createElement('用户ID')

	if user.has_key('_id'):
		id_text = dom.createTextNode(str(user['_id']))
	else:
		id_text = dom.createTextNode(str(user['user_id']))

	id_ele.appendChild(id_text)


	# screen_name
	sn_ele = dom.createElement('screen_name')
	sn_text = dom.createTextNode(user['screen_name'])
	sn_ele.appendChild(sn_text)


	# name
	name_ele = dom.createElement('name')
	# 标签增加属性,设置编码方式
	# name_ele.setAttribute("coding", "utf-8")
	_name = user['name'] if user['name'] else ''
	name_text = dom.createTextNode(_name)
	name_ele.appendChild(name_text)


	# 个人描述
	des_ele = dom.createElement('简介')
	_description = user['description'] if user['description'] else ''
	des_text = dom.createTextNode(_description)
	des_ele.appendChild(des_text)


	# 地理位置
	location_ele = dom.createElement('地理位置')
	_location = user['location'] if user['location'] else ''
	location_text = dom.createTextNode(_location)
	location_ele.appendChild(location_text)


	# 帐号创建日期
	create_ele = dom.createElement('帐号创建日期')
	create_text = dom.createTextNode(str(user['created_at']))
	create_ele.appendChild(create_text)


	# 粉丝数
	follower_ele = dom.createElement('粉丝数')
	follower_text = dom.createTextNode(str(user['followers_count']))
	follower_ele.appendChild(follower_text)


	# 朋友数
	friends_ele = dom.createElement('朋友数')
	friends_text = dom.createTextNode(str(user['friends_count']))
	friends_ele.appendChild(friends_text)


	# 推文数
	status_ele = dom.createElement('推文数')
	status_text = dom.createTextNode(str(user['statuses_count']))
	status_ele.appendChild(status_text)


	# 喜欢的推文数
	favourite_ele = dom.createElement('喜欢的推文数')
	favourite_text = dom.createTextNode(str(user['favourites_count']))
	favourite_ele.appendChild(favourite_text)


	# 列表数量
	list_ele = dom.createElement('所属列表数')
	list_text = dom.createTextNode(str(user['listed_count']))
	list_ele.appendChild(list_text)


	# 是否认证
	verified_ele = dom.createElement('官方认证')
	verified_text = dom.createTextNode(str(user['verified']))
	verified_ele.appendChild(verified_text)


	# 隐私保护
	pro_ele = dom.createElement('隐私保护')
	pro_text = dom.createTextNode(str(user['protected']))
	pro_ele.appendChild(pro_text)


	#地理位置共享
	geo_enabled_ele = dom.createElement('地理位置共享')
	geo_enabled_text = dom.createTextNode(str(user['geo_enabled']))
	geo_enabled_ele.appendChild(geo_enabled_text)


	# 使用语言
	lang_ele = dom.createElement('语言')
	_lang = user['lang'] if user['lang'] else ''
	lang_text = dom.createTextNode(_lang)
	lang_ele.appendChild(lang_text)


	# 时区
	time_zone = dom.createElement('时区')
	_time_zone = user['time_zone'] if user['time_zone'] else ''
	time_text = dom.createTextNode(_time_zone)
	time_zone.appendChild(time_text)


	# 国际协调时偏移量
	utc_ele = dom.createElement('国际协调时偏移量')
	utc_text = dom.createTextNode(str(user['utc_offset']))
	utc_ele.appendChild(utc_text)


	# 是否使用默认头像
	default_ele = dom.createElement('是否使用默认头像')
	default_text = dom.createTextNode(str(user['default_profile_image']))
	default_ele.appendChild(default_text)


	# 头像链接
	profile_ele = dom.createElement('头像链接')
	profile_text = dom.createTextNode(user['profile_image_url'])
	profile_ele.appendChild(profile_text)


	# 背景图片链接
	banner_ele = dom.createElement('背景图片链接')
	_profile_banner_url = user['profile_banner_url'] if user['profile_banner_url'] else ''
	banner_text = dom.createTextNode(_profile_banner_url)
	banner_ele.appendChild(banner_text)

	
	# 主页背景颜色
	bgcolor_ele = dom.createElement('主页背景颜色')
	bgcolor_text = dom.createTextNode(user['profile_background_color'])
	bgcolor_ele.appendChild(bgcolor_text)


	#侧边栏填充颜色
	profile_sidebar_ele = dom.createElement('侧边栏填充颜色')
	profile_sidebar_text = dom.createTextNode(user['profile_sidebar_fill_color'])
	profile_sidebar_ele.appendChild(profile_sidebar_text)
	

	#抓取到的推文数
	tweets_crawled_ele = dom.createElement('抓取到的推文数')
	tweets_crawled_text = dom.createTextNode(str(len(user['tweets'])))
	tweets_crawled_ele.appendChild(tweets_crawled_text)


	#已抓取推文开始时间
	tweets_crawled_start_ele = dom.createElement('已抓取推文开始时间')
	tweets_crawled_start_text = dom.createTextNode(user['tweets'][0]['created_at'] if len(user['tweets']) > 0 else '')
	tweets_crawled_start_ele.appendChild(tweets_crawled_start_text)


	#已抓取推文结束时间
	tweets_crawled_end_ele = dom.createElement('已抓取推文结束时间')
	tweets_crawled_end_text = dom.createTextNode(user['tweets'][-1]['created_at'] if len(user['tweets']) > 0 else '')
	tweets_crawled_end_ele.appendChild(tweets_crawled_end_text)


	# 抓取日期
	crawler_date_ele = dom.createElement('抓取日期')
	crawler_date_text = dom.createTextNode(str(user['crawler_date']))
	crawler_date_ele.appendChild(crawler_date_text)


	# 把基本信息加入到basic_info节点中
	basic_info.appendChild(id_ele)
	basic_info.appendChild(sn_ele)
	basic_info.appendChild(name_ele)
	basic_info.appendChild(des_ele)
	basic_info.appendChild(location_ele)
	basic_info.appendChild(create_ele)
	basic_info.appendChild(follower_ele)
	basic_info.appendChild(friends_ele)
	basic_info.appendChild(status_ele)
	basic_info.appendChild(favourite_ele)
	basic_info.appendChild(list_ele)
	basic_info.appendChild(verified_ele)
	basic_info.appendChild(pro_ele)
	basic_info.appendChild(geo_enabled_ele)
	basic_info.appendChild(lang_ele)
	basic_info.appendChild(time_zone)
	basic_info.appendChild(utc_ele)
	basic_info.appendChild(default_ele)
	basic_info.appendChild(profile_ele)
	basic_info.appendChild(banner_ele)
	basic_info.appendChild(bgcolor_ele)
	basic_info.appendChild(profile_sidebar_ele)
	basic_info.appendChild(tweets_crawled_ele)
	basic_info.appendChild(tweets_crawled_start_ele)
	basic_info.appendChild(tweets_crawled_end_ele)
	basic_info.appendChild(crawler_date_ele)
	
	

	# 职业领域分类
	category_ele = dom.createElement("职业领域")
	category_text = dom.createTextNode(user['category'])
	category_ele.appendChild(category_text)


	# 职业领域得分
	category_score_ele = dom.createElement("职业领域得分")
	category_score_str = ''

	for item in user['category_score']:
		category_score_str += item + ": " + str(user['category_score'][item]) + "; "

	category_score_text = dom.createTextNode(category_score_str[0:-2])
	category_score_ele.appendChild(category_score_text)


	# 用户社交影响力
	influence_ele = dom.createElement("影响力分数")
	influence_text = dom.createTextNode(str(user['influence_score']))
	influence_ele.appendChild(influence_text)


	if user['influence_score'] >= 110:
		influence_rank = '高'
	elif user['influence_score'] >= 60:
		influence_rank = '中'
	else:
		influence_rank = '低'
	# 用户社交影响力大小
	influence_rank_ele = dom.createElement("影响力等级")
	influence_rank_text = dom.createTextNode(influence_rank)
	influence_rank_ele.appendChild(influence_rank_text)


	# 用户心里状态标签
	psy_ele = dom.createElement("心理状态")

	if user['psy'] == 1:
		psy_temp = '正面'
	elif user['psy'] == -1:
		psy_temp = '负面'
	else:
		psy_temp = '中性'

	psy_text = dom.createTextNode(psy_temp)
	psy_ele.appendChild(psy_text)


	# 用户兴趣爱好标签
	interest_ele = dom.createElement("兴趣爱好标签")
	interest_text = dom.createTextNode(user['interest_tags'])
	interest_ele.appendChild(interest_text)


	# 活跃度
	activity_ele = dom.createElement("活跃度")
	activity_text = dom.createTextNode(str(user['activity']))
	activity_ele.appendChild(activity_text)


	# 活跃度变化
	activity_list_ele = dom.createElement("活跃度变化")
	activity_list_str = ''

	for item in user['activity_list']:
		activity_list_str += str(item) + ", "

	activity_list_text = dom.createTextNode(activity_list_str[0:-2])
	activity_list_ele.appendChild(activity_list_text)


	# 心理状态变化(相同推文数，方法1)
	psy_with_count1_ele = dom.createElement("心理状态变化")
	psy_with_count1_ele.setAttribute("type", "相同推文数")
	psy_with_count1_ele.setAttribute("method", "分类器分类")
	psy_with_count1_str = ''

	for item in user['psy_with_count1']:
		psy_with_count1_str += str(item) + ", "

	psy_with_count1_text = dom.createTextNode(psy_with_count1_str[0:-2])
	psy_with_count1_ele.appendChild(psy_with_count1_text)


	# 心理状态变化(相同推文数，方法2)
	psy_with_count2_ele = dom.createElement("心理状态变化")
	psy_with_count2_ele.setAttribute("type", "相同推文数")
	psy_with_count2_ele.setAttribute("method", "情感字典")
	psy_with_count2_str = ''

	for item in user['psy_with_count2']:
		psy_with_count2_str += str(item) + ", "

	psy_with_count2_text = dom.createTextNode(psy_with_count2_str[0:-2])
	psy_with_count2_ele.appendChild(psy_with_count2_text)


	# 心理状态变化(相同时间间隔，方法1)
	psy_with_time1_ele = dom.createElement("心理状态变化")
	psy_with_time1_ele.setAttribute("type", "相同时间间隔")
	psy_with_time1_ele.setAttribute("method", "分类器分类")
	psy_with_time1_str = ''

	for item in user['psy_with_time1']:
		psy_with_time1_str += str(item) + ", "

	psy_with_time1_text = dom.createTextNode(psy_with_time1_str[0:-2])
	psy_with_time1_ele.appendChild(psy_with_time1_text)


	# 心理状态变化(相同时间间隔，方法2)
	psy_with_time2_ele = dom.createElement("心理状态变化")
	psy_with_time2_ele.setAttribute("type", "相同时间间隔")
	psy_with_time2_ele.setAttribute("method", "情感字典")
	psy_with_time2_str = ''

	for item in user['psy_with_time2']:
		psy_with_time2_str += str(item) + ", "

	psy_with_time2_text = dom.createTextNode(psy_with_time2_str[0:-2])
	psy_with_time2_ele.appendChild(psy_with_time2_text)


	# 将隐性属性标签加入到隐性标签中
	implicit_info.appendChild(category_ele)
	implicit_info.appendChild(category_score_ele)
	implicit_info.appendChild(influence_ele)
	implicit_info.appendChild(influence_rank_ele)
	implicit_info.appendChild(psy_ele)
	implicit_info.appendChild(interest_ele)
	implicit_info.appendChild(activity_ele)
	implicit_info.appendChild(activity_list_ele)
	implicit_info.appendChild(psy_with_count1_ele)
	implicit_info.appendChild(psy_with_count2_ele)
	implicit_info.appendChild(psy_with_time1_ele)
	implicit_info.appendChild(psy_with_time2_ele)


	# 将用户信息写入文件
	with open(XML_PATH + '%s.xml' % user['screen_name'], 'w') as f:
		dom.writexml(f, addindent="    ", newl='\n', encoding="utf-8")


	return XML_PATH + '%s.xml' % user['screen_name']