# encoding=utf-8
"""
@Time : 2020/4/23 10:36 
@Author : LiuYanZhe
@File : DBSCAN_lyz.py 
@Software: PyCharm
@Description: DBSCAN聚类算法
"""
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

db = DBSCAN(eps=2,  # 邻域半径
            min_samples=3,  # 最小样本点数，MinPts
            metric='euclidean',
            metric_params=None,
            algorithm='auto',  # 'auto','ball_tree','kd_tree','brute',4个可选的参数 寻找最近邻点的算法，例如直接密度可达的点
            leaf_size=30,  # balltree,cdtree的参数
            p=None,  #
            n_jobs=1)
# 数据集
# data = np.array([[0, 0], [3, 8], [1, 1], [2, 2], [5, 3], [4, 8], [6, 3], [5, 4], [6, 4], [7, 5]])
data = np.array([[0, 7], [0, 6.5], [0, 6], [0, 5.5], [0, 5], [0, 4.5], [1, 4.5], [2, 4.5],
        [3, 7], [3.5, 6.5], [4, 6], [4.5, 5.5], [5, 6], [5.5, 6.5], [6, 7], [4.5, 5], [4.5, 4.5],
        [9, 7], [9.5, 7], [10, 7], [10.5, 7], [10.5, 6.5], [10, 6], [9.5, 5.5], [9, 5],
        [9, 4.5], [9.5, 4.5], [10, 4.5], [10.5, 4.5]])
db.fit(data)
label_list = db.labels_
print(label_list)
plt.figure()
plt.scatter(data[:, 0], data[:, 1], c=label_list)
plt.show()
