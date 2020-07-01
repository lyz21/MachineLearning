# encoding=utf-8
"""
@Time : 2020/4/23 10:41 
@Author : LiuYanZhe
@File : max_min_classify.py 
@Software: PyCharm
@Description: 最大最小距离算法的Python实现
数据集形式data=[[],[],...,[]]
聚类结果形式result=[[[],[],...],[[],[],...],...]
其中[]为一个模式样本，[[],[],...]为一个聚类
"""

import math
import matplotlib.pyplot as plt
import numpy as np


def start_cluster(data, t):
    zs = [data[0]]  # 聚类中心集，选取第一个模式样本作为第一个聚类中心Z1
    # 第2步：寻找Z2,并计算阈值T
    T = step2(data, t, zs)
    # 第3,4,5步，寻找所有的聚类中心
    get_clusters(data, zs, T)
    # 按最近邻分类
    result = classify(data, zs, T)
    return result


# 分类
def classify(data, zs, T):
    result = [[] for i in range(len(zs))]
    for aData in data:
        min_distance = T
        index = 0
        for i in range(len(zs)):
            temp_distance = get_distance(aData, zs[i])
            if temp_distance < min_distance:
                min_distance = temp_distance
                index = i
        result[index].append(aData)
    return result


# 寻找所有的聚类中心
def get_clusters(data, zs, T):
    max_min_distance = 0
    index = 0
    for i in range(len(data)):
        min_distance = []
        for j in range(len(zs)):
            distance = get_distance(data[i], zs[j])
            min_distance.append(distance)
        min_dis = min(dis for dis in min_distance)
        if min_dis > max_min_distance:
            max_min_distance = min_dis
            index = i
    if max_min_distance > T:
        zs.append(data[index])
        # 迭代
        get_clusters(data, zs, T)


# 寻找Z2,并计算阈值T
def step2(data, t, zs):
    distance = 0
    index = 0
    for i in range(len(data)):
        temp_distance = get_distance(data[i], zs[0])
        if temp_distance > distance:
            distance = temp_distance
            index = i
    # 将Z2加入到聚类中心集中
    zs.append(data[index])
    # 计算阈值T
    T = t * distance
    return T


# 计算两个模式样本之间的欧式距离
def get_distance(data1, data2):
    distance = 0
    for i in range(len(data1)):
        distance += pow((data1[i] - data2[i]), 2)
    return math.sqrt(distance)


# 数据集
# data = [[0, 0], [3, 8], [1, 1], [2, 2], [5, 3], [4, 8], [6, 3], [5, 4], [6, 4], [7, 5]]
data = [[0, 7], [0, 6.5], [0, 6], [0, 5.5], [0, 5], [0, 4.5], [1, 4.5], [2, 4.5],
        [3, 7], [3.5, 6.5], [4, 6], [4.5, 5.5], [5, 6], [5.5, 6.5], [6, 7], [4.5, 5], [4.5, 4.5],
        [9, 7], [9.5, 7], [10, 7], [10.5, 7], [10.5, 6.5], [10, 6], [9.5, 5.5], [9, 5],
        [9, 4.5], [9.5, 4.5], [10, 4.5], [10.5, 4.5]]
# 设置阈值比例
t = 0.3
result = start_cluster(data, t)
plt.figure()
for i in range(len(result)):
    print("----------第" + str(i + 1) + "个聚类----------")
    print(result[i])
    result_temp = np.array(result[i])
    plt.scatter(result_temp[:, 0], result_temp[:, 1])
plt.show()

# 打印结果：
# ----------第1个聚类----------
# [[0, 0], [1, 1], [2, 2]]
# ----------第2个聚类----------
# [[3, 8], [4, 8]]
# ----------第3个聚类----------
# [[5, 3], [6, 3], [5, 4], [6, 4], [7, 5]]
