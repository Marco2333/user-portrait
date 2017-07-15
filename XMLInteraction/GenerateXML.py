#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import xml.dom.minidom
import sys
import config
reload(sys)
sys.setdefaultencoding('utf8')

project_path = config.project_path

# 获取DOM树实现对象
impl = xml.dom.minidom.getDOMImplementation()

# 生成某一用户的XML文件
def GenerateUserXml(twitter_user):
    '''

    :param twitter_user: 字典形式
    :return:
    '''

    dom = impl.createDocument(None,'TwitterUser',None)
    root = dom.documentElement

    # 创建子节点
    BasicInfo = dom.createElement('基本信息')
    ImplicitInfo = dom.createElement('隐性属性')
    root.appendChild(BasicInfo)
    root.appendChild(ImplicitInfo)

    # id 节点
    IdE = dom.createElement('user_id')
    IdT = dom.createTextNode(twitter_user['user_id'])
    IdE.appendChild(IdT)
    #
    # 姓名节点标签
    nameE = dom.createElement('name')
    # 标签增加属性
    nameE.setAttribute("coding","utf-8")

    # 姓名标签内容,将编码方式转换一下
    nameT = dom.createTextNode(twitter_user['name'])
    # 将内容加入标签中
    nameE.appendChild(nameT)

    # scrren_name 节点
    SNE = dom.createElement('screen_name')
    SNT = dom.createTextNode(twitter_user['screen_name'])
    SNE.appendChild(SNT)

    # id 节点
    LoE = dom.createElement('地理位置')
    if twitter_user.location != "" and twitter_user != None:
        LoT = dom.createTextNode(twitter_user['location'])
    else:
        LoT = dom.createTextNode("空")
    LoE.appendChild(LoT)

    # 是否认证节点
    VerE = dom.createElement('是否认证过')
    if twitter_user.verified == 1:
        verified = '是'
    else:
        verified = '否'
    VerT = dom.createTextNode(verified)
    VerE.appendChild(VerT)

    # 使用语言
    LangE = dom.createElement('使用语言')
    LangT = dom.createTextNode(str(twitter_user['lang']))
    LangE.appendChild(LangT)

    # 国际协调时间
    UTCE = dom.createElement('国际协调时间')
    UTCT = dom.createTextNode(str(twitter_user['utc_offset']))
    UTCE.appendChild(LangT)

    # 推文是否受保护
    ProtectedE = dom.createElement('推文是否受保护')
    ProtectedT = dom.createTextNode(str(twitter_user['protected']))
    ProtectedE.appendChild(ProtectedT)

    # 主页背景颜色
    BcolorE = dom.createElement('主页背景颜色')
    BcolorT = dom.createTextNode(str(twitter_user['profile_background_color']))
    BcolorE.appendChild(BcolorT)

    # 帐号创建日期
    CreateE = dom.createElement('帐号创建日期')
    CreateT = dom.createTextNode(str(twitter_user['created_at']))
    CreateE.appendChild(CreateT)

    # 背景图片链接
    BannerE = dom.createElement('背景图片链接')
    BannerT = dom.createTextNode(str(twitter_user['profile_banner_url']))
    BannerE.appendChild(BannerT)

    # 头像图片链接
    ProfileIE = dom.createElement('头像图片链接')
    ProfileIT = dom.createTextNode(str(twitter_user['profile_image_url']))
    ProfileIE.appendChild(ProfileIT)

    # 是否使用默认头像图片
    DefaultE = dom.createElement('是否使用默认头像图片')
    DefaultT = dom.createTextNode(str(twitter_user['default_profile_image']))
    DefaultE.appendChild(DefaultT)

    # 时区
    TimeE = dom.createElement('时区')
    TimeT = dom.createTextNode(str(twitter_user['time_zone']))
    TimeE.appendChild(TimeT)

    # 粉丝数 节点
    FLE = dom.createElement('粉丝数')
    FLT = dom.createTextNode(str(twitter_user['followers_count']))
    FLE.appendChild(FLT)

    # 朋友数 节点
    FriendsE = dom.createElement('朋友数')
    FriendsT = dom.createTextNode(str(twitter_user['friends_count']))
    FriendsE.appendChild(FriendsT)

    # 推文数 节点
    STE = dom.createElement('推文数')
    STT = dom.createTextNode(str(twitter_user['statuses_count']))
    STE.appendChild(STT)

    # 点赞次数数 节点
    FAvE = dom.createElement('点赞数')
    FAvT = dom.createTextNode(str(twitter_user['favourites_count']))
    FAvE.appendChild(FAvT)

    # 个人描述
    DescriptionE = dom.createElement('个人简介')
    DescriptionT = dom.createTextNode(str(twitter_user['description']))
    DescriptionE.appendChild(DescriptionT)

    # 抓取日期
    Crawler_dateE = dom.createElement('抓取日期')
    Crawler_dateT = dom.createTextNode(str(twitter_user['crawler_date']))
    Crawler_dateE.appendChild(Crawler_dateT)

    # 把基本信息加入到BasicInfo节点中
    BasicInfo.appendChild(IdE)
    BasicInfo.appendChild(nameE)
    BasicInfo.appendChild(SNE)
    BasicInfo.appendChild(LoE)
    BasicInfo.appendChild(VerE)
    BasicInfo.appendChild(LangE)
    BasicInfo.appendChild(UTCE)
    BasicInfo.appendChild(DescriptionE)
    BasicInfo.appendChild(ProtectedE)
    BasicInfo.appendChild(BcolorE)
    BasicInfo.appendChild(CreateE)
    BasicInfo.appendChild(BannerE)
    BasicInfo.appendChild(TimeE)
    BasicInfo.appendChild(ProfileIE)
    BasicInfo.appendChild(DefaultE)
    BasicInfo.appendChild(FLE)
    BasicInfo.appendChild(FriendsE)
    BasicInfo.appendChild(FAvE)
    BasicInfo.appendChild(STE)
    BasicInfo.appendChild(Crawler_dateE)

    # 用户类别
    CategoryE = dom.createElement("用户领域")
    CategoryT = dom.createTextNode(twitter_user['category'])
    CategoryE.appendChild(CategoryT)

    # 用户心里状态标签
    FeelingE = dom.createElement("近期心理状态")
    FeelingT = dom.createTextNode(config.psychological[twitter_user['psy']])
    FeelingE.appendChild(FeelingT)

    # 用户兴趣爱好标签
    InterestE = dom.createElement("兴趣爱好")
    InterestT = dom.createTextNode(twitter_user['interest_tags'])
    InterestE.appendChild(InterestT)

    # 用户社交影响力标签
    InfluenceE = dom.createElement("影响力分数")
    InfluenceT = dom.createTextNode(str(twitter_user['influenceScore']))
    InfluenceE.appendChild(InfluenceT)

    # 用户社交影响力标签
    RankInfluE = dom.createElement("影响力等级")
    RankInfluT = dom.createTextNode(twitter_user['rank_influ'])
    RankInfluE.appendChild(RankInfluT)

    # 最新推文时间
    NewTweetE = dom.createElement("最新一条推文时间")
    NewTweetT = dom.createTextNode(twitter_user['psy_tweets_starttime'])
    NewTweetE.appendChild(NewTweetT)

    # 将隐性属性标签加入到隐性标签中
    ImplicitInfo.appendChild(CategoryE)
    ImplicitInfo.appendChild(FeelingE)
    ImplicitInfo.appendChild(InterestE)
    ImplicitInfo.appendChild(InfluenceE)
    ImplicitInfo.appendChild(RankInfluE)
    ImplicitInfo.appendChild(NewTweetE)

    # 将用户信息写入文件
    with open(config.XML_path + '%s.xml' % twitter_user['screen_name'],'w') as f:
        dom.writexml(f,addindent=" ",newl='\n')

# 生成XML文件
def GenerateUsersXml(users):
    count = 0
    for twitter_user in users:
    # 创建DOM树,'TwitterUsers'为根节点名称
        GenerateUserXml(twitter_user)
        count += 1
        print "finished %d users" % count
