#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import config
class User:
    def __init__(self,id,screen_name,name,location,statuses_count,friends_count,followers_count,favourites_count,verified,category,influenceScore,rank_influ,psy,psy_seq,psy_tweets_starttime,interest_tags,desciption,crawler_date,time_zone,activity):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
        self.favourites_count = favourites_count
        self.location = location
        self.verified = verified
        self.category = category
        self.influenceScore = influenceScore
        # rank_influ 1:低  2:中  3:高
        self.rank_influ = rank_influ
        # psy 1:正面 0:负面
        self.psy = psy
        # 心理状态序列
        self.psy_seq = psy_seq
        # 最新一条推文起始时间
        self.psy_tweets_starttime = psy_tweets_starttime
        # 兴趣爱好标签
        self.interest_tags = interest_tags
        # 个人简介
        self.description = desciption
        # 人物抓取时间
        self.crawler_date = crawler_date
        # 所处的时区
        self.time_zone = time_zone
        # 活跃度
        self.activity = activity

    def getProportion(self):
        if self.friends_count != 0:
            return (self.followers_count) * 1.0 / self.friends_count
        else:
            return (self.followers_count) * 1.0 / 0.1

    # 获取该类所有属性
    def list_all_members(self):
        attributes = []
        for name,value in vars(self).items():
            attributes.append(name)
        return attributes

    def __str__(self):
        if self.verified == 1:
            verify = "yes"
        else:
            verify = "no"
        if self.location == "":
            location = "no file"
        else:
            location = self.location
        return "用户id:%s  screen_name:%s  姓名:%s  是否认证:%s  地理位置:%s  粉丝数:%d  关注人数:%d  推文数:%d  点赞数:%d   影响力分数:%f   影响力等级:%s   近期心理状态:%s   兴趣爱好标签:%s   个人简介:%s   所属领域:%s   人物抓取时间:%s   所处的时区:%s   活跃度为:%f" % (self.id,self.screen_name,self.name,verify,location,self.followers_count,self.friends_count,self.statuses_count,self.favourites_count,self.influenceScore,config.rank_influence[self.rank_influ],config.psychological[self.psy],self.interest_tags,self.description,self.category,self.crawler_date,self.time_zone,self.activity)