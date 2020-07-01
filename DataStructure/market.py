# encoding=utf-8
"""
@Time : 2020/4/13 11:07 
@Author : LiuYanZhe
@File : market.py 
@Software: PyCharm
@Description: 数据结构——超市设计问题
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math


# 求最短路径
def floyd(graph):
    dist = []
    for i in range(len(graph)):
        sub_dist = []
        for j in range(len(graph)):
            sub_dist.append(graph[i][j])
        dist.append(sub_dist[:])
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(graph)):
                if dist[j][i] + dist[i][k] < dist[j][k]:
                    dist[j][k] = dist[j][i] + dist[i][k]
    return dist


# 初始化
M = float("inf")  # 无穷大
# point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # 点
# point = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # 点
point = ['A', 'B', 'C', 'D']  # 点
point_len = len(point)
init_dis = np.random.randint(1, 10, (point_len, point_len))  # 距离
# init_freq0 = np.random.randint(1, 10, (point_len, point_len))  # 频率
# init_num0 = np.random.randint(1, 10, (point_len, point_len))  # 人数
init_freq = np.random.rand(point_len, point_len)
init_num = np.random.rand(point_len, point_len)
init_freq = np.abs(init_freq)
init_num = np.abs(init_num)
for i in range(point_len):
    for j in range(point_len):
        if math.log(init_freq[i][j]) != 0:
            init_freq[i][j] = 1.0 / math.log(init_freq[i][j])
        if math.log(init_num[i][j]) != 0:
            init_num[i][j] = 1.0 / math.log(init_num[i][j])
print('init_freq:', init_freq)
graph = init_dis * init_freq * init_num
# 消除同一顶点连线
for i in range(len(graph)):
    graph[i][i] = 0
print('graph:', graph)
# 随机取消某两点间连线
for i in range(3):
    temp_x = np.random.randint(0, point_len)
    temp_y = np.random.randint(0, point_len)
    graph[temp_x, temp_y] = M

# graph = [[0, 4, M, 2, M],
#          [4, 0, 4, 1, M],
#          [M, 4, 0, 1, M],
#          [2, 1, 1, 0, M],
#          [M, M, M, M, M]]

dist = floyd(graph)
min_dis = 0
min_point = 0
# 计算总路程长
for i in range(len(dist)):
    temp_dis = 0
    # 正向
    for item in dist[i]:
        temp_dis += item
    # 反向
    for j in range(len(dist[i])):
        temp_dis += dist[j][i]
    if min_dis == 0:
        min_dis = temp_dis
        min_point = i
    elif min_dis > temp_dis:
        min_dis = temp_dis
        min_point = i
print('dist:', dist)
print('min_dis:', min_dis)
print('min_point:', min_point)

# 绘图
G = nx.DiGraph()
G.add_nodes_from(point)  # 设置节点
# 边
edges = []
for i in range(point_len):
    for j in range(point_len):
        # 正向
        temp_dis1 = dist[i][j]
        if temp_dis1 != 0:
            point1 = point[i]
            point2 = point[j]
            edges.append([point1, point2, temp_dis1])
        # 反向
        temp_dis2 = dist[j][i]
        if temp_dis1 != 0:
            point1 = point[j]
            point2 = point[i]
            edges.append([point1, point2, temp_dis2])
G.add_weighted_edges_from(edges)  # 设置边
# pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
# pos = nx.spectral_layout(G)  # 根据图的拉普拉斯特征向量排列节点
# pos = nx.circular_layout(G)   #节点在一个圆环上均匀分布
pos = nx.shell_layout(G)  # 节点在同心圆上分布
nx.draw(G, pos, with_labels=True, width=[float(v['weight'] / 5) for (r, c, v) in G.edges(data=True)], node_size=950,
        alpha=0.8, font_weight='bold', font_size=14,
        font_color='r')
edge_labels = dict([((u, v,), format(d['weight'], '.2f'))
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=10)
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文标签
plt.text(-1, 1, '超市选点：' + str(point[min_point] + '\n最短来回路径长为：' + str(min_dis)), fontsize=14)
plt.show()
