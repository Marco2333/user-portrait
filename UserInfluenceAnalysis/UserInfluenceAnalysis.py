#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import os
import pickle
import types
import FollowProcess
from numpy import *
import time
from scipy.sparse import csr_matrix

# hostname = "localhost"
# username = "root"
# password = "123"
# databasename = "TwitterUserInfo"

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
follower_path = project_folder_path + "/follower/"
follower_dic_path = project_folder_path + "/FollowerDic/"
user_matrix_path = project_folder_path + "/UserPMatrix/"
user_exit_matrix = [name.replace(".pickle","") for name in os.listdir(user_matrix_path)]

class User:
    'twitter用户对象'
    def __init__(self,id,screen_name,name,location,statuses_count,friends_count,followers_count,favourites_count,verified):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
        self.favourites_cout = favourites_count
        self.location = location
        self.verified = verified

    def getProportion(self):
        if self.friends_count != 0:
            return (self.followers_count) * 1.0 / self.friends_count
        else:
            return (self.followers_count) * 1.0 / 0.1

    def __str__(self):
        if self.verified == 1:
            verify = "是"
        else:
            verify = "否"
        if self.location == "":
            location = "未填写"
        else:
            location = self.location

        return "用户id:%s  screen_name：%s  姓名:%s  是否认证:%s  地理位置:%s  粉丝数:%d  关注人数:%d  推文数:%d  点赞次数:%d" % (self.id,self.screen_name,self.name,verify,location,self.followers_count,self.friends_count,self.statuses_count,self.favourites_cout)

# 数据库相关操作函数
# 连接数据库操作
def Conn(hostname,username,password,databasename):
    db = MySQLdb.connect(hostname,username,password,databasename)
    return db

# 获取用户基本信息列表
def getUsersInfo(cursor):
    # db = Conn(hostname,username,password,databasename)
    # cursor = db.cursor()
    cursor.execute("SELECT * FROM EnUserInfo")
    data = cursor.fetchall()
    user = []
    for d in data:
        twitter_user = User(d[0],d[1],d[2],d[3],d[6],d[7],d[8],d[9],d[11])
        user.append(twitter_user)
    return user

# 根据用户id查找用户信息
def getUserInfo(id,cursor):
    cursor.execute("SELECT * FROM EnUserInfo where user_id = %s" % id)
    d = cursor.fetchall()
    twitter_user = User(d[0][0],d[0][1],d[0][2],d[0][3],d[0][6],d[0][7],d[0][8],d[0][9],d[0][11])
    return twitter_user

# 得到当前结果集总数
def getTotoalCount(cursor):
    cursor.execute("SELECT COUNT(*) FROM EnUserInfo")
    counts = cursor.fetchall()
    return counts[0][0]

# 用户相关操作
# 过滤掉推文数小于10的推特用户，返回用户id列表
def Filter(users):
    userRs = []
    for user in users:
        if user.getUserStatuses_count() > 10:
            userRs.append(user)
    print "过滤后剩余结果数%d" % len(userRs)
    return userRs

# 得到认证过的用户列表
def getVerifiedUser(users):
    results = []
    for user in users:
        if user.getUserVerified() == 1:
            results.append(user.getUserId())
    return results

# 得到用户的粉丝列表
def getFollowers(user_id,follower_dic):
    follower = FollowProcess.getUserFollower(user_id,follower_dic)
    if type(follower) == types.StringType:
        followers = follower.split(" ")
    else:
        followers = follower
    return followers

def getFollowerMatrix(followerdic,users):
    totalnumber = len(users)
    usersid = set([user.id for user in users])
    number = len(user_exit_matrix)
    for user in users:
        if user.screen_name not in user_exit_matrix:
            userRow = []
            followers = set(getFollowers(user.id,followerdic))
            followers_in_users = followers & usersid
            for u in users:
                if u.id in followers_in_users or u.id == user.id:
                    userRow.append(u.getProportion())
                else:
                    userRow.append(0)
            print user.screen_name
            user_matrix = csr_matrix(userRow)
            save_file = open(user_matrix_path + "%s.pickle" % user.screen_name,"wb")
            pickle.dump(user_matrix,save_file)
            save_file.close()
            number += 1
            print "已完成%d个用户,剩余%d" % (number,totalnumber - number)
            # UsersMatrix.append(userRow)
    # UsersMatrix = mat(UsersMatrix)
    # 将UsersMatrix持久化
    # save_file = open(project_folder_path + "UserMatrix.pickle","wb")
    # pickle.dump(UsersMatrix,save_file)
    # save_file.close()
    # print "矩阵保存完毕"
    return number

def getuMatrix(path,users):
    uMatrix = []
    count = 0
    totalnumber = len(users)
    for user in users:
        try:
            open_file = open(path + user.screen_name + ".pickle","rb")
            usermatrix = pickle.load(open_file)
            open_file.close()
            uMatrix.append(usermatrix)
            print "load %s" % user.screen_name
            count += 1
            print "%d TO Process" % (totalnumber - count)
        except Exception as e:
            print user.screen_name
    print "共计读入%d个用户" % count
    return uMatrix

# 生成用户id和粉丝/关注人数比的字典
def generateProportion(users):
    prodic = {}
    for user in users:
        prodic[user.id] = user.getProportion()
    return prodic

# 离线查找用户信息
def getUserInfoOffline(users,id):
    for user in users:
        if user.id == id:
            return user

# 不使用矩阵的方式计算PR，计算过程比矩阵慢很多
def PageRank(followerdic,users,threshold,iterationN,uPR,d,proportiondic):
    N = len(users)
    iteration = 0
    usersid = set([user.id for user in users])
    while True:
        flag = True
        iteration += 1
        print "iteration %d" % iteration
        olduPR = uPR
        # 更新每个用户的PR
        userid = 0
        for user in users:
            userPR = 0
            followers = set(getFollowers(user.id,followerdic))
            followers_in_users = followers & usersid
            print len(followers_in_users)
            for u in followers_in_users:
                userPR += (getUserInfoOffline(users,u).getProportion() * uPR[u])
            uPR[user.id] = userPR * d + (1 - d) / N
            userid += 1
            print "done %d users" % userid
        # 判断是否还要迭代
        for ukey in users:
            if math.fabs(uPR[ukey.id] - olduPR[ukey.id]) > threshold:
                flag = False
                break
        if flag == True:
            break
        # 超出设定迭代次数
        if iteration == iterationN:
            break
    # 选出影响力前100的用户
    uiPR = sorted(uPR.items(),key = lambda dic:dic[1],reverse = True)
    return uiPR[:100]

# 利用稀疏矩阵基于PageRank算法影响力排序
def PageRank(uMatrix,fMatrix,d,PRMatrix,threshold,iterationN):
    NewPRMatrix = OldPRMatrix = PRMatrix
    iteration = 0
    rowN = NewPRMatrix.shape[0]
    while True:
        # 将下面的公式转换一下
        newPRMatrix = []
        # NewPRMatrix = fMatrix + d * uMatrix * OldPRMatrix
        for i in range(len(uMatrix)):
            newPRMatrix.append(double(uMatrix[i] * OldPRMatrix * d + fMatrix[i,0]))
        # print newPRMatrix
        NewPRMatrix = mat(newPRMatrix).T
        flag = True
        iteration += 1
        if iteration == iterationN:
            break
        for i in range(rowN):
            if math.fabs(NewPRMatrix[i,0] - OldPRMatrix[i,0]) > threshold:
                flag = False
                break
        if flag == True:
            break
        OldPRMatrix = NewPRMatrix
        print "迭代%d次" % iteration
    print "迭代次数%d" % iteration
    return NewPRMatrix

def CalucateUIPR(uMatrix,users):
    # 用户的screenname：IPR
    uiPR = {}
    i = 0
    for user in users:
        screenname = user.screen_name
        uiPR[screenname] = uMatrix[i,0]
        i += 1
    # 按照影响力降序排列
    uiPR = sorted(uiPR.items(),key = lambda dic:dic[1],reverse = True)
    return uiPR[:100]

# def setUsersFollower(followerdic,cursor):
#     users = getUsersInfo(cursor)
#     i = 0
#     N = getTotoalCount(cursor)
#     for user in users:
#         follower = getFollowers(user.id,followerdic)
#         if len(follower) == 0:
#             continue
#         follower = follower.replace(" ","#")
#         sql = "UPDATE EnUserInfo SET followers = %s where user_id = %s" % (follower,user.id)
#         i += 1
#         print "已处理%d条，还剩%d条待处理" % (i,N - i)
#         cursor.execute(sql)


# update follower_dic
def updateFollower_dic(follower_dic_path,toAddFollower_path,users):
    open_file = open(follower_dic_path,"rb")
    followers_dic = pickle.load(open_file)
    open_file.close()
    famous_users = map(lambda username: username.replace(".txt",""),os.listdir(toAddFollower_path))
    for user in famous_users:
        # followers = ReadFollowers(toAddFollower_path,user)
        user_id = getUserID(user,users)
        print user_id
        followers_dic[user_id] = user
    save_file = open(follower_dic_path + "followerdic.pickle","wb")
    pickle.dump(followers_dic,save_file)
    save_file.close()

def getUserID(username,users):
    for user in users:
        if user.screen_name == username:
            return user.id

if __name__ == '__main__':
    # conn = MySQLdb.connect(
    #     host='localhost',
    #     port = 3306,
    #     user='root',
    #     passwd='123',
    #     db ='TwitterUserInfo',
    # )
    # cursor = conn.cursor()

    # 加载followers字典
    # open_file = open(follower_dic_path + "followerdic.pickle","rb")
    # follower_dic = pickle.load(open_file)
    # open_file.close()

    # 测试followers字典
    # print follower_dic["30009639"]
    # print getFollowers("30009639",follower_dic)

    # 将用户持久化
    # users = getUsersInfo(cursor)
    # save_file = open(project_folder_path + "/users.pickle","wb")
    # pickle.dump(users,save_file)
    # save_file.close()

    # 载入所有用户
    open_file = open(project_folder_path + "/users.pickle","rb")
    users = pickle.load(open_file)
    open_file.close()
    # updateFollower_dic("/home/duncan/TwitterProjectFolder/FollowerDic/followerdic.pickle","/home/duncan/TwitterProjectFolder/follower/famous_users_followers/",users)

    # 生成每个用户的follower矩阵
    # t = time.time()
    # getFollowerMatrix(follower_dic,users)
    # print "用时%fs" % (time.time() - t)

    # 将总的uMatrix保存,总的userMatrix是一个列表，每行是每个用户的followers的稀疏矩阵
    # uMatrix = getuMatrix(user_matrix_path,users)
    # save_file = open(user_matrix_path + "uMatrix.pickle","wb")
    # pickle.dump(uMatrix,save_file)
    # save_file.close()
    # print uMatrix

    # 载入用户粉丝/关注比例字典
    # prodic = generateProportion(users)
    # 直接计算PageRank
    # print PageRank(follower_dic,users,0.01,100,uPR,0.85,prodic)

    # 用户matrix载入
    # uPR = {}
    # for user in users:
    #     uPR[user.id] = 1

    # 加载uMatrix
    open_file = open(user_matrix_path + "uMatrix.pickle")
    uMatrix = pickle.load(open_file)
    open_file.close()

    # print uMatrix.toarray()
    # print uMatrix

    # 矩阵方式计算PageRank
    fMatrix = mat([(1 - 0.85) / len(users) for i in range(len(users))]).T
    initPRMatrix = mat([1 for i in range(len(users))]).T
    print CalucateUIPR(PageRank(uMatrix,fMatrix,0.85,initPRMatrix,0.01,120),users)


    # usermatrix,number = getFollowerMatrix(follower_dic,users)

    # save_file = open(project_folder_path + "/users.pickle","wb")
    # pickle.dump(users,save_file)
    # save_file.close()
    # print "原数据集数目:%d" % getTotoalCount()
    # setUsersFollower(follower_dic,cursor)
    # for user in users:
    #     # print getFollowers(user.id,follower_dic)
    #     print user.id
    #     break
    # print getFollowers("100000075",follower_dic)

    # print number
    # # 过滤后的用户id结果集
    # filterResult = Filter(users)
    # for rs in filterResult:
    #     print rs.getProportion()
    #
    # # 获取认证过的用户
    # # verifiedUserResult = getVerifiedUser(filterResult)
    # # print "认证过的用户数目为%d" % len(verifiedUserResult)
    # cursor.close()
    # conn.commit()
    # conn.close()


