# -*- coding:utf-8 -*-
import sys
import xml.dom.minidom

from .. config import PROJECT_PATH, XML_PATH

reload(sys)
sys.setdefaultencoding('utf8')


# 获取DOM树实现对象
impl = xml.dom.minidom.getDOMImplementation()

# 生成某一用户的XML文件
def generate_user_xml(user):
	dom = impl.createDocument(None, 'TwitterUser', None)
	root = dom.documentElement

	# 创建子节点
	basic_info = dom.createElement('基础信息')
	implicit_info = dom.createElement('隐性属性')
	root.appendChild(basic_info)
	root.appendChild(implicit_info)

	# id 节点
	id_ele = dom.createElement('用户ID')

	if user.has_key('_id'):
		id_text = dom.createTextNode(str(user['_id']))
	else:
		id_text = dom.createTextNode(str(user['user_id']))
	id_ele.appendChild(id_text)

	# 姓名节点标签
	name_ele = dom.createElement('name')
	# 标签增加属性
	name_ele.setAttribute("coding", "utf-8")

	# 姓名标签内容,将编码方式转换一下
	name_text = dom.createTextNode(user['name'])
	# 将内容加入标签中
	name_ele.appendChild(name_text)

	# screen_name 节点
	sn_ele = dom.createElement('screen_name')
	sn_text = dom.createTextNode(user['screen_name'])
	sn_ele.appendChild(sn_text)

	# id 节点
	location_ele = dom.createElement('地理位置')
	if user['location'] != "":
		location_text = dom.createTextNode(user['location'])
	else:
		location_text = dom.createTextNode("空")
	location_ele.appendChild(location_text)

	# 是否认证节点
	verified_ele = dom.createElement('官方认证')
	if user['verified']:
		verified = '已认证'
	else:
		verified = '未认证'
	verified_text = dom.createTextNode(verified)
	verified_ele.appendChild(verified_text)

	# 使用语言
	lang_ele = dom.createElement('语言')
	lang_text = dom.createTextNode(user['lang'])
	lang_ele.appendChild(lang_text)

	# 国际协调时间
	utc_ele = dom.createElement('国际协调时偏移量')
	utc_text = dom.createTextNode(str(user['utc_offset']))
	utc_ele.appendChild(utc_text)

	# 隐私保护
	pro_ele = dom.createElement('隐私保护')
	pro_text = dom.createTextNode(str(user['protected']))
	pro_ele.appendChild(pro_text)

	# 主页背景颜色
	bgcolor_ele = dom.createElement('主页背景颜色')
	bgcolor_text = dom.createTextNode(user['profile_background_color'])
	bgcolor_ele.appendChild(bgcolor_text)

	# 帐号创建日期
	create_ele = dom.createElement('帐号创建日期')
	create_text = dom.createTextNode(str(user['created_at']))
	create_ele.appendChild(create_text)

	# 背景图片链接
	banner_ele = dom.createElement('背景图片链接')
	banner_text = dom.createTextNode(user['profile_banner_url'])
	banner_ele.appendChild(banner_text)

	# 头像链接
	profile_ele = dom.createElement('头像链接')
	profile_text = dom.createTextNode(user['profile_image_url'])
	profile_ele.appendChild(profile_text)

	# 是否使用默认头像图片
	default_ele = dom.createElement('是否使用默认头像')
	default_text = dom.createTextNode(str(user['default_profile_image']))
	default_ele.appendChild(default_text)

	# 时区
	time_zone = dom.createElement('时区')
	time_text = dom.createTextNode(str(user['time_zone']))
	time_zone.appendChild(time_text)

	# 粉丝数 节点
	follower_ele = dom.createElement('粉丝数')
	follower_text = dom.createTextNode(str(user['followers_count']))
	follower_ele.appendChild(follower_text)

	# 朋友数 节点
	friends_ele = dom.createElement('朋友数')
	friends_text = dom.createTextNode(str(user['friends_count']))
	friends_ele.appendChild(friends_text)

	# 推文数 节点
	status_ele = dom.createElement('推文数')
	status_text = dom.createTextNode(str(user['statuses_count']))
	status_ele.appendChild(status_text)

	# 点赞次数数 节点
	favourite_ele = dom.createElement('喜欢的推文数')
	favourite_text = dom.createTextNode(str(user['favourites_count']))
	favourite_ele.appendChild(favourite_text)

	# 个人描述
	des_ele = dom.createElement('简介')
	des_text = dom.createTextNode(str(user['description']))
	des_ele.appendChild(des_text)

	# 抓取日期
	crawler_date_ele = dom.createElement('抓取日期')
	crawler_date_text = dom.createTextNode(str(user['crawler_date']))
	crawler_date_ele.appendChild(crawler_date_text)

	# 把基本信息加入到basic_info节点中
	basic_info.appendChild(id_ele)
	basic_info.appendChild(name_ele)
	basic_info.appendChild(sn_ele)
	basic_info.appendChild(location_ele)
	basic_info.appendChild(verified_ele)
	basic_info.appendChild(lang_ele)
	basic_info.appendChild(utc_ele)
	basic_info.appendChild(des_ele)
	basic_info.appendChild(pro_ele)
	basic_info.appendChild(bgcolor_ele)
	basic_info.appendChild(create_ele)
	basic_info.appendChild(banner_ele)
	basic_info.appendChild(time_zone)
	basic_info.appendChild(profile_ele)
	basic_info.appendChild(default_ele)
	basic_info.appendChild(follower_ele)
	basic_info.appendChild(friends_ele)
	basic_info.appendChild(favourite_ele)
	basic_info.appendChild(status_ele)
	basic_info.appendChild(crawler_date_ele)

	# 用户类别
	category_ele = dom.createElement("职业领域")
	category_text = dom.createTextNode(user['category'])
	category_ele.appendChild(category_text)

	# 用户心里状态标签
	psy_ele = dom.createElement("近期心理状态")
	psy_text = dom.createTextNode(str(user['psy']))
	psy_ele.appendChild(psy_text)

	# 用户兴趣爱好标签
	interest_ele = dom.createElement("兴趣爱好")
	interest_text = dom.createTextNode(user['interest_tags'])
	interest_ele.appendChild(interest_text)

	# 用户社交影响力标签
	influence_ele = dom.createElement("影响力分数")
	influence_text = dom.createTextNode(str(user['influence_score']))
	influence_ele.appendChild(influence_text)

	activity_ele = dom.createElement("活跃度")
	activity_text = dom.createTextNode(str(user['activity']))
	activity_ele.appendChild(activity_text)

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

	# 将隐性属性标签加入到隐性标签中
	implicit_info.appendChild(category_ele)
	implicit_info.appendChild(psy_ele)
	implicit_info.appendChild(interest_ele)
	implicit_info.appendChild(influence_ele)
	implicit_info.appendChild(influence_rank_ele)

	# 将用户信息写入文件
	with open(XML_PATH + '%s.xml' % user['screen_name'], 'w') as f:
		dom.writexml(f, addindent=" ", newl='\n')

	return XML_PATH + '%s.xml' % user['screen_name']