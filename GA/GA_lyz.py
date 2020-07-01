# encoding=utf-8
"""
Name:         GA_lyz
Author:       LiuYanZhe
Date:         2019/11/28
Description:  遗传算法  以寻找最优城市路线为例
                编码：自然数编码
                适应度函数:线性变换/对数变化/指数变换
                选择策略：正比选择-轮盘法
                交叉：双点交叉+顺序交叉
                变异：个体内部交换两个基因
"""
import random
import math
import numpy as np
import logging
from GA import way_plt

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# 禁用日志
logging.disable()

# 城市数
N = 17


# 加载数据方法,txt文件中间逗号隔开，加载为二维矩阵
def loadData():
    data = np.loadtxt('citys_LOCATION.txt')
    return data


# 路径问题相关方法——计算城市间距离，这里将加载到的城市坐标计算各个之间的距离存储起来
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


# 路径问题相关方法——计算路径长度函数,参数列表：individual_list为路径，dis_city为距离矩阵
def pathlength(individual_list, dis_city):
    # 开始
    start = individual_list[0]
    dis = 0
    for i in range(1, len(individual_list)):
        dis = dis + dis_city[individual_list[i - 1]][individual_list[i]]
    dis = dis + dis_city[individual_list[len(individual_list) - 1]][start]
    return dis


# 选择最优解
def getBestPath(population_list, citydis_list):
    objectfun_list = objectfun(population_list, citydis_list)
    bestPathobj = max(objectfun_list)
    sub = objectfun_list.index(bestPathobj)
    bestPath = population_list[sub]
    bestPathLength = pathlength(bestPath, citydis_list)
    return bestPath, bestPathLength


# 遗传算法方法——编码。编码方式：自然数编码   参数列表：基因个数，生成个体（染色体）个数
def encoding(gene_num, individual_num):
    # 存储初始种群  存储方式 [ [初始个体],[初始个体],[初始个体]... ]
    population_list = []
    # 生成基因候选列表
    temp_list = []
    for i in range(gene_num):
        temp_list.append(i)
    for i in range(individual_num):
        # 选择基因生成初始个体编码
        individual_list = []
        temp_temp_list = temp_list.copy()  # 不能直接list2=list1，改变list2会影响list1
        while True:
            end = len(temp_temp_list) - 1
            sub = random.randint(0, end)
            individual_list.append(temp_temp_list[sub])
            temp_temp_list.pop(sub)  # list.remove()参数为元素而不是索引；list.pop()根据下标删除；del(list[i])根据索引删除
            if len(temp_temp_list) <= 1:
                individual_list.append(temp_temp_list[0])
                break
        # 生成的第i个体存储到种群中
        population_list.append(individual_list)
    return population_list


# 遗传算法方法——目标函数（与求解的优化问题相关，这里是找距离最小值）;参数列表：population_list种群集合,citydis_list为城市距离
def objectfun(population_list, citydis_list):
    # 记录目标函数值,对应于population_list
    objectfun_list = []
    for i in range(len(population_list)):
        individual_list = population_list[i]
        # 获取路径长度,取倒数，则路径越短f越大选择概率越大
        length = 1 / pathlength(individual_list, citydis_list)
        objectfun_list.append(length)
    return objectfun_list


# 遗传算法方法——适应度函数（四种，这里有线性变换/对数变化/指数变换）    参数列表：objectfun_list 目标函数计算结果
def fitnessfun(objectfun_list):
    a = 2
    b = 5
    k = 2
    fitnessfun_list = []
    for i in range(len(objectfun_list)):
        # 线性变换
        # F = math.pow(a, k) * objectfun_list[i] + math.pow(b, k)  # math.pow(a，b) a的b次方
        # 对数变化（扩大目标函数差别）
        F = a * math.pow(math.e, b * objectfun_list[i]) + k
        # 对数变换（缩小目标函数差值）
        # F = a * math.log(objectfun_list[i]) + b  # log(a,b) 以b为底的a的对数，默认为e
        fitnessfun_list.append(F)
    return fitnessfun_list

# 遗传算法方法——选择策略（这里用轮赌法，越小的选择概率越大）  参数列表：selectnum 选择数目 , population_list 种群集合,fitnessfun_list 适应度函数集合
def selectfun(selectrate, population_list, fitnessfun_list):
    # 根据选择率计算本次选择个数
    selectnum = math.ceil(len(population_list) * selectrate)
    # 存储新选择的个体
    population_new_list = []
    # 存储概率
    proability_list = []
    # 计算概率
    sum = 0
    for i in range(len(fitnessfun_list)):
        sum += fitnessfun_list[i]
    for fitnessfun in fitnessfun_list:
        proability = fitnessfun / sum * 1000  # 概率乘以1000，扩大概率差距，方便选择
        proability_list.append(proability)
    logging.debug('种群：' + str(population_list))
    logging.debug('概率：' + str(proability_list))

    # 轮赌法选择selectnum个子代个体,因为轮赌法与顺序有关，因此从两个方向选择。每次选择后去掉该选择的个体，避免重复选择同一个体
    temp_proability_list = proability_list.copy()
    temp_population_list = population_list.copy()
    k = 1  # 控制选择方向
    while len(population_new_list) < selectnum:
        # 随机生成一个实数
        rand = random.uniform(min(temp_proability_list), max(temp_proability_list))
        logging.debug('随机数：' + str(rand))
        if k == 1:
            for j in range(len(temp_population_list)):
                if rand - temp_proability_list[j] <= 0:  # 随机数比概率小就选择，即概率越大，选择几率越大
                    population_new_list.append(temp_population_list[j])
                    temp_proability_list.pop(j)  # 每选择一个便弹出，防止重复选择
                    temp_population_list.pop(j)
                    k = 0
                    break
        if k == 0:
            for j in range(len(temp_population_list) - 1, -1, -1):
                if rand - temp_proability_list[j] <= 0:  # 随机数比概率小就选择，即概率越大，选择几率越大
                    population_new_list.append(temp_population_list[j])
                    temp_proability_list.pop(j)
                    temp_population_list.pop(j)
                    k = 1
                    break
    return population_new_list

# 遗传算法方法——交叉（精髓）（此处为双点交叉）    参数列表：crorate交叉概率，population_list 种群
# def crossover(crorate, population_list):
#     # 交叉个数(向上取整)
#     cronum = math.ceil(len(population_list) * crorate)
#     for i in range(cronum):
#         # 随机选择两个父代个体
#         while True:
#             individual1 = random.randint(0, len(population_list)-1)
#             individual2 = random.randint(0, len(population_list)-1)
#             if individual1 != individual2:
#                 break
#         # 随机生成两个交叉点
#         while True:
#             point1 = random.randint(0, len(population_list[0])-1)
#             point2 = random.randint(0, len(population_list[0])-1)
#             if point1 > point2:
#                 temp = point1
#                 point1 = point2
#                 point2 = temp
#             if point1!=point2:
#                 break
#         # 交叉
#         list1=population_list[individual1]
#         list2=population_list[individual2]
#         print('交叉前',population_list)
#         temp_list=list1.copy()
#         for j in range(point1,point2):
#             list1[j]=list2[j]
#             list2[j]=temp_list[j]
#         population_list[individual1]=list1
#         population_list[individual2]=list2
#         print('交叉后',population_list)
#     return population_list
# 遗传算法方法——交叉（精髓）（此处为顺序交叉）    参数列表：crorate交叉概率，population_list 种群
def crossover(crorate, population_list):
    # 交叉个数(向上取整)
    cronum = math.ceil(len(population_list) * crorate)
    for i in range(cronum):
        # 随机选择两个父代个体
        while True:
            individual1 = random.randint(0, len(population_list) - 1)
            individual2 = random.randint(0, len(population_list) - 1)
            if individual1 != individual2:
                break
        # 随机生成两个交叉点
        while True:
            point1 = random.randint(0, len(population_list[0]) - 1)
            point2 = random.randint(0, len(population_list[0]) - 1)
            if point1 > point2:
                temp = point1
                point1 = point2
                point2 = temp
            if point2 - point1 >= 2:  # 至少交换两个
                break
        logging.debug('交叉前' + str(population_list))
        # 两个交叉个体
        list1 = population_list[individual1]
        list2 = population_list[individual2]
        logging.debug('交叉前list1' + str(list1))
        logging.debug('交叉前list2' + str(list2))
        logging.debug('交叉点' + str(point1) + '--' + str(point2))
        # 暂存两个交叉域中的内容
        t1_list = []
        t2_list = []
        for j in range(point1, point2):
            t1_list.append(list1[j])
            t2_list.append(list2[j])
        # 置空要交换的基因位置
        for j in range(len(list1)):
            if list1[j] in t2_list:
                list1[j] = -1
            if list2[j] in t1_list:
                list2[j] = -1
        # logging.debug('交叉基因1'+str(t1_list))
        # logging.debug('交叉基因2'+str(t2_list))
        # 交叉操作
        sub1 = 0
        sub2 = 0
        for j in range(len(list1)):
            if list1[j] == -1:
                list1[j] = t2_list[sub1]
                sub1 += 1
            if list2[j] == -1:
                list2[j] = t1_list[sub2]
                sub2 += 1
        population_list[individual1] = list1
        population_list[individual2] = list2
        logging.debug('交叉后' + str(population_list))
        logging.debug('交叉后list1' + str(list1))
        logging.debug('交叉后list2' + str(list2))
        logging.debug('---')
    return population_list


# 遗传算法方法——变异（精髓） 参数列表：mutrat 变异率,population_list 种群
def mutation(mutrate, population_list):
    logging.debug('变异前：' + str(population_list))
    # 变异个数(向上取整)
    mutnum = math.ceil(len(population_list) * mutrate)
    for i in range(mutnum):
        # 随机选择1个父代个体
        individual_sub = random.randint(0, len(population_list) - 1)
        individual = population_list[individual_sub]
        logging.debug('变异前：' + str(individual))
        # 随机生成两个交换点
        while True:
            point1 = random.randint(0, len(population_list[0]) - 1)
            point2 = random.randint(0, len(population_list[0]) - 1)
            if point2 != point1:
                break
        temp = individual[point1]
        individual[point1] = individual[point2]
        individual[point2] = temp
        population_list[individual_sub] = individual
        logging.debug('变异点：' + str(point1) + ',' + str(point2))
        logging.debug('变异后：' + str(population_list))
        logging.debug('变异后：' + str(individual))
        logging.debug('---')
    return population_list


# 主方法
def GA_main(maxIteraNum):
    # 获得初始种群    参数列表：（城市数，初始种群的个体数）
    population_list = encoding(N, 500)
    # 获取城市坐标数据
    data = loadData()
    # 绘图类
    draw = way_plt.DrawWay(data)
    # 计算城市距离
    citydis_list = cityDis(data)
    for i in range(maxIteraNum):
        # 通过目标函数计算      参数列表：（种群集合，城市距离矩阵） 返回值：目标函数计算结果
        objectfun_list = objectfun(population_list, citydis_list)
        # 使用适应度函数计算     参数列表：（目标函数计算结果）    返回值：适应度函数计算结果
        fitnessfun_list = fitnessfun(objectfun_list)
        # 选择下一代个体,每10次减少0.01数量       参数列表：（选择率，种群集合，适应度函数计算结果）
        if i % 10 == 0:
            population_list = selectfun(0.99, population_list, fitnessfun_list)
        else:
            population_list = selectfun(1, population_list, fitnessfun_list)
        # 交叉                参数列表：（交叉率，种群列表）
        population_list = crossover(0.6, population_list)
        # 变异                参数列表：（变异率，种群列表）
        population_list = mutation(0.2, population_list)
        print(population_list)
        if i % 10 == 0:
            print('第', i, '次循环', population_list)
            # 当前最优路径
            bestPath, length = getBestPath(population_list, citydis_list)
            draw.update(bestPath)
    # 获得最优路径
    bestPath, length = getBestPath(population_list, citydis_list)
    print('最优路径：', bestPath, ' ', '长度：', length)
    # 画出图像
    draw.drawFinal(bestPath)
    return bestPath, length


bestPath, length = GA_main(200)
