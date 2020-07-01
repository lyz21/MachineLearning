# encoding=utf-8
"""
@Time : 2020/6/20 16:18 
@Author : LiuYanZhe
@File : BP.py 
@Software: PyCharm
@Description: 用自己的BP神经网络
"""
from math_model.py import BP_source
from math_model.util import dataUtil

data0 = dataUtil.load_data('../data/data.csv')
# data0 = data0.drop(['wzqdcsd', 'wzqdcsC', 'wzqdcsA'], axis=1)
# 标准化
data = dataUtil.standardization(data0)
print('data:', data.head(10))
# 划分x,y
x, y = dataUtil.get_x_y(data)
print('x:', x)
# 划分训练集测试集
x_train, x_test, y_train, y_test = dataUtil.k_fold(x, y)

BP_source.main(x_train, y_train, x_test, y_test, input_num=len(x_train[0]), hidden_num=len(x_train[0]) * 2 + 1,
               output_num=1, max_iter=100)
