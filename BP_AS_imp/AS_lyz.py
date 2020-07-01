# encoding=utf-8
"""
Name:         AS_lyz
Description:  使用蚁群算法优化神经网络
Author:       LiuYanZhe
Date:         2019/12/1
"""
import logging
import numpy as np
import random
import math
from BP_AS_imp import BP

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志
# logging.disable()

'''全局变量'''
# 最大循环次数
# MAXITEM = 50
# 蚂蚁个数
ANT_NUM = 817
# 结点个数   # 权值数+阈值数      (18*37+37*3)+(37+3)
NODE_NUM = 817
# 每两个结点间路径数（权值、阈值取值划分个数）
DIVIDE = 10
# 每条路线上的残余信息素
T_LIST = np.ones((NODE_NUM, DIVIDE)).tolist()
# 残留信息的重要性
A = 1
# 启发信息(能见度/先验知识)的重要性
B = 1
# 信息素的减弱程度，0-1
C = 0.5
# ACS/AQS/ADS模型中常量Q大小
Q = 1
# q0,q1将0-1划分三段，分别使用不同的选择策略
q0 = 0.4
q1 = 0.8
# BP神经网络相关
# 各层节点数
INPUT_NUM = 18
HIDDEN_NUM = 37
OUTPUT_NUM = 3
M = 18
N = 37
# 存储最优E
best_E = 1
# 存储最优E
list_bestE = []
# 权值、阈值选择矩阵
wei_thr_choose_list = []
for i in range(DIVIDE + 1):
    wei_thr_choose_list.append(-1 + i * (2 / (DIVIDE)))
# 存储最优权值矩阵
best_inHid_weight = np.ones((INPUT_NUM, HIDDEN_NUM)).tolist()
best_outhid_weight = np.ones((HIDDEN_NUM, OUTPUT_NUM)).tolist()
# 存储最优阈值矩阵
best_hidden_threshold_list = [0.0] * HIDDEN_NUM
best_output_threshold_list = [0.0] * OUTPUT_NUM


# 蚂蚁类
class Ant:
    def __init__(self, start_position):
        self.start_position = start_position  # 记录蚂蚁起始下标
        self.passed_list = []  # 记录蚂蚁走过的路
        self.choose_list = []  # 保存蚂蚁选择的路径


# 主方法
def main_AS(MAXITEM=50, x_list=[], y_list=[]):
    global T_LIST
    # 主循环
    item = 0
    while item < MAXITEM:
        # print('第', str(item), '次循环')
        # 让每个蚂蚁走一遍
        for i in range(ANT_NUM):
            # print('第', str(i + 1), '只蚂蚁')
            # 随机分配该蚂蚁位置(随机分配到某一结点)
            start_position = random.randint(0, NODE_NUM - 1)
            # logging.debug('start_position:'+str(start_position))
            # 实例化该蚂蚁
            ant = Ant(start_position)
            # 记录当前结点下标
            nowposition = start_position
            # 走完剩下的结点（选择路径=====此处有改进，使用三种选择策略）
            for j in range(NODE_NUM):
                # 1 找到从nowposition到nowposition+1的所有路径信息素列表，T_LIST为信息素
                t_list = T_LIST[nowposition]
                # logging.debug('t_list:'+str(t_list))
                # 生成随机数q，决定使用哪一种生成策略
                q = random.uniform(0, 1)
                # 第一种选择策略,随机选择
                if q > q1:
                    rand_sub = random.randint(0, DIVIDE - 1)  # 生成随机下标
                    # 局部更新信息素
                    t_list[rand_sub] = (1 - C) * t_list[rand_sub] + C * min(t_list)
                    # 将该路径加入已选路径中
                    ant.choose_list.append(rand_sub)
                    # 将该结点加入已走节点中
                    ant.passed_list.append(nowposition)
                    # 将结点后移
                    nowposition += 1
                    if nowposition == NODE_NUM:  # 如果节点到最后一个，回到第一个
                        nowposition = 0
                    continue
                # 第二种选择策略,信息素最大的一条
                elif q > q0 and q <= q1:
                    # 选择的路径下标
                    sub = t_list.index(max(t_list))
                    # 局部更新信息素
                    t_list[sub] = (1 - C) * t_list[sub] + C * min(t_list)
                    # 将该路径加入已选路径中
                    ant.choose_list.append(sub)
                    # 将该结点加入已走节点中
                    ant.passed_list.append(nowposition)
                    # 将结点后移
                    nowposition += 1
                    if nowposition == NODE_NUM:  # 如果节点到最后一个，回到第一个
                        nowposition = 0
                    continue
                # 第三种选择策略,赌轮法
                else:
                    # 2 计算选择每条路径的概率
                    # 2.1 分母（DIVIDE条路径的信息素累加和）
                    sum = 0
                    for k in range(DIVIDE):
                        sum = sum + t_list[k]
                    # 2.2 概率
                    p_list = []
                    for k in range(DIVIDE):
                        p = t_list[k] / sum
                        p_list.append(p)
                    # 3 选择路径（轮转法）
                    # 3.1 生成随机数
                    rand = random.uniform(0, max(p_list))  # 用来选择概率
                    k = random.randint(0, DIVIDE - 1)  # 用来选择比较的开始下标
                    # logging.debug('随机数：'+str(rand)+'\n概率分布：'+str(p_list))
                    temp_i = 0  # 记录循环次数
                    while temp_i < DIVIDE:
                        # 3.2 赌轮选择
                        if rand - p_list[k] <= 0:
                            # 局部更新信息素
                            t_list[k] = (1 - C) * t_list[k] + C * min(t_list)
                            # 将该路径加入已选路径中
                            ant.choose_list.append(k)
                            # 将该结点加入已走节点中
                            ant.passed_list.append(nowposition)
                            # 将结点后移
                            nowposition += 1
                            if nowposition == NODE_NUM:  # 如果节点到最后一个，回到第一个
                                nowposition = 0
                            break
                        else:
                            # 本次没选中，下标后移
                            k += 1
                            if k == DIVIDE:
                                k = 0
                            temp_i += 1  # 循环次数+1
            # 更新信息素
            # 0 转换数据
            # 0.1 将选择的路径下标变为真实值         ###转换为真实值是似乎有错，直接转了，没有考虑起始结点不同
            true_list = []
            for sub in ant.choose_list:
                true_list.append(wei_thr_choose_list[sub])
            # 调整选择的顺序----------------------------------------
            true_list_copy = true_list.copy()
            start_sub = start_position
            for j in range(len(true_list)):
                true_list[start_sub] = true_list_copy[j]
                start_sub += 1
                if start_sub == len(true_list):
                    start_sub = 0
            # 0.2 将选择的数据变为阈值列表和权值矩阵
            out_threshold_temp_list = []
            hid_threshold_temp_list = []
            inHid_temp_weight = np.ones((INPUT_NUM, HIDDEN_NUM)).tolist()
            outhid_temp_weight = np.ones((HIDDEN_NUM, OUTPUT_NUM)).tolist()
            for j in range(OUTPUT_NUM + HIDDEN_NUM):
                if j < OUTPUT_NUM:
                    out_threshold_temp_list.append(true_list[j])
                else:
                    hid_threshold_temp_list.append(true_list[j])
            temp = OUTPUT_NUM + HIDDEN_NUM
            for n in range(INPUT_NUM):
                for m in range(HIDDEN_NUM):
                    inHid_temp_weight[n][m] = true_list[temp]
                    temp += 1
            for n in range(HIDDEN_NUM):
                for m in range(OUTPUT_NUM):
                    outhid_temp_weight[n][m] = true_list[temp]
                    temp += 1
            # 0.3 带入神经网络计算全局误差，误差越小越好
            # E = BP_lyz.measure(hid_threshold_temp_list, out_threshold_temp_list, inHid_temp_weight, outhid_temp_weight)
            E = BP.measure(hid_threshold_temp_list, out_threshold_temp_list, inHid_temp_weight, outhid_temp_weight,
                           x_list=x_list, y_list=y_list)
            # 存储最优矩阵
            global best_E, best_hidden_threshold_list, best_output_threshold_list, best_inHid_weight, best_outhid_weight
            if E < best_E:
                # print('信息素：',T_LIST)
                best_E = E
                best_hidden_threshold_list = hid_threshold_temp_list
                best_output_threshold_list = out_threshold_temp_list
                best_inHid_weight = inHid_temp_weight
                best_outhid_weight = outhid_temp_weight
                print('best_output_threshold_list：', best_output_threshold_list)
                # 最优解备份到txt文件中
                np.savetxt('data/AS_lyz-ant_output_threshold_list.txt', best_output_threshold_list)
                np.savetxt('data/AS_lyz-ant_hidden_threshold_list.txt', best_hidden_threshold_list)
                np.savetxt('data/AS_lyz-ant_outhid_weight.txt', best_outhid_weight)
                np.savetxt('data/AS_lyz-ant_inHid_weight.txt', best_inHid_weight)
            # 1 ACS模型更新 信息素增量过大，需要调整！！！！
            #  E为全局误差，误差越小信息素增量dT越大，选择概率越高
            dT = Q * math.exp(-math.sqrt(E / (M * N)))  # E为全局误差，误差越小信息素增量dT越大，选择概率越高
            # print('dT:',dT)
            # 2 全局更新信息素
            # 2.1 遍历走过的路径,即结点下标
            for j in range(len(ant.passed_list)):
                # 找到本次结点下标
                sub = ant.passed_list[j]
                # 找到该结点对应的路径的信息素
                t_list = T_LIST[sub]
                # 找到选择的路径下标
                way_sub = ant.choose_list[j]
                # 找到该信息素,并更新
                u = math.exp(-item / 20)
                t_list[way_sub] = u * (1 - C) * t_list[way_sub] + dT
                # t_list[way_sub]=t_list[way_sub]+dT
                # T_LIST[sub]=t_list    # 不用再回带，会直接更改T_LIST中的值
        if item % 50 == 0:
            print('第', item, '次最优解E:', best_E)
        list_bestE.append(best_E)
        # logging.debug('信息素：' + str(T_LIST))
        np.savetxt('message/AS_lyz-信息素.txt', T_LIST)
        np.savetxt('message/AS_lyz-蚁群算法每次最优_E.txt', list_bestE)
        item += 1
    print('最优解E:', best_E)

    return best_output_threshold_list, best_hidden_threshold_list, best_outhid_weight, best_inHid_weight
# main_AS()
