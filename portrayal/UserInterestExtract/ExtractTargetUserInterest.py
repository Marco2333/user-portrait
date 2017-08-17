#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import re
import nltk
from pytagcloud import create_tag_image,make_tags
import webbrowser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from ..MongoDBInteraction import TweetsWithMongo as mongo
from ..MySQLInteraction import TwitterWithMysql as mysql
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from numpy import *
from ..import config

BeatFactor = 3000000

project_path = config.project_path

# usercandidate = []

stopwords = config.getStopWords()

# 推文切分为单词
def Split(text):
    text = re.sub(r'[@|#][\d|\w|_]+|http[\w|:|.|/|\d]+',"",text)
    # print text
    wordslist = []
    if text == "" or text == None:
        return []
    words = word_tokenize(text.encode('utf-8').decode('Latin-1'))
    # clear @/#/url/emotion
    for word in words:
        # count = 0
        if word.isalpha() and word.lower() not in stopwords and len(word) > 2:
            # word = word.lower()
            wordslist.append(word)
    return wordslist

# 获取某用户的单词列表,返回结果是用户的单词集合
def GenerateWords(id,table="StandardUsers"):

    # 获取用户推文
    candidates = getUserTopInterest(id)
    wordsSet = map(lambda candidate:(candidate[0]).lower(),candidates)
    return set(wordsSet)

# 推文预处理
def PreProcess(text):
    # open_file = open(slang_file_path,"rb")
    # slang = pickle.load(open_file)
    # open_file.close()

    wordslist = Split(text)
    try:
        pos = nltk.pos_tag(wordslist)
    except Exception as e:
        pos = []
    return pos

'''
步骤2：兴趣词或短语生成候选集
兴趣词的模式为
单个词形式：Noun|Adjective|Verb (经测试效果不是很好，暂时选用名词Noun形式)
词组形式：(Verb?)(Adjective|Noun)Noun+ (词组形式暂时选用动词+名词 或  形容词+名词形式)
动词和名词先做词性还原
'''
def Generation(pos):
    if len(pos) < 1:
        return []
    usercandidate = []
    # global usercandidate
    multicandidate = []
    lemmatizer = WordNetLemmatizer()
    # single_pattern = ["N","J","V"]
    for w in pos:
        # if w[1][0] in single_pattern:
        # if w[1][0] == 'V':
        #     # 排除前100常用的动词
        #     word = lemmatizer.lemmatize(w[0],'v')
        #     if word in topverbwords:
        #         continue
        if(w[1][0] == 'N'):
            word = lemmatizer.lemmatize(w[0])
        # else:
        #     word = lemmatizer.lemmatize(w[0],'a')
            if word.lower() not in stopwords:
                usercandidate.append(word)

    # 两个词的长度
    if(len(pos) == 2 and pos[0][1][0] == 'J' and pos[1][1][0] == 'N'):
        # 这边名词已经合成为短语加进去,所以单个名词集合除去单个名词
        try:
            usercandidate.remove(pos[1][0])
        except Exception as e:
            pass
        phase = lemmatizer.lemmatize(pos[0][0],'a') + " " + lemmatizer.lemmatize(pos[1][0])
        usercandidate.append(phase)
        return usercandidate

    i = 0
    while(i < len(pos) - 2):
        phase = ""
        # verb + adj + n+ or verb n+
        if (pos[i])[1][0] == 'V' and (pos[i + 1][1][0] == 'N' or (pos[i + 1][1][0] == "J" and pos[i + 2][1][0] == "N")):
            if pos[i + 1][1][0] == 'J':
                suffix = lemmatizer.lemmatize(pos[i + 1][0],'a')
            else:
                suffix = lemmatizer.lemmatize(pos[i + 1][0],'n')
            phase += lemmatizer.lemmatize((pos[i])[0],'v') + " " + suffix
            i = i + 2
            # 最多加两个名词
            j = 1
            while(i < len(pos) and (pos[i])[1][0] == 'N' and j != 2):
                phase += " " + lemmatizer.lemmatize((pos[i])[0])
                i += 1
                j += 1
            # 移除单个名词
            try:
                usercandidate.remove(lemmatizer.lemmatize((pos[i])[0]))
            except Exception as e:
                pass
            multicandidate.append(phase)
        # adj + n+
        elif(pos[i][1][0] == "J" and pos[i + 1][1][0] == "N"):
            phase +=lemmatizer.lemmatize((pos[i])[0],"a") + " " + lemmatizer.lemmatize((pos[i + 1])[0])
            # 移除单个名词
            try:
                usercandidate.remove(lemmatizer.lemmatize((pos[i + 1])[0]))
            except Exception as e:
                pass
            i += 2
            j = 1
            while(i < len(pos) and (pos[i])[1][0] == 'N' and j != 2):
                phase += " " + lemmatizer.lemmatize((pos[i])[0])
                # 移除单个名词
                try:
                    usercandidate.remove(lemmatizer.lemmatize((pos[i])[0]))
                except Exception as e:
                    pass
                i += 1
                j += 1

            multicandidate.append(phase)
        # n n+
        # elif(pos[i][1][0] == "N" and pos[i + 1][1][0] == "N"):
        #     if((i != 0 and pos[i - 1][1][0] != "V" and pos[i - 1][1][0] != "J") or i ==0):
        #         phase += lemmatizer.lemmatize((pos[i])[0]) + " " + lemmatizer.lemmatize((pos[i + 1])[0])
        #         i += 2
        #         while(i < len(pos) and (pos[i])[1][0] == 'N'):
        #             phase += " " + lemmatizer.lemmatize((pos[i])[0])
        #             i += 1
        #     MultiCandidate.append(phase)
        else:
            i += 1
    if len(multicandidate) != 0:
        usercandidate += multicandidate
    return usercandidate

'''
步骤3：候选集排序
单用户使用TF词频排序,并生成前NS兴趣候选集
'''
def CalculateTF(usercandidate):
    vac = set(usercandidate)
    vacdic = {}
    # 得到词频
    for phase in vac:
        vacdic[phase] = usercandidate.count(phase)
    sum = 0
    for key in vacdic.keys():
        sum += vacdic[key]
    # 计算TF值
    for key in vacdic.keys():
        vacdic[key] = vacdic[key] * 1.0 / sum

    # 按照键值排序
    vacdic = sorted(vacdic.items(),key = lambda dic:dic[1],reverse = True)
    # 输出前100个兴趣候选集
    return vacdic[:50]

# 代码重构,直接从mongo数据库中读取推文
def getUserTopInterest(userid):
    # global usercandidate
    usercandidate = []
    # 获取该用户的推文
    tweets = mongo.getUserTweets(userid)
    # 移除回复/对话的推文 （是以@XXXX开头）
    # print "user tweet id is %d" % user_tweet_id
    res = Generation(PreProcess(tweets))
    # Generation(PreProcess(line.decode("utf-8")))
    if res != None:
        usercandidate += res
    usercandidate = CalculateTF(usercandidate)
    return usercandidate

'''
步骤4:得到目标用户候选集后，在其它用户中计算TFIDF值
'''
def CalculateTFIDF(usercandidate,user_id,table="StandardUsers"):

    # 获取用户的所有id
    userids = mysql.getUsersId(table)
    userNumber = len(userids)
    print "正在计算TFIDF,数据库中共计%d个用户" % (userNumber)
    # print "该用户有%d个用户,现在开始计算" % (userNumber - 1)
    tfidf = [1 for i in range(50)]
    # for i in range(100):
    #     tfidf.append(1)
    count = 0
    for userid in userids:
        if userid == user_id:
            continue
            # lines = f.readlines()
        wordsSet = GenerateWords(userid)
        id = 0
        for candidate in usercandidate:
            # 全部转换成小写
            if (candidate[0]).lower() in wordsSet:
                tfidf[id] += 1
            # except Exception as e:
            #     pass
            id += 1
        count += 1
        print count
    id = 0
    for uc in usercandidate:
        value = math.log(userNumber * 1.0 / tfidf[id]) * uc[1]
        tfidf[id] = value
        id += 1
    # tfidf = map(lambda value:math.log(value * 1.0 / userNumber) * usercandidate[key],tfidf)
    return tfidf

'''
步骤5:计算TextRank-TFIDF排序
'''
def CalucateSum(matrix):
    op = []
    for i in range(matrix.shape[0]):
        sum = 0
        for j in range(matrix.shape[0]):
            sum += matrix[i,j]
        op.append(sum)
    return op

def CalculateWeight(usercandidate):
    matrix = []
    for u1 in range(len(usercandidate)):
        line = []
        for u2 in range(len(usercandidate)):
            weight = min(usercandidate[u1][1],usercandidate[u2][1])
            line.append(weight)
        matrix.append(line)
    oldmatrix = mat(matrix)
    newmatrix = []
    op = CalucateSum(oldmatrix)
    # print op
    for i in range(oldmatrix.shape[0]):
        line = []
        for j in range(oldmatrix.shape[0]):
            line.append(float(oldmatrix[i,j] * 1.0 / op[j]))
        newmatrix.append(line)
    newmatrix = mat(newmatrix)
    return newmatrix

def CalculateTextRank(ucMatrix,threshold,dampFactor,idf,InitTRMatrix):
    TFIDFMatrix = mat(idf).T * (1 - dampFactor) / BeatFactor
    # print TFIDFMatrix
    TRMatrix = InitTRMatrix.T
    oldMatrix = TRMatrix
    # iteration
    iteration = 0
    while True:
        newMatrix = TRMatrix = ucMatrix * TRMatrix + TFIDFMatrix
        # newMatrix = TRMatrix = ucMatrix * TRMatrix

        flag = True
        for i in range(newMatrix.shape[0]):
            if math.fabs(newMatrix[i,0] - oldMatrix[i,0]) > threshold:
                flag = False
                break
        if flag == True:
            break
        iteration += 1
        if iteration == 20000:
            break
        # print iteration
        oldMatrix = TRMatrix
    # print "the number of iteration is %d " % iteration
    return TRMatrix

def CalucateUCTR(usercandidate,ucTRMatrix):
    ucTR = {}
    i = 0
    for user in usercandidate:
        candidate = user[0]
        TR = ucTRMatrix[i,0]
        i += 1
        ucTR[candidate] = TR
    # 按照ucTR的键值排序
    ucTR = sorted(ucTR.items(),key = lambda dic:dic[1],reverse = True)
    # print ucTR[:10]
    ucTR10,ucTR50 = ucTR[:10],ucTR[:50]
    return ucTR10,ucTR50

def ProcessBio(userid,table="StandardUsers"):
    description = mysql.getUserDescription(table,userid)
    results = Generation(PreProcess(description))
    return results

def GenerateTargetUserInterest(Target_userid):
    # 初始矩阵设为权值都为1的矩阵
    TR = [1 for i in range(50)]
    InitTRMatrix = mat(TR)

    # steponetime = time.time()
    target_user_candidate = getUserTopInterest(Target_userid)
    # steptwotime = time.time()
    # print "第一步计算用户兴趣候选集,用时 %f s" % (steptwotime - steponetime)
    # print "正在计算TFIDF,大约需要几分钟"
    idf = CalculateTFIDF(target_user_candidate,Target_userid)
    # print "第二步计算用户TFIDF特征,用时 %f s" % (time.time() - steptwotime)
    # print "开始TextRank迭代计算用户兴趣候选集排序,计算中"
    # trstarttime = time.time()
    uiMatrix = CalculateWeight(target_user_candidate)
    ucTRMatrix = CalculateTextRank(uiMatrix,0.0001,0.85,idf,InitTRMatrix)
    Interest10,Interest50 = CalucateUCTR(target_user_candidate,ucTRMatrix)
    # trendtime = time.time()
    # print "迭代过程耗时 %f s" % (trendtime - trstarttime)
    return Interest10,Interest50

# 测试标签云库，将用户兴趣集可视化
def GenerateTagCloud(InterestSorted,name):
    newdic = []
    for d in InterestSorted:
        newdic.append((d[0],d[1] * 10000))
    tags = make_tags(newdic, minsize = 5,maxsize=30)
    # 保存在当前目录下
    create_tag_image(tags, name + 'tags.png', size=(700, 600), fontname='Nobile')
    webbrowser.open(name + 'tags.png') # see results


# 对外接口,返回该用户前10个兴趣标签
def GenerateInterestsWithFollowers(userid):
    '''
    :param path: 该用户推文路径
    :param screen_name: 该用户screen_name
    :param followers_path: 该用户粉丝们的推文路径
    :return:
    '''
    Interest10,Interest50 = GenerateTargetUserInterest(userid)
    description = ProcessBio(userid)
    interests = map(lambda interest:interest[0],Interest10)
    # 把简介加入到兴趣标签中,去除重复的
    interests = set(interests)
    interests.union(set(description))
    new_interests = set()
    lower_interest = set()
    interests.union(set(description))
    # 去除重复的标签
    for interest in interests:
        if interest.lower() not in lower_interest:
            lower_interest.add(interest.lower())
            new_interests.add(interest)
    interests = ",".join(new_interests)
    # 将50个兴趣标签生成TagCloud
    # GenerateTagCloud(Interest50,userid)
    return interests

# 对外接口,返回该用户前10个兴趣标签,但不在粉丝中TextRank排序
def GenerateInterestsWithTF(userid):
    '''
    :param path: 该用户推文路径
    :param screen_name: 该用户screen_name
    :param followers_path: 该用户粉丝们的推文路径
    :return:
    '''
    Interest10 = getUserTopInterest(userid)[:10]
    description = ProcessBio(userid)
    interests = map(lambda interest:interest[0],Interest10)
    # 把简介加入到兴趣标签中,去除重复的
    interests = set(interests)
    new_interests = set()
    lower_interest = set()
    interests.union(set(description))
    # 去除重复的标签
    for interest in interests:
        if interest.lower() not in lower_interest:
            lower_interest.add(interest.lower())
            new_interests.add(interest)
    interests = ",".join(new_interests)
    return interests

# 生成所有用户的兴趣标签
def GenerateAllUsersInterestTags(table="StandardUsers"):
    users = mysql.getUsersInfo(table)
    count = 0
    loss = 0
    for user in users:
        try:
            interests = GenerateInterestsWithFollowers(user.id)
            print "%s:" % user.id
            print interests
            # 写入数据库中
            mysql.updateUserInterest(table,user.id,interests.encode('utf-8'))
        except Exception as e:
            loss += 1
            print "lose userid:%s" % user.id
            print "loss %d users" % loss
        count += 1
        print "finished %d users" % count

# 以推文和用户简介为参数获取用户的兴趣标签
def GenerateInterestsWithTFFromTweets(text,bio):
    #　获取简介的兴趣标签
    bio = Generation(PreProcess(bio))
    # 获取推文的兴趣标签
    res = Generation(PreProcess(text))
    usercandidate = CalculateTF(res)[:10]
    interests = map(lambda interest:interest[0],usercandidate)
    # 把简介加入到兴趣标签中,去除重复的
    interests = set(interests)
    new_interests = set()
    lower_interest = set()
    interests.union(set(bio))
    # 去除重复的标签
    for interest in interests:
        if interest.lower() not in lower_interest:
            lower_interest.add(interest.lower())
            new_interests.add(interest)
    interests = ",".join(new_interests)
    return interests

# 样例
def test():
    starttime = time.time()
    # 生成所有标准人物样本库中人物的兴趣爱好标签
    GenerateAllUsersInterestTags()
    # print GenerateInterestsWithFollowers("1173831")
    endtime = time.time()
    print "used %f seconds" % (endtime - starttime)

# test()

# print GenerateInterestsWithTF("10126672")
# print PreProcess("China is a nice country")
# print mysql.getUserInfo('104557267',"StandardUsers")
# print mysql.getUserDescription("StandardUsers",'10126672')