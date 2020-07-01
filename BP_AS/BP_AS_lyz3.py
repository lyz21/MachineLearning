# encoding=utf-8
"""
@Time : 2020/2/8 15:57 
@Author : LiuYanZhe
@File : BP_AS_lyz3.py 
@Software: PyCharm
@Description: 只运行未改进与改进后的主方法，准备论文
"""
from BP_AS import BP_lyz
from BP_AS import BP0
from BP_AS import BP_0_lyz
import time
import numpy as np
from BP_AS import ROC
from BP_AS import Matrix
from BP_AS import Utils


# 将3维表示朝代转化为1维，例[0,0,1]-->2
def del_res(list0):
    res_list = []
    for temp_list in list0:
        index = temp_list.index(max(temp_list))
        res_list.append(index)
    return res_list


maxIter = 450
learnRate = 0.4

stratTime = time.time()
print('未改进：')
list_rate, list_count, list_all_count, list_pre, y_list, list_E1 = BP0.main(max_iter=maxIter,
                                                                            learnRate=learnRate)
res_pre_list = del_res(list_pre)
res_y_list = del_res(y_list)
Matrix.main_lyz(res_y_list, res_pre_list, 'Confusion matrix - Unimproved model')
ROC.main_lyz(list_pre, y_list, 'Unimproved model - ROC')
# print('未改进时间', time.time() - stratTime)

print('-----------------')
output_threshold_list = np.loadtxt('ant_output_threshold_list.txt')
hidden_threshold_list = np.loadtxt('ant_hidden_threshold_list.txt')
outhid_weight = np.loadtxt('ant_outhid_weight.txt')
inHid_weight = np.loadtxt('ant_inHid_weight.txt')
print('蚁群+学习率+权值算法改进：')
BP_startTime = time.time()
list_rate, list_count, list_all_count, list_pre, y_list, list_E2, list_learnRate = BP_lyz.main_par(
    output_threshold_list,
    hidden_threshold_list,
    outhid_weight,
    inHid_weight, learnRate=learnRate,
    max_iter=maxIter)
res_pre_list = del_res(list_pre)
res_y_list = del_res(y_list)
Matrix.main_lyz(res_y_list, res_pre_list, 'Confusion matrix - Improved model')
ROC.main_lyz(list_pre, y_list, 'Improved model - ROC')
BP_endTime = time.time()
print('蚁群+学习率+权值算法运行时间：', BP_endTime - BP_startTime)
print('-----------------')
print('算法总运行时间：', BP_endTime - stratTime)

x = list(range(1, maxIter + 1))
Utils.draw1Line(x, list_E1, 'Unimproved curve', 'Times-E1')
Utils.draw1Line(x, list_E2, 'Improved curve', 'Times-E2')
x = list(range(1, len(list_learnRate)+1))
Utils.draw1Line(x, list_learnRate, 'learnRate curve', 'learnRate curve')
print('结束')
