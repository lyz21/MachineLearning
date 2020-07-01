# encoding=utf-8
"""
@Time : 2020/6/19 19:36 
@Author : LiuYanZhe
@File : K-Means.py 
@Software: PyCharm
@Description: k-means聚类
"""
from sklearn.cluster import KMeans
from math_model.util import dataUtil
from math_model.util import picutil
import pandas as pd
import numpy as np


# 计算0 1的概率
def get_probability(index, data):
    data1 = data[index]
    d_0 = data1[data1['label'] == 0]
    d_1 = data1[data1['label'] == 1]
    return len(d_1) / (len(d_1) + len(d_0))


# 返回类中的阴性点
def get_yin(index, data):
    data1 = data[index]
    d_0 = data1[data1['label'] == 0]
    num = d_0['number']
    return num


data0 = dataUtil.load_data('../data/data.csv')
# 标准化
# data0 = dataUtil.standardization(data0)
data = data0.iloc[:, 1:data0.shape[1] - 1]
# data0 = data0.iloc[:, 1:]
# data0 = data0.drop(['wzqdcsd', 'wzqdcsC', 'wzqdcsA', 'wzqdcsB'], axis=1)
# data0 = data0.drop(['wzqdcsC', 'wzqdcsA', 'wzqdcsB'], axis=1)
# 归一化
# data = dataUtil.scale(data)
best_j = []  # 类别个数
best_sc = []  # 比例
best_i = []  # 第几类
num_list = set()  # 创建集合，存储num，不重复
print(data)
for j in range(2, 100):
    print('*' * 20, j)
    cluster_model = KMeans(n_clusters=j, random_state=4)
    cluster_model.fit(data)
    labels = np.array(cluster_model.labels_)
    print('labels:', labels)
    for i in range(j):
        print('*' * 10, i)
        index = (labels == i)
        if len(index) == 0:
            continue
        sc = get_probability(index, data0)
        print('类别:', i)
        print('阳性占比：', sc)
        if sc >0.8:
            best_i.append(i)
            best_j.append(j)
            best_sc.append(sc)
            num = get_yin(index, data0)
            print('num：', num)
            num_list.update(num)
            print('num_list:', num_list)
print('best_i:', best_i)
print('best_j:', best_j)
print('best_sc:', best_sc)
print('num_list:', num_list)
# clusters = pd.Series(cluster_model.labels_)


# print(clusters)
# data['pre-label'] = clusters
# print(data)


# n = clusters.value_counts().sort_index()
# print(n)
# print(data)
# picutil.draw_matrix(clusters, data['label'])
# 计算准确率
# acc = dataUtil.get_acc(data['label'], clusters)
# print('acc：', acc)
# ROC
# fpr, tpr, auc = dataUtil.get_ROC_AUC(data['label'], clusters)
# picutil.draw_AOC_AUC(fpr, tpr, auc)
