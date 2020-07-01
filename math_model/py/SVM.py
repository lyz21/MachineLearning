# encoding=utf-8
"""
@Time : 2020/6/19 18:04
@Author : LiuYanZhe
@File : SVM.py
@Software: PyCharm
@Description:
"""
# 构建出了一个SVM的分类模型，并进行了拟合
from sklearn import svm
from math_model.util import dataUtil
from math_model.util import picutil
import pandas as pd

data0 = dataUtil.load_data('../data/data_22.csv')
# data0 = dataUtil.load_data('../data/data.csv')
# data0 = data0.drop(['wzqdcsd', 'wzqdcsC', 'wzqdcsA'], axis=1)
data0 = data0.iloc[:, 1:]
# 标准化
data = dataUtil.standardization(data0)
print('*' * 10, 'data(标准化之后)')
print(data.head(10))
# 划分x,y
x, y = dataUtil.get_x_y(data)
print('*' * 10, 'x')
print(x)
print('*' * 10, 'y')
print(y)
# 划分训练集测试集
x_train, x_test, y_train, y_test = dataUtil.k_fold(x, y)
print('*' * 10, 'x_train')
print(x_train)
print('*' * 10, 'x_test')
print(x_test)
print('*' * 10, 'y_train')
print(y_train)
print('*' * 10, 'y_test')
print(y_test)
# print(x_train.shape)
# print(x_test.shape)
# SVM拟合
clf = svm.SVC()
clf.fit(list(x_train), list(y_train))
# SVM预测
y_pre = clf.predict(x_test)
print('*' * 10, 'y_pre')
print(y_pre)
print('*' * 10, 'y_test')
print(y_test)
# 计算准确率
acc = dataUtil.get_acc(y_pre, y_test)
print('*' * 10, 'acc')
print('acc:', acc)
# 模型评估,混淆矩阵
picutil.draw_matrix(y_pre, y_test)
# ROC
fpr, tpr, auc = dataUtil.get_ROC_AUC(y_test, y_pre)
picutil.draw_AOC_AUC(fpr, tpr, auc)
# PR
precision, recall, auc = dataUtil.get_PR_AUC(y_test, y_pre)
