# encoding=utf-8
"""
@Time : 2020/2/7 16:46 
@Author : LiuYanZhe
@File : BP_AS_lyz2.py 
@Software: PyCharm
@Description: 网格找最优解
"""
from BP_AS import AS_lyz
from BP_AS import BP_lyz
from BP_AS import BP0
from BP_AS import BP_0_lyz
import time
import numpy as np

iter_list = [500, 1000, 1500]
learnRate_list = [0.001, 0.01, 0.1, 0.5]

best1 = {'name': '未改进', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}
best2 = {'name': '动态调整学习率', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}
best3 = {'name': '修改权值+动态学习率', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}
best4 = {'name': '蚁群算法改进神经网络', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}
best5 = {'name': '蚁群+学习率+权值算法改进', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}

for maxIter in iter_list:
    for learn_rate in learnRate_list:
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('maxIter:', maxIter, ';', 'learn_rate:', learn_rate)
        stratTime = time.time()
        print('未改进：')
        rightRate = BP0.main(max_iter=maxIter, learnRate=learn_rate)
        if rightRate > best1['rightrate']:
            best1['rightrate'] = rightRate
            best1['maxIter']=maxIter
            best1['learn_rate']=learn_rate
        print('未改进时间', time.time() - stratTime)

        print('-----------------')

        print('动态调整学习率：')
        bpTime = time.time()
        rightRate = BP_0_lyz.main(max_iter=maxIter, learnRate=learn_rate)
        if rightRate > best2['rightrate']:
            best2['rightrate'] = rightRate
            best2['maxIter']=maxIter
            best2['learn_rate']=learn_rate
        print('动态调整学习率运行时间：', time.time() - bpTime)

        print('-----------------')
        print('修改权值+动态学习率')
        rightRate = BP_lyz.main(max_iter=maxIter, learnRate=learn_rate)
        if rightRate > best3['rightrate']:
            best3['rightrate'] = rightRate
            best3['maxIter']=maxIter
            best3['learn_rate']=learn_rate
        # print('-----------------')
        # print('蚁群算法：')
        # ant_startTime = time.time()
        # 蚁群算法
        # output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight = AS_lyz.main_AS(MAXITEM=30)
        # print('蚁群算法运行时间：', time.time() - ant_startTime)
        print('-----------------')
        # # # BP神经网络
        output_threshold_list = np.loadtxt('ant_output_threshold_list.txt')
        hidden_threshold_list = np.loadtxt('ant_hidden_threshold_list.txt')
        outhid_weight = np.loadtxt('ant_outhid_weight.txt')
        inHid_weight = np.loadtxt('ant_inHid_weight.txt')
        print('蚁群算法改进神经网络：')
        print('output_threshold_list:', output_threshold_list)
        BP_startTime = time.time()
        rightRate=BP0.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight, learnRate=learn_rate,
                     max_iter=maxIter)
        if rightRate > best4['rightrate']:
            best4['rightrate'] = rightRate
            best4['maxIter']=maxIter
            best4['learn_rate']=learn_rate
        BP_endTime = time.time()

        print('蚁群算法改进运行时间：', BP_endTime - BP_startTime)

        print('-----------------')

        output_threshold_list = np.loadtxt('ant_output_threshold_list.txt')
        hidden_threshold_list = np.loadtxt('ant_hidden_threshold_list.txt')
        outhid_weight = np.loadtxt('ant_outhid_weight.txt')
        inHid_weight = np.loadtxt('ant_inHid_weight.txt')
        print('蚁群+学习率+权值算法改进：')
        BP_startTime = time.time()
        rightRate=BP_lyz.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight, learnRate=learn_rate,
                        max_iter=maxIter)
        if rightRate > best5['rightrate']:
            best5['rightrate'] = rightRate
            best5['maxIter']=maxIter
            best5['learn_rate']=learn_rate
        BP_endTime = time.time()
        print('蚁群+学习率+权值算法运行时间：', BP_endTime - BP_startTime)

        print('-----------------')
        print('算法总运行时间：', BP_endTime - stratTime)
print(best1)
print(best2)
print(best3)
print(best4)
print(best5)
