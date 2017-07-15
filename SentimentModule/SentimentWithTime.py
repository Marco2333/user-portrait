#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import time
import sys
sys.path.append("..")
from MongoDBInteraction import TweetsWithMongo as mongo

# 从mongodb中读出的日期是 "Fri Dec 16 04:22:58 +0000 2016"
import datetime
import SentimentAnalyze as Senti
import config

months = config.months
# 将字符串格式转换成可以转换成datetime的字符串格式
def Str2Time(str):
    strs = str.split(" ")
    week = strs[0]
    month = months[strs[1]]
    day = strs[2]
    time = strs[3]
    year = strs[5]
    DateTime = year + '-' + month + '-' + day + ' ' + time
    return DateTime

# 计算两个时间之间的差
def CalcTime(date1,date2):
    date1 = time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2 = datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])

    return abs((date2 - date1).days)

# 获取一个用户获取的推文中其所有的时间
def getTimeSequence(userid):
    count = 0
    Time = []

    tweets = mongo.getTweets(userid)
    if tweets.count() == 0:
        print "没有推文"
        return
    # 获取从抓取时间向前2个月的推文
    for tweet in tweets[1:]:
        # if(CalcTime(Str2Time(tweet['created_at']),starttime) > threshold):
        #     break
        Time.append(Str2Time(tweet['created_at']))
        count += 1

    days = CalcTime(Time[0],Time[len(Time) - 1])
    # print "相隔了%d天" % days
    # print "推文条数%d" % count
    return Time

# 以两个月为一个周期,获取周期性的心理状态
def getTweetsByMonths(tweets,period):
    '''

    :param userid:用户id
    :param period: 周期月数
    :return:返回最新推文起始时间以及每个周期内的推文
    '''
    # count表示推文条数
    count = 0
    threshold = period * 30
    if tweets == None:
        print "没有推文"
        return
    # 最开始的一条推文起始时间
    starttime = Str2Time(tweets[0]['created_at'])
    period_tweets = []
    temp_starttime = starttime
    temp_period_text = ""
    for tweet in tweets:
        time = Str2Time(tweet['created_at'])
        # 在周期内,推文加入
        if CalcTime(time,temp_starttime) <= threshold:
            temp_period_text += tweet['text']
        else:
        # 否则重新记录起始时间
            temp_starttime = time
            period_tweets.append(temp_period_text)
            temp_period_text = ""
        count += 1
    # 最后要把临时获取的推文加入
    if(temp_period_text != ""):
        period_tweets.append(temp_period_text)
    # print "共有%d个周期" % len(period_tweets)
    # print "推文数%d条" % count
    return starttime,period_tweets

# 对外接口
# 加入时间后的推文情感分类
def SentimentWithTime(tweets,period=1):
    '''

    :param userid:用户id
    :param period: 时间间隔的月数(默认参数1个月)
    :return:返回最开始推文起始时间和每个周期的心理状态以及总体心理状态结果
    '''
    starttime,period_tweets = getTweetsByMonths(tweets,period)
    psychologic = []
    neg = pos = 0
    for tweet in period_tweets:
        res,confidence = Senti.sentiment(tweet)
        if res == 'pos':
            pos += 1
        else:
            neg += 1
        psychologic.append(res)

    if (len(period_tweets) == 0):
        res = 0
        return starttime,psychologic,res

    # print pos * 1.0 / len(period_tweets)
    if pos * 1.0 / len(period_tweets) > 0.5:
        res =  1
    else:
        res = -1

    return starttime,psychologic,res

