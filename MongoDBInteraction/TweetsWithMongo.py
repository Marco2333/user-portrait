#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pymongo import MongoClient
from MySQLInteraction import TwitterWithMysql as mysql
import config
from TwitterUsers import TwitterUsers

# 连接文档数据库
def Conn():
    # connect to mongodb localhost
    client = MongoClient(config.mongo_host,config.mongo_port)
    # define the name of database
    db = client.twitterForTestInflu
    return db

# 根据用户id查找推文,userid是字符串格式
def getTweets(userid):
    db = Conn()
    # mongodb中没有找到该用户推文,返回None
    if(db.tweets.find({'user_id':long(userid)}).count() == 0):
        return None
    results = db.tweets.find({'user_id':long(userid)})
    return results

# 返回推文文本
def getUserTweets(userid,collection_name="tweets"):
    db = Conn()
    tweets = ""
    result = db[collection_name].find({"user_id":long(userid)})
    for res in result:
        tweets += res["text"]
    return tweets

# 将mysql中的标准人物存入mongo数据库中
def InsertStandardUsers(table):
    db = Conn()
    collection = db['StandardUsers']
    users = mysql.getUsersInfo(table)
    # 开始插入
    count = 0
    for user in users:
        data = {}
        data['user_id'] = (long)(user.id)
        data['screen_name'] = user.screen_name
        data['name'] = (user.name).decode("Latin-1").encode('utf-8')
        data['location'] = (user.location).decode("Latin-1").encode('utf-8')
        data['statuses_count'] = user.statuses_count
        data['friends_count'] = user.friends_count
        data['followers_count'] = user.followers_count
        data['favourites_count'] = user.favourites_count
        data['verified'] = user.verified
        data['category'] = user.category
        data['influenceScore'] = user.influenceScore
        data['rank_influ'] = user.rank_influ
        data['psy'] = user.psy
        data['psy_seq'] = user.psy_seq
        data['psy_tweets_starttime'] = user.psy_tweets_starttime
        data['interest_tags'] = (user.interest_tags).decode("Latin-1").encode('utf-8')
        data['description'] = (user.description).decode("Latin-1").encode('utf-8')
        data['crawler_date'] = user.crawler_date
        collection.insert(data)
        count += 1
        print "insert %d users" % count
    # 建立索引
    try:
        collection.ensureIndex("user_id",unique=True)
    except Exception as e:
        print "索引建立失败"

# 清空StandardUsers集合
def ClearCollection(collection_name):
    db = Conn()
    collection = db[collection_name]
    collection.remove({})

# 从mongo标准人物样本库中获取人物信息
def getUserById(userid,collection_name="StandardUsers"):
    '''

    :param userid: 字符串格式的userid
    :param collection_name: 集合名称,默认参数为StandardUsers
    :return:
    '''
    db = Conn()
    collection = db[collection_name]
    d = collection.find({"user_id":long(userid)})
    twitter_user = TwitterUsers.User(d[0]['user_id'],d[0]['screen_name'],d[0]['name'],d[0]['location'],d[0]['statuses_count'],d[0]['friends_count'],d[0]['followers_count'],d[0]['favourites_count'],d[0]['verified'],d[0]['category'],d[0]['influenceScore'],d[0]['rank_influ'],d[0]['psy'],d[0]['psy_seq'],d[0]['psy_tweets_starttime'],d[0]['interest_tags'],d[0]['description'],d[0]['crawler_date'])
    return twitter_user

# 检查数据库中是否存在用户
def CheckUser(userid,collection_name="StandardUsers"):
    db = Conn()
    collection = db[collection_name]
    d = collection.find({"user_id":long(userid)}).count()
    if d == 0:
        return False
    return True
