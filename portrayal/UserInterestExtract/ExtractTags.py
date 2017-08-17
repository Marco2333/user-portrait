#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import re
import os

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
tweets_folder_path = project_folder_path + "/TweetsSamples/"

def Extract(text):
    mention_dic = {}
    topics_dic = {}
    mentions_list = re.findall(r"@[\w|\d|_]+",text)
    topics_list = re.findall(r"#[\w|\d|_]+",text)
    mention_set = set(mentions_list)
    topics_set = set(topics_list)
    for m in mention_set:
        mention_dic[m] = mentions_list.count(m)
    for t in topics_set:
        topics_dic[t] = topics_list.count(t)
    # print mention_dic,topics_dic
    return mention_dic,topics_dic

if __name__ == "__main__":
    with open(tweets_folder_path + "RealDonMancini","r") as f:
        text = ""
        lines = f.readlines()
        for line in lines:
            text += line.replace("\n","")
        metions,topics =  Extract(text)
        metions = sorted(metions.items(),key = lambda dic:dic[1],reverse = True)
        topics = sorted(topics.items(),key = lambda dic:dic[1],reverse = True)
        # 输出前10的提及的人物screen_name和话题
        print metions[:10]
        print topics[:10]


