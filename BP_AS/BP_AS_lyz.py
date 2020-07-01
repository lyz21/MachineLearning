# encoding=utf-8
"""
Name:         BP_AS_lyz
Description:  算法入口
Author:       LiuYanZhe
Date:         2019/12/2
"""
from BP_AS import AS_lyz
from BP_AS import BP_lyz
from BP_AS import BP0
from BP_AS import BP_0_lyz
import time
import numpy as np

stratTime = time.time()
print('未改进：')
BP0.main(max_iter=1000,learnRate=0.1)
print('未改进时间', time.time() - stratTime)
print('-----------------')
print('动态调整学习率：')
bpTime = time.time()
BP_0_lyz.main(max_iter=1000,learnRate=0.1)
print('动态调整学习率运行时间：', time.time() - bpTime)
print('-----------------')
print('修改权值+动态学习率')
BP_lyz.main(max_iter=1000,learnRate=0.1)
print('修改权值+动态学习率')
print('-----------------')
print('蚁群算法：')
ant_startTime = time.time()
# 蚁群算法
# output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight = AS_lyz.main_AS(MAXITEM=30)
print('蚁群算法运行时间：', time.time() - ant_startTime)
print('-----------------')

output_threshold_list = np.loadtxt('ant_output_threshold_list.txt')
hidden_threshold_list = np.loadtxt('ant_hidden_threshold_list.txt')
outhid_weight = np.loadtxt('ant_outhid_weight.txt')
inHid_weight = np.loadtxt('ant_inHid_weight.txt')
# # # BP神经网络
print('蚁群算法改进神经网络：')
print('output_threshold_list:',output_threshold_list)
BP_startTime = time.time()
BP0.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight,learnRate=0.1, max_iter=1300)
BP_endTime = time.time()
print('蚁群算法改进运行时间：', BP_endTime - BP_startTime)
# print('-----------------')

output_threshold_list = np.loadtxt('ant_output_threshold_list.txt')
hidden_threshold_list = np.loadtxt('ant_hidden_threshold_list.txt')
outhid_weight = np.loadtxt('ant_outhid_weight.txt')
inHid_weight = np.loadtxt('ant_inHid_weight.txt')

print('蚁群+学习率+权值算法改进：')
BP_startTime = time.time()
BP_lyz.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight,learnRate=0.1, max_iter=1300)
BP_endTime = time.time()
print('蚁群+学习率+权值算法运行时间：', BP_endTime - BP_startTime)
print('-----------------')
print('算法总运行时间：', BP_endTime - stratTime)
