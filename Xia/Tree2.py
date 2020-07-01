# MAX = 999999  # 定义最大数
M = 999999  # 定义最大数
import networkx as nx  # 绘图
import matplotlib.pyplot as plt


class Start(object):  # 创建类
    def __init__(self, lin, n):  # 基类对象，在这里用于传入参数和初始化类
        self.lin = lin  # 传入邻接矩阵
        self.n = n  # 传入节点总个数
        self.bian = self.get_bian()  # 根据邻接矩阵，获得无向连接图的边数

    def get_bian(self):  # 类中的获取边数的方法
        count = 0  # 初始化边数变量
        for i in range(self.n):  # 循环遍历整个邻接矩阵获得边数
            for j in range(i):  # 内循环
                if self.lin[i][j] != 0 and self.lin[i][j] != 999:  # 如果不是本身（！=0）或者不连接（！=-1）则为一条边
                    count += 1  # 符合条件边数加1
        return count  # 返回边数

    def Prim(self):  # Prim算法
        s = [0]  # 记录已经存在与最小生成树的节点
        o = [i for i in range(1, self.n)]  # 将每一个节点分开存放方便遍历
        quan = 0  # 总权重
        rex = []  # 结果列表
        while len(o) > 0:  # 循环生成最小生成树
            dian1, dian2, temp = 0, 0, M  # 定义标志变量=0代表自身，=MAX代表不连通
            for j in s:  # 遍历已经存在于最小生成树的节点
                for i in o:  # 遍历每不存在于最小生成树的节点
                    if self.lin[j][i] == 999 or self.lin[j][i] == 0:  # 如果连两个节点不连通，继续循环
                        continue  # 继续循环
                    else:  ##如果联通
                        if temp > self.lin[j][i]:  # 选择存在于最小生成树和不存在于最小生成树的两个节点中边权最小的节点
                            temp = self.lin[j][i]  # 中间变量存储最小边权
                            dian1 = i  # 中间变量不存在于最小生成树的点
                            dian2 = j  # 中间变量存在于最小生成树的点
            quan += temp  # 计算总边权
            rex.append([dian2, dian1, temp])  # 将此节点存于结果中
            s.append(dian1)  # 将不存在于最小生成树的节点插入到最小生成树的节点
            o.remove(dian1)  # 在不存在于最小生成树的列表中删除此节点
        rex.append(quan)  # 将总边权插入到最终结果
        return rex  # 返回

    def Kruskal(self):  # Kruskal算法
        s = 0  # 初始化总边权
        rex = []  # 定义最小生成树的每一条边的列表
        a = []  # 定义边的列表
        for i in range(self.n):  # 循环遍历整个邻接矩阵
            for j in range(self.n):  # 内循环
                if self.lin[i][j] != -1 and self.lin[i][j] != 0:  # 如果不是本身（！=0）或者不连接（！=-1）则为一条边
                    a.append([i, j, self.lin[i][j]])  # 将边以两个节点和一个边权的格式存储
        a.sort(key=lambda a: a[2])  # 对每个边以边权排序
        group = [[i] for i in range(self.n)]  # 初始化，将每个节点看作一个连通分支
        for e in a:  # 循环遍历边的列表
            for i in range(group.__len__()):  # 循环遍历每个连通分支
                if e[0] in group[i]:  # 判断这个边的一个节点是否在这个连通分支内
                    m = i  # 如果是记录下来
                if e[1] in group[i]:  # 判断这个边的另一个节点是否在这个连通分支内
                    n = i  # 如果是记录下来
            if m != n:  # 如果这条边的两个节点在两个连通分支内，则可以选择此边
                rex.append(e)  # 将结果储存
                s += e[2]  # 计算总边权
                group[m] = group[m] + group[n]  # 将两个连通分支合并
                group[n] = []  # 将另一个联通分支清空
        rex.append(s)  # 将总边权加入到结果列表
        return rex  # 返回


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
    plt.savefig('./xia.png', dpi=400, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    # n = int(input("请输入节点个数："))  # 输入节点个数
    # lin = []  # 定义邻接矩阵的列表
    # 节点
    # node = [1, 2, 3, 4, 5, 6]
    node = [0, 1, 2, 3, 4, 5]
    n = len(node)
    # 用矩阵表示边的权值
    lin = [
        [M, 6, 1, 5, M, M],
        [M, M, 5, M, 3, M],
        [M, M, M, 5, 6, 4],
        [M, M, M, M, M, 2],
        [M, M, M, M, M, 6],
        [M, M, M, M, M, M]
    ]
    # for i in range(n):  # 循环输入邻接矩阵
    #     print("请输入邻接矩阵第", i + 1, "行：(每个元素以 空格 隔开，自身为 0，两点之间无直线连接为 -1)")  # 以行为单位一行一行输入
    #     q = input()  # 用变量接受输入的字符串
    #     q = q.split(" ")  # 将字符串转化为列表
    #     q = list(map(int, q))  # 将列表中的字符串转化为int类型
    #     lin.append(q)  # 将输入的每一行加入到邻接矩阵中
    # print("您输入的邻接矩阵为：")  # 输出用户输入的邻接矩阵，用于用户检验错误
    # for i in lin:  # 循环一行一行输出
    #     print(i)  # 输出
    print("开始Prim算法...")  # 提示语句
    start = Start(lin, n)  # 创建类的对象
    qq = start.Prim()  # 调用类中Prim方法，开始进行Prim生成最小生成树
    print("Prim最小生成树为：[开始点，结束点，权]")  # 输出Prim最小生成树结果
    qq.pop(len(qq) - 1)
    print(qq)  # 输出
    draw_net(node=node, edges=qq)
    print("*******************************************************************")
    print("开始Kruskal算法...")  # 提示语句
    pp = start.Kruskal()  # 开始Kruskal算法
    print("Kruskal最小生成树为：[开始点，结束点，权]")  # 输出结果
    pp.pop(len(pp) - 1)
    print(pp)  # 输出
    draw_net(node=node, edges=pp)
