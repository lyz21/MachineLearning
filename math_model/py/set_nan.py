# encoding=utf-8
"""
@Time : 2020/6/21 21:34 
@Author : LiuYanZhe
@File : set_nan.py 
@Software: PyCharm
@Description: 填充缺失值
"""
from sklearn.linear_model import Ridge,Lasso
from math_model.util import dataUtil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取数据
data0 = dataUtil.load_data('../data/data_nan.csv')
data_nan, data_no_nan, y_train = dataUtil.get_nan_nonan(data0)
# 划分数据
x_train = data_no_nan.iloc[:, 6: data_no_nan.shape[1] - 1]
x_pre = data_nan.iloc[:, 6: data_no_nan.shape[1] - 1]
print(x_train)
print(x_pre)
print(y_train)
# clf = Ridge(alpha=.5)
clf = Ridge()
clf.fit(x_train, y_train)
print(clf.coef_)  # 相关系数
print(clf.intercept_)  # 截距
y_pre = clf.predict(x_pre)
print('*' * 10, 'pre')
print(y_pre)
data_nan_copy = data_nan.copy()
data_nan_copy.loc[:, 'cql'] = y_pre
# 合并
dataUtil.mer_t_pd(data_no_nan, data_nan_copy)
