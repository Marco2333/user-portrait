#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
# 配置文件
# 目录配置
import os
project_path = os.path.abspath(".")
stop_words_path = project_path + "/resource/stopwords.txt"
XML_path = project_path + "/resource/UsersXML/"

# mysql配置
host = "localhost"
port = 3306
user = "root"
passwd = "123"
db = "TwitterUserInfo"

# mongodb配置
mongo_host = "127.0.0.1"
mongo_port = 27017

# neo4j配置
neo_host = "bolt://localhost:7687"
neo_user = "neo4j"
neo_passwd = "123"

# 参数配置
months = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
high_influence = 120
medium_influence = 70
rank_influence = {1:"较低",2:"中等",3:"较大"}
psychological = {1:"正面",-1:"负面",0:"未知"}

#多项式贝叶斯分类器/线性svm/随机森林/随机梯度下降/极端树
mnb = "MultinomialNB"
svm = 'LinearSVM'
forest = 'RandomForest'
sgd = 'SGD'
etree = 'ExtraTree'
ada = 'adaboost'

# 资源配置
# 读取停用词
def getStopWords(path=stop_words_path):
    stopwords = set()
    with open(path,"r") as f:
        lines = f.readlines()
    for line in lines:
        stopwords.add(line.replace("\r\n","").rstrip())
    return stopwords

# stopwords = getStopWords(stop_words_path)
