#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 计算标准人物样本库人物的心理状态

import SentimentWithTime as senti
from MySQLInteraction import TwitterWithMysql as mysql

# 计算人物的心理状态
def calcpsy(table):
    users = mysql.getUsersInfo(table)
    count = 1
    neg = 0
    unknown = 0
    loss = 0
    for user in users:
        try:
            starttime,psychologic,res = senti.SentimentWithTime(user.id)
            # 将序列转换成字符串
            psychologic = ",".join(psychologic)
            if(res == -1):
                neg += 1
            elif(res == 0):
                unknown += 1
            # 将心理状态写入数据库
            mysql.updateUserPsy(table,user.id,res,psychologic,starttime)
        except Exception as e:
            loss += 1
            print "losss %d users" % loss
            print user.id
        print "finished %d users" % count
        count += 1
    print "负面心理的有%d个" % neg
    print "未知状态的有%d个" % unknown

# 全局计算所有人的心理状态
# calcpsy("StandardUsers")