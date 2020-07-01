# encoding=utf-8
"""
@Time : 2020/6/21 15:11 
@Author : LiuYanZhe
@File : label_s.py 
@Software: PyCharm
@Description: 半监督分类
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, metrics
from sklearn import svm
from sklearn.semi_supervised import LabelSpreading
from math_model.util import dataUtil
import pandas as pd

# 获取数据
data0 = dataUtil.load_data('../data/data.csv')
# 更改标签
data0.loc[(data0['label'] == 0), ['label']] = -1
# 确定为阴性的标签，该为0
num_list = dataUtil.find_92()
data0.loc[data0['number'].isin(num_list), ['label']] = 0
print(data0[data0['number'].isin(num_list)])
print(data0)
# 划分x，y
data0 = data0.iloc[:, 5:]
data_x, data_y = dataUtil.get_x_y(data0)
# 训练数据
# data_y_train = np.copy(data_y)
print('data_y_train:', data_y)
# 模型
clf = LabelSpreading(max_iter=100, kernel='rbf', gamma=0.1)
ls = (clf.fit(data_x, data_y), data_y)
rbf_svc = (svm.SVC(kernel='rbf', gamma=.5).fit(data_x, data_y), data_y)
y_pre = clf.predict(data_x)

print('预测:', y_pre)
np.savetxt('pre.txt', y_pre)
# print('真实:', y_test)
# print('正确个数：', len((y_pre == y_test)))
# h = 0.02
# x_min, x_max = data_x[:, 0].min() - 1, data_x[:, 0].max() + 1
# y_min, y_max = data_x[:, 1].min() - 1, data_x[:, 1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
#                      np.arange(y_min, y_max, h))
# for i, (clf, y_train) in enumerate((ls, rbf_svc)):
#     # Plot the decision boundary. For that, we will assign a color to each
#     # point in the mesh [x_min, x_max]x[y_min, y_max].
#     plt.subplot(2, 2, i + 1)
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#     print(Z)
# print('预测标签ls：', ls)  #
# print('预测标签rbf_svc[1]：', rbf_svc[1])  #
# print('实际标签data_y:', data_y)  #
# index = (rbf_svc[1] == data_y)
# print('正确个数：', len(index))
# clf = LabelSpreading(max_iter=100, kernel='rbf', gamma=0.1)
# clf.fit(data_x, data_y_train)
# ### 获取预测准确率
# data_y = pd.array(data_y)
# p_y = data_y[data_y['label'] == 0]
# predicted_labels = clf.transduction_[p_y]  # 预测标记
# print("Accuracy:%f" % metrics.accuracy_score(predicted_labels))
