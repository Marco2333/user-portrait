#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 测试分类器分类精度


import os
import pickle
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

'''
装载训练集
'''
project_path = os.path.abspath("..")
piclke_path = project_path + "/DocumentClassify/pickles/"
'''
BCC分类：business/entertainment/politics/sport/technology
CNN分类：agriculture/economy/education/entertainment/military/politics/religion/sports/technology

DataSet1 是 CNN + BCC新闻数据集(分类融合起来)
DataSet2 是 BCC新闻数据集
DataSet3 是 CNN新闻数据集
DataSet4 是 CNN + BCC新闻数据集(CNN填补BCC没有的分类)
'''

def Training(data_set_path):
    print "------------------------------------------开始读入训练集--------------------------------------"
    training_set_path = project_path + data_set_path
    # print training_set_path
    training_set = datasets.load_files(training_set_path)
    totalnumber = len(training_set.data)
    print "文本类别分别是:"
    categories = training_set.target_names
    print categories

    # 2,8划分训练集
    training_set_x = []
    training_set_y = []
    test_set_x = []
    test_set_y = []
    rarray = np.random.random(totalnumber)
    for i in range(totalnumber):
        if rarray[i] < 0.7:
            training_set_x.append(training_set.data[i])
            training_set_y.append(training_set.target[i])
        else:
            test_set_x.append(training_set.data[i])
            test_set_y.append(training_set.target[i])
    training_set_y = np.array(training_set_y)
    test_set_y = np.array(test_set_y)
    test_set_x = np.array(test_set_x)
    categories_path = piclke_path + "categories.pickle"
    save_categories = open(categories_path,"wb")
    pickle.dump(categories,save_categories)
    save_categories.close()

    # 统计词频
    count_vect = CountVectorizer(stop_words="english",decode_error="ignore")
    x_train_counts = count_vect.fit_transform(training_set_x)

    count_vect_path = piclke_path + "count_vect.pickle"
    save_count_vect = open(count_vect_path,"wb")
    pickle.dump(count_vect,save_count_vect)
    save_count_vect.close()
    print "词频向量已保存"

    # 计算词频-逆文档词频
    tf_transformer = TfidfTransformer().fit(x_train_counts)
    # 持久化tf_transformer
    tf_transformer_path = piclke_path + "tf_transformer.picle"
    save_tf_transformer = open(tf_transformer_path,"wb")
    pickle.dump(tf_transformer,save_tf_transformer)
    save_tf_transformer.close()
    print "词频-文档逆词频已保存"
    x_train_tf = tf_transformer.transform(x_train_counts)

    # 多项式贝叶斯分类器分类
    clf = MultinomialNB().fit(x_train_tf,training_set_y)

    print "分类器训练完成......."
    MultinomialNB_classifier_path = piclke_path + "MultinomialNB_classifier.pickle"
    save_tweets_MultinomialNB_classifier = open(MultinomialNB_classifier_path,"wb")
    pickle.dump(clf,save_tweets_MultinomialNB_classifier)
    save_tweets_MultinomialNB_classifier.close()

    print "分类器已保存，目录为" + MultinomialNB_classifier_path
    test_set_count = count_vect.transform(test_set_x)
    test_tf_transformer = tf_transformer.transform(test_set_count)
    predicted = clf.predict(test_tf_transformer)
    print "accuracy:"
    print np.mean(predicted == test_set_y)
# Training("/DocumentClassify/DataSet1")