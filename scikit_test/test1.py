# encoding=utf-8
"""
@Time : 2020/3/20 16:03
@Author : LiuYanZhe
@File : test1.py
@Software: PyCharm
@Description: 官方demo 使用scikit-opt中的遗传算法 解决TSP 问题
"""
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt
from sko.GA import GA_TSP

num_points = 17

# 随机生成点坐标
# points_coordinate = np.random.rand(num_points, 2)
points_coordinate = np.loadtxt('citys_LOCATION.txt')
# 距离矩阵
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


# 计算总距离
def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])


ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
best_points, best_distance = ga_tsp.run()
print('best_points:', best_points)
print('best_distance:', best_distance)
fig, ax = plt.subplots(1, 2)
# 连接两个矩阵
best_points_ = np.concatenate([best_points, [best_points[0]]])
best_points_coordinate = points_coordinate[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
ax[1].plot(ga_tsp.generation_best_Y)
plt.show()
