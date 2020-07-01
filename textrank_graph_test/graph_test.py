# encoding=utf-8
"""
@Time : 2020/3/29 13:19 
@Author : LiuYanZhe
@File : graph_test.py 
@Software: PyCharm
@Description: 
"""
import networkx as nx
import matplotlib.pyplot as plt

nodes = ['1', '2', '3', '4']  # 节点
edges = [['1', '2', 2], ['2', '3', 2], ['3', '4', 10]]  # 边
# edges = [('1', '2', 2), ('2', '3', 2), ('3', '4', 10)]  # 边
G = nx.Graph()
colors = range(20)
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

# pos = nx.circular_layout(G)   #节点在一个圆环上均匀分布
# pos = nx.random_layout(G) #节点随机分布
# pos = nx.spring_layout(G)#用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
# pos = nx.drawing.layout.spring_layout(G)
# pos = nx.shell_layout(G)  # 节点在同心圆上分布
pos = nx.spectral_layout(G)  # 根据图的拉普拉斯特征向量排列节点
nx.draw(G, pos, with_labels=True, width=0.5, node_size=3, font_weight='bold', font_size=6)

# nx.draw_networkx_edges(G, pos=nx.drawing.layout.spring_layout(G), edge_color='#000000', width=1)
# nx.draw_networkx_nodes(G, pos=nx.drawing.layout.spring_layout(G), node_color='red', node_size=7)


# nx.draw(G, pos=pos, node_color='#0000CD', edge_color='#000000', width=1, node_size=3, edge_cmap=plt.cm.gray,
#         with_labels=True,)
plt.show()
