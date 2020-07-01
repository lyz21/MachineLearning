# encoding=utf-8
"""
@Time : 2020/4/30 15:21 
@Author : LiuYanZhe
@File : AlgorithmDesign.py 
@Software: PyCharm
@Description: 算法设计大作业
"""
import networkx as nx  # 绘图
import matplotlib.pyplot as plt
import numpy as np

# 全局变量
# M = float("inf")  # 无穷大浮点数
M = 2147483647  # 无穷大整数


# kruskal算法
# 判断是否可以添加
def choose(s_list, a, b):
    for S in s_list:
        if a in S and b in S:
            return 0

    return 1


# 合并
def merge(s_list):
    size = len(s_list)
    for i in range(size):
        for j in range(size):
            x = list(set(s_list[i] + s_list[j]))
            y = len(s_list[i]) + len(s_list[j])
            if i == j or s_list[i] == 0 or s_list[j] == 0:
                break
            elif len(x) < y:
                s_list[i] = x
                s_list[j] = [0]
    for item in s_list:
        if item == [0]:
            s_list.remove(item)
    return s_list


def kruskal(node, edges):
    # 已选节点
    s_list = []
    S = []
    new_edges = []
    # 排序
    edges = sorted(edges, key=lambda length: length[2], reverse=False)
    S.append(edges[0][0])
    S.append(edges[0][1])
    s_list.append(S)
    new_edges.append(edges[0])
    edges.pop(0)
    print('edges:', edges)
    print('new_edges:', new_edges)
    print('S:', S)
    print('s_list:', s_list)
    while len(new_edges) < len(node) - 1:
        print('-' * 20)
        a, b = edges[0][0], edges[0][1]
        if choose(s_list, a, b) == 1:  # 可以添加
            print('a,b:', a, b)
            print('s_list:', s_list)
            s_list.append([a, b])
            new_edges.append(edges[0])
            s_list = merge(s_list)
            print('new_edges:', new_edges)
            print('s_list:', s_list)
        edges.pop(0)
    return new_edges


# prim算法
def prim(node, weight):
    # 记录节点长度
    size = len(node)
    # 生成树
    S = []
    e = node.copy()
    # 初始化节点
    S.append(e[0])  # 加入第一个节点
    e.pop(0)  # 按索引删除
    print('node:', node)
    print('S,e:', S, e)
    edges = []
    # 循环找最小
    while len(S) < size:
        print('---' * 20)
        min_len = M  # 暂存最小值
        min_x, min_y = 0, 0  # 暂存最小值的下标
        for n in S:
            for j in e:
                if weight[n - 1][j - 1] < min_len:
                    min_x, min_y, min_len = n - 1, j - 1, weight[n - 1][j - 1]
        S.append(node[min_y])
        e.remove(node[min_y])  # 按元素删
        edges.append([min_x + 1, min_y + 1, min_len])
        print('S,e:', S, e)
        print('T:', edges)
    return edges


# 初始化数据
def init_data():
    # 节点
    node = [1, 2, 3, 4, 5, 6]
    # 用矩阵表示边的权值
    weight = [
        [M, 6, 1, 5, M, M],
        [M, M, 5, M, 3, M],
        [M, M, M, 5, 6, 4],
        [M, M, M, M, M, 2],
        [M, M, M, M, M, 6],
        [M, M, M, M, M, M]
    ]
    # 边
    edges = []
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            w = weight[i][j]
            if w != M:
                edges.append([i + 1, j + 1, weight[i][j]])
    return node, weight, edges


def init_data2(size):
    # 节点
    node = list(np.array(range(1, size + 1, 1)))
    weight = np.random.randint(1, 10, (size, size))
    print('节点：', node)
    # 转为上三角矩阵，即两点只有一条线
    for i in range(len(weight)):
        for j in range(i, len(weight[i])):
            weight[j][i] = M
    # 随机去除边
    i = 0
    while i < size / 2:
        i = np.random.randint(0, size)
        j = np.random.randint(0, size)
        weight[i][j] = M
        i += 1
    print('权值矩阵：', weight)
    # 边
    edges = []
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            w = weight[i][j]
            if w != M and w > 0:
                edges.append([i + 1, j + 1, w])
    return node, weight, edges


# 绘图
def draw_net(node, edges):
    G = nx.Graph()
    G.add_nodes_from(node)  # 设置节点
    G.add_weighted_edges_from(edges)  # 设置边
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    nx.draw(G, pos, with_labels=True, node_size=950, alpha=0.8, font_weight='bold', font_size=14, font_color='r')
    edge_labels = dict([((u, v,), format(d['weight'], '.0f'))
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=10)
    plt.savefig('./1.png', dpi=400, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # 初始化数据（两种方式）
    node, weight, edges = init_data()
    # node, weight, edges = init_data2(10)
    print(edges)
    # 绘制初始图像
    draw_net(node, edges)

    # 调用算法（两种）
    # edges = prim(node, weight)
    edges = kruskal(node, edges)

    # 绘制最简图
    draw_net(node, edges)
