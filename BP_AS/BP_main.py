# encoding=utf-8
"""
Name:         BP_main
Description:  
Author:       LiuYanZhe
Date:         2019/12/4
"""
from BP_AS import BP_lyz
from BP_AS import BP0
from BP_AS import BP_0_lyz
import numpy as np
# output_threshold_list = np.loadtxt('output_threshold_list.txt')
# hidden_threshold_list = np.loadtxt('hidden_threshold_list.txt')
# outhid_weight = np.loadtxt('outhid_weight.txt')
# inHid_weight = np.loadtxt('inHid_weight.txt')
# BP_lyz.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight, max_iter=10)
print('无改进')
BP0.main(max_iter=1000,learnRate=0.1)
print('动态更改学习率')
BP_0_lyz.main(max_iter=1000,learnRate=0.1)
print('修改权值+动态学习率')
BP_lyz.main(max_iter=1000,learnRate=0.1)
# list=[[1,0,0],[0,0,1],[0,1,0]]
# list1=BP_lyz.normalDY(list,1,0)
# print('归一化后：',list1)
# list1=BP_lyz.normalX(list,1,0)
# print('归一化后：',list1)
# list2=BP_lyz.normalDY_F(list1,1,0)
# print('反归一化后：',list2)
