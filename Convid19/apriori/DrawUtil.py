# encoding=utf-8
"""
@Time : 2020/4/2 22:40 
@Author : LiuYanZhe
@File : DrawUtil.py 
@Software: PyCharm
@Description: Apriori绘图工具
"""
import networkx as nx
import matplotlib.pyplot as plt


def Draw(map_list, word_list, pic_path, title='DiGraph'):
    # 绘图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
    G = nx.DiGraph()
    colors = range(20)
    G.add_nodes_from(word_list)  # 设置节点
    G.add_weighted_edges_from(map_list)  # 设置边
    # pos = nx.circular_layout(G)   #节点在一个圆环上均匀分布
    # pos = nx.random_layout(G)  # 节点随机分布
    pos = nx.shell_layout(G)  # 节点在同心圆上分布
    # pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    # pos = nx.spectral_layout(G)  # 根据图的拉普拉斯特征向量排列节点
    # 绘制网络图
    # nx.draw(G, pos, with_labels=True, width=0.5, node_size=6, alpha=0.8, font_weight='bold', font_size=7,
    #         font_color='r')
    # 绘制网络图-边宽为权重
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] * 3) for (r, c, v) in G.edges(data=True)], node_size=950,
            alpha=0.8, font_weight='bold', font_size=14,
            font_color='r')
    # plt.title(title + '  DiGraph')
    plt.title(title, y=-0.05,fontsize=16)
    plt.savefig(pic_path, dpi=600, bbox_inches='tight')
    plt.show()


def Draw4(map_list1, word_list1, map_list2, word_list2, map_list3, word_list3, map_list4, word_list4, pic_path,
          title='DiGraph'):
    TITLE1 = 'January 1 to March 28'
    TITLE2 = 'January 1 to January 25'
    TITLE3 = 'January 26 to February 16'
    TITLE4 = 'February 17 to March 28'
    # 绘图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
    G = nx.DiGraph()
    # G = nx.grid_2d_graph(4, 4)
    plt.subplot(221)
    G.add_nodes_from(word_list1)  # 设置节点
    G.add_weighted_edges_from(map_list1)  # 设置边
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] * 2) for (r, c, v) in G.edges(data=True)], node_size=250,
            alpha=0.8, font_weight='bold', font_size=8,
            font_color='r')
    plt.title(TITLE1 + '  DiGraph')

    plt.subplot(222)
    G.add_nodes_from(word_list2)  # 设置节点
    G.add_weighted_edges_from(map_list2)  # 设置边
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] * 2) for (r, c, v) in G.edges(data=True)], node_size=250,
            alpha=0.8, font_weight='bold', font_size=8,
            font_color='r')
    plt.title(TITLE2 + '  DiGraph')

    plt.subplot(223)
    G.add_nodes_from(word_list3)  # 设置节点
    G.add_weighted_edges_from(map_list3)  # 设置边
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] * 2) for (r, c, v) in G.edges(data=True)], node_size=250,
            alpha=0.8, font_weight='bold', font_size=8,
            font_color='r')
    plt.title(TITLE3 + '  DiGraph')

    plt.subplot(224)
    G.add_nodes_from(word_list4)  # 设置节点
    G.add_weighted_edges_from(map_list4)  # 设置边
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] * 2) for (r, c, v) in G.edges(data=True)], node_size=250,
            alpha=0.8, font_weight='bold', font_size=8,
            font_color='r')
    plt.title(TITLE4 + '  DiGraph')

    plt.savefig(pic_path, dpi=1200, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # pic_path='apriori_main'
    # map_list1=[['发展', '疫情', 0.2840909090909091], ['发展', '防控', 0.20454545454545456], ['复工', '发展', 0.13636363636363635], ['复工', '疫情', 0.29545454545454547], ['复工', '防控', 0.22727272727272727], ['疫情', '防控', 0.6136363636363636], ['防控', '疫情', 0.6136363636363636], ['发展', '工作', 0.19318181818181818], ['发展', '疫情', 0.2840909090909091], ['发展', '防控', 0.20454545454545456], ['工作', '发展', 0.19318181818181818], ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635], ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636], ['发展', '疫情', 0.2840909090909091], ['发展', '防控', 0.20454545454545456], ['疫情', '防控', 0.6136363636363636], ['英雄', '发展', 0.13636363636363635], ['英雄', '疫情', 0.22727272727272727], ['英雄', '防控', 0.20454545454545456], ['防控', '疫情', 0.6136363636363636], ['复工', '工作', 0.17045454545454544], ['复工', '疫情', 0.29545454545454547], ['复工', '防控', 0.22727272727272727], ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635], ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636], ['复工', '疫情', 0.29545454545454547], ['复工', '联控', 0.14772727272727273], ['复工', '防控', 0.22727272727272727], ['疫情', '防控', 0.6136363636363636], ['联控', '复工', 0.14772727272727273], ['联控', '疫情', 0.2840909090909091], ['联控', '防控', 0.22727272727272727], ['防控', '疫情', 0.6136363636363636], ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['武汉', '工作', 0.125], ['武汉', '疫情', 0.25], ['武汉', '防控', 0.2159090909090909], ['疫情', '工作', 0.38636363636363635], ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636], ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635], ['疫情', '防控', 0.6136363636363636], ['英雄', '工作', 0.13636363636363635], ['英雄', '疫情', 0.22727272727272727], ['英雄', '防控', 0.20454545454545456], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636]]
    # word_list1={'联控', '疫情', '英雄', '复工', '发展', '工作', '武汉', '防控'}
    # map_list2=[['使命', '发展', 0.24], ['使命', '基层', 0.2], ['使命', '治理', 0.2], ['发展', '使命', 0.24], ['发展', '基层', 0.28], ['发展', '治理', 0.28], ['基层', '发展', 0.28], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '基层', 0.24], ['使命', '发展', 0.24], ['使命', '基层', 0.2], ['使命', '牢记', 0.32], ['发展', '使命', 0.24], ['发展', '基层', 0.28], ['发展', '牢记', 0.2], ['基层', '发展', 0.28], ['牢记', '使命', 0.32], ['牢记', '发展', 0.2], ['牢记', '基层', 0.16], ['使命', '发展', 0.24], ['使命', '治理', 0.2], ['使命', '牢记', 0.32], ['发展', '使命', 0.24], ['发展', '治理', 0.28], ['发展', '牢记', 0.2], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '牢记', 0.16], ['牢记', '使命', 0.32], ['牢记', '发展', 0.2], ['牢记', '治理', 0.16], ['使命', '发展', 0.24], ['使命', '治理', 0.2], ['使命', '经济', 0.16], ['发展', '使命', 0.24], ['发展', '治理', 0.28], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '经济', 0.16], ['经济', '使命', 0.16], ['经济', '发展', 0.12], ['经济', '治理', 0.16], ['使命', '教育', 0.16], ['使命', '牢记', 0.32], ['工作', '使命', 0.12], ['工作', '教育', 0.12], ['工作', '牢记', 0.12], ['教育', '使命', 0.16], ['教育', '工作', 0.12], ['教育', '牢记', 0.2], ['牢记', '使命', 0.32], ['牢记', '教育', 0.2]]
    # word_list2={'使命', '发展', '教育', '牢记', '经济', '基层', '治理', '工作'}
    # map_list3=[['发展', '武汉', 0.13636363636363635], ['发展', '疫情', 0.18181818181818182], ['发展', '社区', 0.13636363636363635], ['发展', '防控', 0.18181818181818182], ['武汉', '疫情', 0.5], ['武汉', '社区', 0.22727272727272727], ['武汉', '防控', 0.5], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['社区', '发展', 0.13636363636363635], ['社区', '武汉', 0.22727272727272727], ['社区', '疫情', 0.2727272727272727], ['社区', '防控', 0.2727272727272727], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['城市', '工作', 0.13636363636363635], ['城市', '武汉', 0.13636363636363635], ['城市', '疫情', 0.18181818181818182], ['城市', '防控', 0.18181818181818182], ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['武汉', '工作', 0.3181818181818182], ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['基层', '新春', 0.13636363636363635], ['基层', '疫情', 0.18181818181818182], ['基层', '防控', 0.18181818181818182], ['基层', '阻击战', 0.13636363636363635], ['新春', '基层', 0.13636363636363635], ['新春', '疫情', 0.18181818181818182], ['新春', '防控', 0.18181818181818182], ['新春', '阻击战', 0.13636363636363635], ['疫情', '防控', 1.0], ['疫情', '阻击战', 0.4090909090909091], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091], ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091], ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['应收', '工作', 0.18181818181818182], ['应收', '武汉', 0.22727272727272727], ['应收', '疫情', 0.2727272727272727], ['应收', '防控', 0.2727272727272727], ['武汉', '工作', 0.3181818181818182], ['武汉', '应收', 0.22727272727272727], ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['打赢', '工作', 0.22727272727272727], ['打赢', '疫情', 0.36363636363636365], ['打赢', '防控', 0.36363636363636365], ['打赢', '阻击战', 0.2727272727272727], ['疫情', '工作', 0.5909090909090909], ['疫情', '防控', 1.0], ['疫情', '阻击战', 0.4090909090909091], ['防控', '工作', 0.5909090909090909], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091], ['阻击战', '工作', 0.22727272727272727], ['阻击战', '打赢', 0.2727272727272727], ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091], ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['武汉', '工作', 0.3181818181818182], ['武汉', '疫情', 0.5], ['武汉', '社区', 0.22727272727272727], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['社区', '工作', 0.18181818181818182], ['社区', '武汉', 0.22727272727272727], ['社区', '疫情', 0.2727272727272727], ['社区', '防控', 0.2727272727272727], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['武汉', '工作', 0.3181818181818182], ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['疫情', '阻击战', 0.4090909090909091], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091], ['阻击战', '工作', 0.22727272727272727], ['阻击战', '武汉', 0.18181818181818182], ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091], ['打赢', '疫情', 0.36363636363636365], ['打赢', '防控', 0.36363636363636365], ['打赢', '阻击战', 0.2727272727272727], ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['疫情', '阻击战', 0.4090909090909091], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091], ['阻击战', '打赢', 0.2727272727272727], ['阻击战', '武汉', 0.18181818181818182], ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091]]
    # word_list3={'新春', '疫情', '发展', '基层', '打赢', '应收', '工作', '社区', '武汉', '城市', '阻击战', '防控'}
    # map_list4=[['发展', '复工', 0.2682926829268293], ['发展', '工作', 0.2682926829268293], ['发展', '疫情', 0.5121951219512195], ['发展', '防控', 0.34146341463414637], ['复工', '发展', 0.2682926829268293], ['复工', '工作', 0.3170731707317073], ['复工', '疫情', 0.5853658536585366], ['复工', '防控', 0.43902439024390244], ['工作', '发展', 0.2682926829268293], ['工作', '复工', 0.3170731707317073], ['工作', '疫情', 0.5121951219512195], ['工作', '防控', 0.4146341463414634], ['疫情', '发展', 0.5121951219512195], ['疫情', '复工', 0.5853658536585366], ['疫情', '工作', 0.5121951219512195], ['疫情', '防控', 0.7560975609756098], ['防控', '发展', 0.34146341463414637], ['防控', '复工', 0.43902439024390244], ['防控', '工作', 0.4146341463414634], ['防控', '疫情', 0.7560975609756098], ['发展', '复工', 0.2682926829268293], ['发展', '疫情', 0.5121951219512195], ['发展', '联控', 0.2682926829268293], ['发展', '防控', 0.34146341463414637], ['复工', '发展', 0.2682926829268293], ['复工', '疫情', 0.5853658536585366], ['复工', '联控', 0.3170731707317073], ['复工', '防控', 0.43902439024390244], ['疫情', '发展', 0.5121951219512195], ['疫情', '复工', 0.5853658536585366], ['疫情', '联控', 0.4878048780487805], ['疫情', '防控', 0.7560975609756098], ['联控', '发展', 0.2682926829268293], ['联控', '复工', 0.3170731707317073], ['联控', '疫情', 0.4878048780487805], ['联控', '防控', 0.3902439024390244], ['防控', '发展', 0.34146341463414637], ['防控', '复工', 0.43902439024390244], ['防控', '疫情', 0.7560975609756098], ['防控', '联控', 0.3902439024390244], ['发展', '工作', 0.2682926829268293], ['发展', '疫情', 0.5121951219512195], ['发展', '英雄', 0.24390243902439024], ['发展', '防控', 0.34146341463414637], ['工作', '发展', 0.2682926829268293], ['工作', '疫情', 0.5121951219512195], ['工作', '英雄', 0.24390243902439024], ['工作', '防控', 0.4146341463414634], ['疫情', '发展', 0.5121951219512195], ['疫情', '工作', 0.5121951219512195], ['疫情', '防控', 0.7560975609756098], ['英雄', '发展', 0.24390243902439024], ['英雄', '工作', 0.24390243902439024], ['英雄', '疫情', 0.3902439024390244], ['英雄', '防控', 0.34146341463414637], ['防控', '发展', 0.34146341463414637], ['防控', '工作', 0.4146341463414634], ['防控', '疫情', 0.7560975609756098], ['防控', '英雄', 0.34146341463414637], ['复工', '工作', 0.3170731707317073], ['复工', '疫情', 0.5853658536585366], ['复工', '防控', 0.43902439024390244], ['工作', '复工', 0.3170731707317073], ['工作', '疫情', 0.5121951219512195], ['工作', '英雄', 0.24390243902439024], ['工作', '防控', 0.4146341463414634], ['疫情', '复工', 0.5853658536585366], ['疫情', '工作', 0.5121951219512195], ['疫情', '防控', 0.7560975609756098], ['英雄', '复工', 0.17073170731707318], ['英雄', '工作', 0.24390243902439024], ['英雄', '疫情', 0.3902439024390244], ['英雄', '防控', 0.34146341463414637], ['防控', '复工', 0.43902439024390244], ['防控', '工作', 0.4146341463414634], ['防控', '疫情', 0.7560975609756098], ['防控', '英雄', 0.34146341463414637], ['复工', '疫情', 0.5853658536585366], ['复工', '联控', 0.3170731707317073], ['复工', '防控', 0.43902439024390244], ['疫情', '复工', 0.5853658536585366], ['疫情', '联控', 0.4878048780487805], ['疫情', '防控', 0.7560975609756098], ['联控', '复工', 0.3170731707317073], ['联控', '疫情', 0.4878048780487805], ['联控', '防控', 0.3902439024390244], ['脱贫', '复工', 0.1951219512195122], ['脱贫', '疫情', 0.2682926829268293], ['脱贫', '联控', 0.17073170731707318], ['脱贫', '防控', 0.2682926829268293], ['防控', '复工', 0.43902439024390244], ['防控', '疫情', 0.7560975609756098], ['防控', '联控', 0.3902439024390244]]
    # word_list4={'工作', '英雄', '脱贫', '疫情', '复工', '联控', '防控', '发展'}
    # Draw4(word_list1=word_list1,map_list1=map_list1,word_list2=word_list2,map_list2=map_list2,word_list3=word_list3,map_list3=map_list3,word_list4=word_list4,map_list4=map_list4,pic_path=pic_path)
    PICNAME1 = '../pic/apriori_title.png'
    PICNAME2 = '../pic/apriori_title1.png'
    PICNAME3 = '../pic/apriori_title2.png'
    PICNAME4 = '../pic/apriori_title3.png'
    TITLE1 = 'January 1 to March 28'
    TITLE2 = 'January 1 to January 25'
    TITLE3 = 'January 26 to February 16'
    TITLE4 = 'February 17 to March 28'
    map_list1 = [['发展', '疫情', 0.2840909090909091], ['发展', '防控', 0.20454545454545456], ['复工', '发展', 0.13636363636363635],
                 ['复工', '疫情', 0.29545454545454547], ['复工', '防控', 0.22727272727272727], ['疫情', '防控', 0.6136363636363636],
                 ['防控', '疫情', 0.6136363636363636], ['发展', '工作', 0.19318181818181818], ['发展', '疫情', 0.2840909090909091],
                 ['发展', '防控', 0.20454545454545456], ['工作', '发展', 0.19318181818181818],
                 ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635],
                 ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636],
                 ['发展', '疫情', 0.2840909090909091], ['发展', '防控', 0.20454545454545456], ['疫情', '防控', 0.6136363636363636],
                 ['英雄', '发展', 0.13636363636363635], ['英雄', '疫情', 0.22727272727272727],
                 ['英雄', '防控', 0.20454545454545456], ['防控', '疫情', 0.6136363636363636], ['复工', '工作', 0.17045454545454544],
                 ['复工', '疫情', 0.29545454545454547], ['复工', '防控', 0.22727272727272727],
                 ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635],
                 ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636],
                 ['复工', '疫情', 0.29545454545454547], ['复工', '联控', 0.14772727272727273],
                 ['复工', '防控', 0.22727272727272727], ['疫情', '防控', 0.6136363636363636], ['联控', '复工', 0.14772727272727273],
                 ['联控', '疫情', 0.2840909090909091], ['联控', '防控', 0.22727272727272727], ['防控', '疫情', 0.6136363636363636],
                 ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['武汉', '工作', 0.125],
                 ['武汉', '疫情', 0.25], ['武汉', '防控', 0.2159090909090909], ['疫情', '工作', 0.38636363636363635],
                 ['疫情', '防控', 0.6136363636363636], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636],
                 ['工作', '疫情', 0.38636363636363635], ['工作', '防控', 0.3409090909090909], ['疫情', '工作', 0.38636363636363635],
                 ['疫情', '防控', 0.6136363636363636], ['英雄', '工作', 0.13636363636363635], ['英雄', '疫情', 0.22727272727272727],
                 ['英雄', '防控', 0.20454545454545456], ['防控', '工作', 0.3409090909090909], ['防控', '疫情', 0.6136363636363636]]
    word_list1 = {'联控', '疫情', '英雄', '复工', '发展', '工作', '武汉', '防控'}
    map_list2 = [['使命', '发展', 0.24], ['使命', '基层', 0.2], ['使命', '治理', 0.2], ['发展', '使命', 0.24], ['发展', '基层', 0.28],
                 ['发展', '治理', 0.28], ['基层', '发展', 0.28], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '基层', 0.24],
                 ['使命', '发展', 0.24], ['使命', '基层', 0.2], ['使命', '牢记', 0.32], ['发展', '使命', 0.24], ['发展', '基层', 0.28],
                 ['发展', '牢记', 0.2], ['基层', '发展', 0.28], ['牢记', '使命', 0.32], ['牢记', '发展', 0.2], ['牢记', '基层', 0.16],
                 ['使命', '发展', 0.24], ['使命', '治理', 0.2], ['使命', '牢记', 0.32], ['发展', '使命', 0.24], ['发展', '治理', 0.28],
                 ['发展', '牢记', 0.2], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '牢记', 0.16], ['牢记', '使命', 0.32],
                 ['牢记', '发展', 0.2], ['牢记', '治理', 0.16], ['使命', '发展', 0.24], ['使命', '治理', 0.2], ['使命', '经济', 0.16],
                 ['发展', '使命', 0.24], ['发展', '治理', 0.28], ['治理', '使命', 0.2], ['治理', '发展', 0.28], ['治理', '经济', 0.16],
                 ['经济', '使命', 0.16], ['经济', '发展', 0.12], ['经济', '治理', 0.16], ['使命', '教育', 0.16], ['使命', '牢记', 0.32],
                 ['工作', '使命', 0.12], ['工作', '教育', 0.12], ['工作', '牢记', 0.12], ['教育', '使命', 0.16], ['教育', '工作', 0.12],
                 ['教育', '牢记', 0.2], ['牢记', '使命', 0.32], ['牢记', '教育', 0.2]]
    word_list2 = {'使命', '发展', '教育', '牢记', '经济', '基层', '治理', '工作'}
    map_list3 = [['发展', '武汉', 0.13636363636363635], ['发展', '疫情', 0.18181818181818182],
                 ['发展', '社区', 0.13636363636363635], ['发展', '防控', 0.18181818181818182], ['武汉', '疫情', 0.5],
                 ['武汉', '社区', 0.22727272727272727], ['武汉', '防控', 0.5], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0],
                 ['社区', '发展', 0.13636363636363635], ['社区', '武汉', 0.22727272727272727], ['社区', '疫情', 0.2727272727272727],
                 ['社区', '防控', 0.2727272727272727], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0],
                 ['城市', '工作', 0.13636363636363635], ['城市', '武汉', 0.13636363636363635],
                 ['城市', '疫情', 0.18181818181818182], ['城市', '防控', 0.18181818181818182], ['工作', '武汉', 0.3181818181818182],
                 ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['武汉', '工作', 0.3181818181818182],
                 ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5],
                 ['疫情', '防控', 1.0], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0],
                 ['基层', '新春', 0.13636363636363635], ['基层', '疫情', 0.18181818181818182],
                 ['基层', '防控', 0.18181818181818182], ['基层', '阻击战', 0.13636363636363635],
                 ['新春', '基层', 0.13636363636363635], ['新春', '疫情', 0.18181818181818182],
                 ['新春', '防控', 0.18181818181818182], ['新春', '阻击战', 0.13636363636363635], ['疫情', '防控', 1.0],
                 ['疫情', '阻击战', 0.4090909090909091], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091],
                 ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091], ['工作', '武汉', 0.3181818181818182],
                 ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['应收', '工作', 0.18181818181818182],
                 ['应收', '武汉', 0.22727272727272727], ['应收', '疫情', 0.2727272727272727], ['应收', '防控', 0.2727272727272727],
                 ['武汉', '工作', 0.3181818181818182], ['武汉', '应收', 0.22727272727272727], ['武汉', '疫情', 0.5],
                 ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0],
                 ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0],
                 ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909], ['打赢', '工作', 0.22727272727272727],
                 ['打赢', '疫情', 0.36363636363636365], ['打赢', '防控', 0.36363636363636365],
                 ['打赢', '阻击战', 0.2727272727272727], ['疫情', '工作', 0.5909090909090909], ['疫情', '防控', 1.0],
                 ['疫情', '阻击战', 0.4090909090909091], ['防控', '工作', 0.5909090909090909], ['防控', '疫情', 1.0],
                 ['防控', '阻击战', 0.4090909090909091], ['阻击战', '工作', 0.22727272727272727],
                 ['阻击战', '打赢', 0.2727272727272727], ['阻击战', '疫情', 0.4090909090909091],
                 ['阻击战', '防控', 0.4090909090909091], ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909],
                 ['工作', '防控', 0.5909090909090909], ['武汉', '工作', 0.3181818181818182], ['武汉', '疫情', 0.5],
                 ['武汉', '社区', 0.22727272727272727], ['武汉', '防控', 0.5], ['疫情', '工作', 0.5909090909090909],
                 ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['社区', '工作', 0.18181818181818182],
                 ['社区', '武汉', 0.22727272727272727], ['社区', '疫情', 0.2727272727272727], ['社区', '防控', 0.2727272727272727],
                 ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5], ['防控', '疫情', 1.0],
                 ['工作', '武汉', 0.3181818181818182], ['工作', '疫情', 0.5909090909090909], ['工作', '防控', 0.5909090909090909],
                 ['武汉', '工作', 0.3181818181818182], ['武汉', '疫情', 0.5], ['武汉', '防控', 0.5],
                 ['疫情', '工作', 0.5909090909090909], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0],
                 ['疫情', '阻击战', 0.4090909090909091], ['防控', '工作', 0.5909090909090909], ['防控', '武汉', 0.5],
                 ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091], ['阻击战', '工作', 0.22727272727272727],
                 ['阻击战', '武汉', 0.18181818181818182], ['阻击战', '疫情', 0.4090909090909091],
                 ['阻击战', '防控', 0.4090909090909091], ['打赢', '疫情', 0.36363636363636365],
                 ['打赢', '防控', 0.36363636363636365], ['打赢', '阻击战', 0.2727272727272727], ['武汉', '疫情', 0.5],
                 ['武汉', '防控', 0.5], ['疫情', '武汉', 0.5], ['疫情', '防控', 1.0], ['疫情', '阻击战', 0.4090909090909091],
                 ['防控', '武汉', 0.5], ['防控', '疫情', 1.0], ['防控', '阻击战', 0.4090909090909091],
                 ['阻击战', '打赢', 0.2727272727272727], ['阻击战', '武汉', 0.18181818181818182],
                 ['阻击战', '疫情', 0.4090909090909091], ['阻击战', '防控', 0.4090909090909091]]
    word_list3 = {'新春', '疫情', '发展', '基层', '打赢', '应收', '工作', '社区', '武汉', '城市', '阻击战', '防控'}
    map_list4 = [['发展', '复工', 0.2682926829268293], ['发展', '工作', 0.2682926829268293], ['发展', '疫情', 0.5121951219512195],
                 ['发展', '防控', 0.34146341463414637], ['复工', '发展', 0.2682926829268293], ['复工', '工作', 0.3170731707317073],
                 ['复工', '疫情', 0.5853658536585366], ['复工', '防控', 0.43902439024390244], ['工作', '发展', 0.2682926829268293],
                 ['工作', '复工', 0.3170731707317073], ['工作', '疫情', 0.5121951219512195], ['工作', '防控', 0.4146341463414634],
                 ['疫情', '发展', 0.5121951219512195], ['疫情', '复工', 0.5853658536585366], ['疫情', '工作', 0.5121951219512195],
                 ['疫情', '防控', 0.7560975609756098], ['防控', '发展', 0.34146341463414637], ['防控', '复工', 0.43902439024390244],
                 ['防控', '工作', 0.4146341463414634], ['防控', '疫情', 0.7560975609756098], ['发展', '复工', 0.2682926829268293],
                 ['发展', '疫情', 0.5121951219512195], ['发展', '联控', 0.2682926829268293], ['发展', '防控', 0.34146341463414637],
                 ['复工', '发展', 0.2682926829268293], ['复工', '疫情', 0.5853658536585366], ['复工', '联控', 0.3170731707317073],
                 ['复工', '防控', 0.43902439024390244], ['疫情', '发展', 0.5121951219512195], ['疫情', '复工', 0.5853658536585366],
                 ['疫情', '联控', 0.4878048780487805], ['疫情', '防控', 0.7560975609756098], ['联控', '发展', 0.2682926829268293],
                 ['联控', '复工', 0.3170731707317073], ['联控', '疫情', 0.4878048780487805], ['联控', '防控', 0.3902439024390244],
                 ['防控', '发展', 0.34146341463414637], ['防控', '复工', 0.43902439024390244], ['防控', '疫情', 0.7560975609756098],
                 ['防控', '联控', 0.3902439024390244], ['发展', '工作', 0.2682926829268293], ['发展', '疫情', 0.5121951219512195],
                 ['发展', '英雄', 0.24390243902439024], ['发展', '防控', 0.34146341463414637], ['工作', '发展', 0.2682926829268293],
                 ['工作', '疫情', 0.5121951219512195], ['工作', '英雄', 0.24390243902439024], ['工作', '防控', 0.4146341463414634],
                 ['疫情', '发展', 0.5121951219512195], ['疫情', '工作', 0.5121951219512195], ['疫情', '防控', 0.7560975609756098],
                 ['英雄', '发展', 0.24390243902439024], ['英雄', '工作', 0.24390243902439024], ['英雄', '疫情', 0.3902439024390244],
                 ['英雄', '防控', 0.34146341463414637], ['防控', '发展', 0.34146341463414637], ['防控', '工作', 0.4146341463414634],
                 ['防控', '疫情', 0.7560975609756098], ['防控', '英雄', 0.34146341463414637], ['复工', '工作', 0.3170731707317073],
                 ['复工', '疫情', 0.5853658536585366], ['复工', '防控', 0.43902439024390244], ['工作', '复工', 0.3170731707317073],
                 ['工作', '疫情', 0.5121951219512195], ['工作', '英雄', 0.24390243902439024], ['工作', '防控', 0.4146341463414634],
                 ['疫情', '复工', 0.5853658536585366], ['疫情', '工作', 0.5121951219512195], ['疫情', '防控', 0.7560975609756098],
                 ['英雄', '复工', 0.17073170731707318], ['英雄', '工作', 0.24390243902439024], ['英雄', '疫情', 0.3902439024390244],
                 ['英雄', '防控', 0.34146341463414637], ['防控', '复工', 0.43902439024390244], ['防控', '工作', 0.4146341463414634],
                 ['防控', '疫情', 0.7560975609756098], ['防控', '英雄', 0.34146341463414637], ['复工', '疫情', 0.5853658536585366],
                 ['复工', '联控', 0.3170731707317073], ['复工', '防控', 0.43902439024390244], ['疫情', '复工', 0.5853658536585366],
                 ['疫情', '联控', 0.4878048780487805], ['疫情', '防控', 0.7560975609756098], ['联控', '复工', 0.3170731707317073],
                 ['联控', '疫情', 0.4878048780487805], ['联控', '防控', 0.3902439024390244], ['脱贫', '复工', 0.1951219512195122],
                 ['脱贫', '疫情', 0.2682926829268293], ['脱贫', '联控', 0.17073170731707318], ['脱贫', '防控', 0.2682926829268293],
                 ['防控', '复工', 0.43902439024390244], ['防控', '疫情', 0.7560975609756098], ['防控', '联控', 0.3902439024390244]]
    word_list4 = {'工作', '英雄', '脱贫', '疫情', '复工', '联控', '防控', '发展'}
    # Draw(map_list1,word_list1,PICNAME1,TITLE1)
    # Draw(map_list2,word_list2,PICNAME2,TITLE2)
    # Draw(map_list3,word_list3,PICNAME3,TITLE3)
    Draw(map_list4, word_list4, PICNAME4, TITLE4)
