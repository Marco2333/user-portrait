#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


import sys
sys.path.append("..")
from Neo4jInteraction import TwitterWithNeo4j as neo4j
from MySQLInteraction import TwitterWithMysql as mysql

# 创建结点
def CreateNodes(path):
    '''

    :param path: CSV文件路径
    :return:
    '''
    neo4j.CreateNodesFromCSV(path)

# 删除所有结点和关系
def DeleteNodesAndRels():
    neo4j.DeleteAllNodesAndRels()

# 初始化操作
def Initial(path="file:///users.csv"):
    '''
    :param path: csv路径
    :return:
    '''
    # csv文件需要放在默认import目录下
    CreateNodes(path)

    # 建立索引
    neo4j.IndexBySName()

    # 设置userid为唯一
    neo4j.UniqueID()

# 查询两个用户是否有follows关系
def isFollow(userid1,userid2):
    return neo4j.isFollow(userid1,userid2)

# 单条插入关系
def InsertFollowsRel(userid1,userid2):
    neo4j.InsertFollowsRel(userid1,userid2)

# 查询某用户的关联用户,深度不小于7(默认参数=1)
def SearchFollowersByDepth(userid):
    users = neo4j.SearchFollowersByDepth(userid)
    return users

# 查询某个领域内的用户
def SearchUsersByCategory(categroy):
    users = neo4j.SearchUsersByCategory(categroy)
    return users

# 从mysql数据库中将标准人物样本库的人物关系存入neo4j中
# mysql数据格式:userid1,userid2,followed_by,following
def InsertRelsToNeoFromMysql(table="relation_temp"):
    relationships = mysql.getUserRelation(table)
    print len(relationships)
    # 对每一条关系插入到neo4j中
    count = 0
    for relation in relationships:
        InsertFollowsRel(relation[0],relation[1])
        count += 1
        print "insert %d relations" % count


if __name__ == '__main__':
    # 初始化操作,最开始执行一次,用于创建结点
    DeleteNodesAndRels()
    Initial()

    # 插入mysql中所有的关系
    InsertRelsToNeoFromMysql()

