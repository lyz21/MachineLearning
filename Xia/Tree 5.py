import matplotlib.pyplot as plt
import networkx as nx

node = [1, 2, 3, 4, 5, 6, ]
# G = [
#     {5: 10, 1: 28},  # 0
#     {0: 28, 6: 14, 2: 16},  # 1
#     {1: 16, 3: 12},  # 2
#     {2: 12, 4: 22, 6: 18},  # 3
#     {3: 22, 5: 25, 6: 24},  # 4
#     {0: 10, 4: 25},  # 5
#     {1: 14, 3: 18, 4: 24}  # 6
# ]
G = [
    {2: 6, 3: 1, 4: 5},  # 1
    {1: 6, 3: 5, 5: 3, },  # 2
    {1: 1, 2: 5, 4: 5, 5: 6, 6: 4, },  # 3
    {1: 5, 3: 5, 6: 2},  # 4
    {2: 3, 3: 6, 6: 6, },  # 5
    {3: 4, 4: 2, 5: 6}  # 6
]
import heapq


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


def prim(G):
    # 这个图的顶点个数，prim算法的边数就是顶点数减一

    n = len(G)

    # 从第一个顶点开始

    v = 0
    # 这个集合避免重复的顶点被重复执行，造成无限循环
    s = {v}  # 存放边的值
    edges = []  # 存放结果
    res = []
    for _ in range(n - 1):  # 对字典进行解包
        for u, w in G[v].items():  # hwapq优先级队列回自动弹出最小值，默认以元祖中第一个元素排序
            # 所以第一个参数w代表权值，v，u表示两个顶点
            heapq.heappush(edges, (w, v, u))  # 循环条件，只有当我们的边存在才会进行循环
        while edges:  # 对优先级队列中的边进行拆包，拿出权值最小的那个边
            w, p, q = heapq.heappop(edges)

            if q not in s:  # 访问一个顶点，就把这个顶点放进集合中
                s.add(q)  # 把最小的边加入到我们的结果中
                res.append(((p, q), w))  # 把下一个顶点作为起始顶点
                v = q  # 然后推出这一次的顶点，操作下一个顶点
                break
    return res


list_t = prim(G)
print(list_t)

list_t_new = []
for ege in list_t:
    list_t_new.append([ege[0][0], ege[0][1], ege[1]])
draw_net(node, list_t_new)
