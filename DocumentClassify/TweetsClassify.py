#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import pickle
import config
import os
import TweetsClassifyTraining

project_path = config.project_path
data_folder_path = "/TweetsSamples/"
pickle_path = project_path + "/DocumentClassify/pickles/"
tf_transformer_path = pickle_path + "tf_transformer.picle"
categories_path = pickle_path + "categories.pickle"
count_vect_path = pickle_path + "count_vect.pickle"

def Classify(text,Classifier):
    '''
    :param text:待分类的文本
    :param Classifier:分类器类别
    :return: 返回分类结果
    '''
    if text == "" or text == None:
        return "None"
    txt = []
    # print text
    txt.append(text)

    # 如果模型持久化文件不存在则需要先训练
    if len(os.listdir(config.project_path + "/DocumentClassify/pickles/")) <= 6:
        TweetsClassifyTraining.Training()

    # 测试数据转化为特征向量
    open_file = open(count_vect_path)
    count_vect = pickle.load(open_file)
    open_file.close()

    x_test_counts = count_vect.transform(txt)

    open_file = open(tf_transformer_path)
    tf_transformer = pickle.load(open_file)
    open_file.close()

    x_test_tf = tf_transformer.transform(x_test_counts)


    # 选择分类器
    classifier_path = pickle_path + Classifier + "_classifier.pickle"

    # 分类
    open_file = open(classifier_path)
    clf = pickle.load(open_file)
    open_file.close()

    open_file = open(categories_path)
    target_names = pickle.load(open_file)
    open_file.close()

    result = target_names[clf.predict(x_test_tf.toarray())[0]]
    return result

# 多模型融合,给每个模型结果相应的权重[0.4,0.3,0.1,0.1,0.1]
def Classify_MultiModels(text,classifiers,weight):
    if text == "" or text == None:
        return "None"
    txt = []
    # print text
    txt.append(text)

    # 测试数据转化为特征向量
    open_file = open(count_vect_path)
    count_vect = pickle.load(open_file)
    open_file.close()

    x_test_counts = count_vect.transform(txt)

    open_file = open(tf_transformer_path)
    tf_transformer = pickle.load(open_file)
    open_file.close()

    x_test_tf = tf_transformer.transform(x_test_counts)

    results = []
    results_set = []
    classify_result = {}
    for (Classifier,i) in zip(classifiers,range(len(classifiers))):
        # 选择分类器
        classifier_path = pickle_path + Classifier + "_classifier.pickle"

        # 分类
        open_file = open(classifier_path)
        clf = pickle.load(open_file)
        open_file.close()

        open_file = open(categories_path)
        target_names = pickle.load(open_file)
        open_file.close()

        result = target_names[clf.predict(x_test_tf.toarray())[0]]
        results.append((result,weight[i]))
        results_set.append(result)
    results_set = set(results_set)
    for res in results_set:
        value = 0
        for tuple in results:
            if res == tuple[0]:
                value += tuple[1]
        classify_result[res] = value
    classify_result = sorted(classify_result.items(),key = lambda dic:dic[1],reverse = True)
    return classify_result[:1][0][0]

def Accuracy(resdic,users):
    '''
    :param resdic: 格式: {screen_name:category}
    :param users:  格式: {name,screen_name,category}
    :return:准确率
    '''
    correct = 0
    if isinstance(users,list):
        for dickey in resdic.keys():
            for user in users:
                if dickey == user.screen_name and resdic[dickey] == user.category:
                    correct += 1
                    break
    else:
        for dickey in resdic.keys():
            for id in users.keys():
                if dickey == id:
                    if resdic[dickey] == users[id]:
                        correct += 1
                        break
    return (correct * 1.0 / len(resdic))


# 测试分类器效果
def test():
    # 读取20个名人screenname/name/标注分类
    # open_file = open(pickle_path + "20famous.pickle")
    # famous = pickle.load(open_file)
    # open_file.close()
    # famous_screen_name = os.listdir(famouse_tweets_folder_path)
    # # print famous_screen_name
    # correct  = 0
    # for name in famous_screen_name:
    #     filename = name
    #     file_path = famouse_tweets_folder_path + filename
    #     text = getTweets(file_path)
    #     category = Classify(text)
    #     for user in famous:
    #         if name == user[0] and user[2] == category:
    #             correct += 1
    #             break
    #     print "%s => %s" % (name,category)
    # print "以标注的20个名人为准准确率为:"
    # print (correct * 1.0 / 20)
    text = """Even as China needs to reassure the international community that it has no aggressive intentions, which it is trying to do with its modest military budget increase this year, it is caught in a bit of a bind.China seeks to become a major world power, and one of the hallmarks of such a status is blue-water capability and the ability to project military might globally;"""
    print Classify(text)
# test()