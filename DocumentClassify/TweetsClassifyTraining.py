#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import sys
sys.path.append("..")
import config
import pickle
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# 贝叶斯-多项式贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB
# 随机梯度下降分类器
from sklearn.linear_model import SGDClassifier
# 随机森林和极端随机树
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
# 人工神经网络-多层传感器网络
# from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
# 引入集成学习来提高准确率
# adaboost用决策树来集成
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


'''
装载训练集
'''
project_path = config.project_path
piclke_path = project_path + "/DocumentClassify/pickles/"
'''
BCC分类：business/entertainment/politics/sport/technology
CNN分类：agriculture/economy/education/entertainment/military/politics/religion/sports/technology

DataSet1 是 CNN + BCC新闻数据集(分类融合起来)
DataSet2 是 BCC新闻数据集(加了维基词条的一些文章,加了CNN的一些文本,结果有提升)
DataSet3 是 CNN新闻数据集
DataSet4 是 CNN + BCC新闻数据集(CNN填补BCC没有的分类)
DataSet5 是 CNN新闻 + BCC新闻 + 推文数据集(融合)
'''

def Training(data_set_path=config.project_path + "/DocumentClassify/DataSet2"):
    print "------------------------------------------开始读入训练集--------------------------------------"
    training_set_path = project_path + data_set_path
    # print training_set_path
    training_set = datasets.load_files(training_set_path)
    print "文本类别分别是:"
    categories = training_set.target_names
    print categories
    categories_path = piclke_path + "categories.pickle"
    save_categories = open(categories_path,"wb")
    pickle.dump(categories,save_categories)
    save_categories.close()

    # 统计词频
    count_vect = CountVectorizer(stop_words="english",decode_error="ignore")
    x_train_counts = count_vect.fit_transform(training_set.data)

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
    clf = MultinomialNB().fit(x_train_tf,training_set.target)
    print "多项式贝叶斯分类器训练完成......."
    MultinomialNB_classifier_path = piclke_path + "MultinomialNB_classifier.pickle"
    save_tweets_MultinomialNB_classifier = open(MultinomialNB_classifier_path,"wb")
    pickle.dump(clf,save_tweets_MultinomialNB_classifier)
    save_tweets_MultinomialNB_classifier.close()
    print "多项式贝叶斯分类器已保存，目录为" + MultinomialNB_classifier_path


    # 使用线性核的SVM来分类
    # clf_svm = SVC(kernel='linear').fit(x_train_tf,training_set.target) # 默认的核是rbf核
    # print "线性核的SVM分类器训练完成......."
    # LinearSVM_classifier_path = piclke_path + "LinearSVM_classifier.pickle"
    # save_tweets_LinearSVM_classifier = open(LinearSVM_classifier_path,"wb")
    # pickle.dump(clf_svm,save_tweets_LinearSVM_classifier)
    # save_tweets_LinearSVM_classifier.close()
    # print "线性核的SVM分类器已保存，目录为" + LinearSVM_classifier_path

    # 使用随即梯度下降模型来分类
    # clf_SGD = SGDClassifier(loss="hinge", penalty="l2").fit(x_train_tf.toarray(),training_set.target)
    # print "随机梯度下降分类器训练完成......."
    # SGD_classifier_path = piclke_path + "SGD_classifier.pickle"
    # save_tweets_SGD_classifier = open(SGD_classifier_path,"wb")
    # pickle.dump(clf_SGD,save_tweets_SGD_classifier)
    # save_tweets_SGD_classifier.close()
    # print "随机梯度下降分类器已保存，目录为" + SGD_classifier_path

    # 使用随机森林模型来分类
    clf_RandomForest = RandomForestClassifier(n_estimators=10).fit(x_train_tf.toarray(),training_set.target)
    print "随机森林分类器训练完成......."
    RandomForest_classifier_path = piclke_path + "RandomForest_classifier.pickle"
    save_tweets_RandomForest_classifier = open(RandomForest_classifier_path,"wb")
    pickle.dump(clf_RandomForest,save_tweets_RandomForest_classifier)
    save_tweets_RandomForest_classifier.close()
    print "随机森林分类器已保存，目录为" + RandomForest_classifier_path

    # 使用人工神经网络
    # clf_MLP = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1).fit(x_train_tf.toarray(),training_set.target)
    # print "多层传感器分类器训练完成......."
    # MLP_classifier_path = piclke_path + "MLP_classifier.pickle"
    # save_tweets_MLP_classifier = open(MLP_classifier_path,"wb")
    # pickle.dump(clf_MLP,save_tweets_MLP_classifier)
    # save_tweets_MLP_classifier.close()
    # print "多层传感器分类器已保存，目录为" + MLP_classifier_path

    # 使用极端随机树
    # clf_ExtraTree = ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0).fit(x_train_tf.toarray(),training_set.target)
    # print "极端随机树分类器训练完成......."
    # ExtraTree_classifier_path = piclke_path + "ExtraTree_classifier.pickle"
    # save_tweets_ExtraTree_classifier = open(ExtraTree_classifier_path,"wb")
    # pickle.dump(clf_ExtraTree,save_tweets_ExtraTree_classifier)
    # save_tweets_ExtraTree_classifier.close()
    # print "极端随机树分类器已保存，目录为" + ExtraTree_classifier_path

    #　集成学习
    bdt_real = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2),
        n_estimators=600,
        learning_rate=1)
    bdt_real.fit(x_train_tf.toarray(),training_set.target)
    print "adaboost训练完成...."
    adaboost_classifier_path = piclke_path + "adaboost_classifier.pickle"
    save_tweets_adaboost_classifier = open(adaboost_classifier_path,"wb")
    pickle.dump(bdt_real,save_tweets_adaboost_classifier)
    save_tweets_adaboost_classifier.close()


# Training("/DocumentClassify/DataSet2")

