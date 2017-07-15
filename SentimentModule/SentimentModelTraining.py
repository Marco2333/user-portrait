#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import nltk
import random
# 将nltk和scikitlearn框架结合起来
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import LinearSVC
from nltk.tokenize import word_tokenize
import config


# 对一段文档建立特征
def Word2Features(document,word_features):
    # document = document.decde('utf-8')
    words = word_tokenize(document,language='english')
    words = set([w for w in words if w not in config.stopwords])
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# 训练
def Training():
    # 加载语料库
    short_pos = open("twitter-sentiment-dataset/positive.txt","r").read()
    short_neg = open("twitter-sentiment-dataset/negative.txt","r").read()

    documents = []
    all_words = []

    # J是代表形容词，R代表副词，V代表动词
    allowed_types = ['J']

    line = 0
    for p in short_pos.split("\n"):
        try:
            line += 1
            words = word_tokenize(p)
            documents.append((p,"pos"))
            #print documents
            pos = nltk.pos_tag(words)
            # 形容词对情感影响较大，所以选取形容词为特征
            for w in pos:
                if w[1][0] in allowed_types:
                    # 这一步可以再优化，词性还原，提取词根等等
                    all_words.append(w[0].lower())
        except Exception as e:
            print ("positive文档第%d行有编码问题:") % line
            print p

    line = 0
    for p in short_neg.split("\n"):
        try:
            line += 1
            words = word_tokenize(p)
            documents.append((p,"neg"))
            pos = nltk.pos_tag(words)
            # 形容词对情感影响较大，所以选取形容词为特征
            for w in pos:
                if w[1][0] in allowed_types:
                    all_words.append(w[0].lower())
        except Exception as e:
            print ("negative文档第%d行有编码问题:") % line
            print p

    # 将处理好的文档持久化
    save_documents = open("pickle_algos/documents.pickle","wb")
    pickle.dump(documents,save_documents)
    save_documents.close()
    print("处理完成的文档已保存!")

    # 将所有词按照词频按降次排序
    all_words = nltk.FreqDist(all_words)
    # 选取前5000个词作为特征属性,按照词频作为特征提取的依据
    word_features = list(all_words.keys())[:5000]
    # print (word_features)

    # 将特征属性持久化
    save_features = open("pickle_algos/word_features5K.pickle","wb")
    pickle.dump(word_features,save_features)
    save_features.close()
    print("特征属性已保存!")

    featuresets = [(Word2Features(rev,word_features),category) for (rev,category) in documents]
    # 打乱，为了抽取训练集和测试集
    random.shuffle(featuresets)
    print("共有数据集: ")
    print len(featuresets)

    testing_set = featuresets[10000:]
    print("测试集:659条")
    training_set = featuresets[:10000]
    print("训练集:10000条")

    # 分类器选择
    # 朴素贝叶斯-nltk自带分类器
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("朴素贝叶斯分类精度:")
    print(nltk.classify.accuracy(classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/naivebayes.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()

    # 多项式分类器-sklearn
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    print("多项式分类器分类精度:")
    print(nltk.classify.accuracy(MNB_classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/MNB_classifier.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()

    # 伯努利分类器-sklearn
    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)
    print("伯努利分类器分类精度：")
    print(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/BernoulliNB_classifier.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()

    # 逻辑回归分类-sklearn
    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    print("逻辑回归分类器分类精度:")
    print(nltk.classify.accuracy(LogisticRegression_classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/LogisticRegression_classifier.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()

    # 线性支持向量机分类器-sklearn
    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    print("线性支持向量机分类精度:")
    print(nltk.classify.accuracy(LinearSVC_classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/LinearSVC_classifier.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()

    # 梯度下降分类器-sklearn
    SGDC_classifier = SklearnClassifier(SGDClassifier())
    SGDC_classifier.train(training_set)
    print("梯度下降分类精度：")
    print(nltk.classify.accuracy(SGDC_classifier,testing_set))
    # 分类器持久化
    save_classifier = open("pickle_algos/SGDC_classifier.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()