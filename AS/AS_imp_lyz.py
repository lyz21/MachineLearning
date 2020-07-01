# encoding=utf-8
"""
Name:         ACS_lyz
Description:  蚁群算法- 第三版 - Ant-Cycle模型
Author:       LiuYanZhe
Date:         2019/10/28
"""
import logging
import math
import random

import numpy as np

from AS import way_plt

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志
logging.disable()
'''全局变量'''
# 最大循环次数
MAXITEM = 20000
# 蚂蚁个数
ANT_NUM = 6
# 城市个数
CITY_NUM = 18
# 路径残余信息度，初始化为1
T = np.ones((CITY_NUM, CITY_NUM))
# 残留信息的重要性
A = 1
# 启发信息(能见度/先验知识)的重要性
B = 1
# 信息素的减弱程度，0-1
C = 0.5
# Ant-Quantity System模型中常量Q大小
Q = 1
# q0,q1将0-1划分三段，分别使用不同的选择策略(赌轮，信息素最大，随机)
q0 = 0.98
q1 = 0.99

'''方法'''


# 加载数据方法,txt文件中间逗号隔开，加载为二维矩阵
def loadData():
    data = np.loadtxt('citys_LOCATION.txt')
    return data


# 处理数据，这里将加载到的城市坐标计算各个之间的距离存储起来
def cityDis(data):
    dis_city = []  # 存储结构为[[list]],使用dis_city[i][j]表示，第i个到第j个城市的距离
    for i in range(len(data)):
        temp_list = []  # 暂存第i个城市1到其他所有城市距离
        for j in range(len(data)):
            # 勾股定理计算距离，第i到第j个城市的距离
            dis = math.sqrt(pow(data[i][0] - data[j][0], 2) + pow(data[i][1] - data[j][1], 2))
            temp_list.append(dis)
        dis_city.append(temp_list)
    return dis_city


# 统计相同路径最多的数目,返回该路径和该路径出现数目,判断算法收敛程度，适时终结算法，返回最优路径下标和出现个数
def maxSameWayNum(allway_list):
    count_list = []
    num_list = []
    for items in allway_list:
        if items not in count_list:
            count_list.append(items)
            num_list.append(1)
        else:
            num_list[count_list.index(items)] += 1
    max_num = max(num_list)
    best_way_sub = num_list.index(max_num)
    return best_way_sub, max_num


# 此方法按照不同的使用环境计算，此时计算的是路径总长度
# 计算路径长度,listPath为蚂蚁路径，dis_city为距离矩阵
def path_dis(listPath, dis_city):
    # 开始
    start = listPath[0]
    dis = 0
    for i in range(1, len(listPath)):
        dis = dis + dis_city[listPath[i - 1]][listPath[i]]
    dis = dis + dis_city[listPath[len(listPath) - 1]][start]
    return dis


'''类'''


# 蚂蚁类
class Ant:
    def __init__(self, now_position, data_length):
        self.now_position = now_position  # 蚂蚁当前位置下标
        self.passed_list = []  # 已经走过的位置下标
        self.allowed_list = []  # 还未走过的位置下标
        for i in range(data_length):
            self.allowed_list.append(i)


'''主方法'''


def main_aco():
    # 加载数据
    data = loadData()
    # 处理数据（计算距离）
    dis_city = cityDis(data)
    # 最优路径
    best_way = []
    # 最优路径长度
    best_way_length = -1

    # 画图类
    draw = way_plt.DrawWay(data)

    # 主循环
    item = 0
    while item < MAXITEM:
        global q0, q1
        print('第', str(item + 1), '次循环')
        if item >= 10000:
            q0 = 0.8
            q1 = 0.81
        # 存储本次循环每只蚂蚁所走的路经
        allway_list = []
        # 让每个蚂蚁走一遍
        for i in range(ANT_NUM):
            # 随机分配该蚂蚁起始位置下标
            now_position = random.randint(0, len(data) - 1)
            # 实例化Ant类
            ant = Ant(now_position, len(data))
            # 将当前位置下标加入走过的路列表中
            ant.passed_list.append(now_position)
            # 将当前位置从未走过的路中删除（pop是使用下标，remove使用元素对比）
            ant.allowed_list.remove(now_position)
            # 循环走完剩下所有城市（选择路径=====此处有改进，使用三种选择策略）
            while len(ant.allowed_list) > 0:
                # 当前城市
                ant.now_position = ant.passed_list[len(ant.passed_list) - 1]
                # 生成随机数q，决定使用哪一种生成策略
                q = random.uniform(0, 1)
                # 第一种选择策略,随机选择
                if q > q1:
                    rand_sub = random.randint(0, len(ant.allowed_list) - 1)  # 生成随机下标
                    # 下一个选择的城市
                    rand_city = ant.allowed_list[rand_sub]
                    # 将该城市加入已选，并从未选中剔除
                    ant.passed_list.append(rand_city)
                    ant.allowed_list.pop(rand_sub)
                    # 局部更新信息素
                    # 与该城市相连信息素最低的信息素量
                    min_t = 100
                    for k in ant.allowed_list:
                        temp_t = T[ant.now_position, k]
                        if temp_t < min_t:
                            min_t = temp_t
                    T[ant.now_position][rand_sub] = (1 - C) * T[ant.now_position][rand_sub] + C * min_t
                # 第二种选择策略,信息素最大的一条
                elif q > q0 and q <= q1:
                    # max_city记录剩下的的城市中到达本城市信息素最大的城市和信息素
                    max_city = ant.allowed_list[0]
                    max_t = 0
                    min_t = 100
                    # 遍历查找最大信息素城市
                    for k in ant.allowed_list:
                        # 当前城市到下标为k的城市之间的残留信息度
                        temp_t = T[ant.now_position, k]
                        if temp_t > max_t:
                            max_t = temp_t
                            max_city = k
                        if temp_t < min_t:
                            min_t = temp_t
                    # 将该城市加入已选，并从未选中剔除
                    ant.passed_list.append(max_city)
                    ant.allowed_list.remove(max_city)
                    # 局部更新信息素
                    T[ant.now_position][max_city] = (1 - C) * T[ant.now_position][max_city] + C * min_t
                # 第三种选择策略,赌轮法
                else:
                    '''公式计算下面选择每个城市的概率'''
                    # 分母(总乘积)
                    pro = 0
                    # 遍历从now_position出发可以到达的其他所有城市
                    for j in ant.allowed_list:
                        # 当前城市到下标为j的城市之间的残留信息度
                        now_T = T[ant.now_position, j]
                        # 当前城市到第j城市的先验知识H（能见度）
                        now_longth = dis_city[now_position][j]
                        H = 1 / now_longth
                        # 计算总乘积
                        pro = pro + math.pow(now_T, A) * math.pow(H, B)
                    # 计算概率
                    nowToj_p_list = []
                    for j in ant.allowed_list:
                        # 当前城市到下标为j的城市之间的残留信息度
                        now_T = T[now_position, j]
                        # 当前城市到第j城市的先验知识H（能见度）
                        now_longth = dis_city[now_position][j]
                        H = 1 / now_longth
                        # 概率
                        p = math.pow(now_T, A) * math.pow(H, B) / pro
                        nowToj_p_list.append(p)
                    '''选择下一个位置，轮赌法选择，与概率大小和排列顺序有关'''
                    # 生成随机数
                    rand = random.uniform(0, max(nowToj_p_list))
                    for j in range(len(ant.allowed_list)):
                        if (rand - nowToj_p_list[j]) <= 0:
                            # 下一个城市下标
                            nextCity = ant.allowed_list[j]
                            # 将该城市加入已选，并从未选中剔除
                            ant.passed_list.append(nextCity)
                            ant.allowed_list.pop(j)
                            # 局部更新信息素
                            # 与该城市相连信息素最低的信息素量
                            min_t = 100
                            for k in ant.allowed_list:
                                temp_t = T[ant.now_position, k]
                                if temp_t < min_t:
                                    min_t = temp_t
                            T[ant.now_position][nextCity] = (1 - C) * T[ant.now_position][nextCity] + C * min_t
                            break
            '''更新信息素'''
            # dT = Q / path_dis(ant.passed_list, dis_city)
            #  距离越小信息素增量dT越大，选择概率越高
            dT = Q * math.exp(-math.sqrt(path_dis(ant.passed_list, dis_city) / (18 * 37)))
            # print(str(ant.passed_list),':',str(dT))
            for m in range(len(ant.passed_list) - 1):
                firstCity_sub = ant.passed_list[m]
                secondCity_sub = ant.passed_list[m + 1]
                T[firstCity_sub][secondCity_sub] = (1 - C) * T[firstCity_sub][secondCity_sub] + dT
            firstCity_sub = ant.passed_list[len(ant.passed_list) - 1]
            secondCity_sub = ant.passed_list[0]
            # 找到该信息素,并更新
            u = math.exp(-item / 20)
            T[firstCity_sub][secondCity_sub] = u * (1 - C) * T[firstCity_sub][secondCity_sub] + dT
            # print('信息素：',str(T))
            allway_list.append(ant.passed_list)
        # 找到当前路径中最优路径下标和出现次数
        # print(allway_list)
        best_way_sub, count = maxSameWayNum(allway_list)
        # 计算当前最优路径长度
        length = path_dis(allway_list[best_way_sub], dis_city)
        # 若新出现的路径更小，更新
        if best_way_length > length or best_way_length == -1:
            # 最优路径
            best_way = allway_list[best_way_sub]
            best_way_length = length
            # 绘制图像
            draw.update(best_way, length)
        # 若一次循环中同样的路径出现次数超过90%，则证明比较收敛，可以结束算法。但是如果只依靠收敛判断的话，在数据量很少的情况下很容易出错，所以用了上面补充
        if count / len(allway_list) >= 0.9:
            break
        item += 1
    print('最优路径：', str(best_way), ' 路径长度为：', str(best_way_length))
    # 画出路线
    draw.drawFinal(best_way, best_way_length)


main_aco()
