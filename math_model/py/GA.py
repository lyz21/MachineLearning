# encoding=utf-8
"""
@Time : 2020/6/20 15:35 
@Author : LiuYanZhe
@File : GA.py 
@Software: PyCharm
@Description: 使用遗传算法优化神经网络
"""
import matplotlib.pyplot as plt
from sko.GA import GA
from math_model.py import ANN
import numpy as np
import pandas as pd
from math_model.util import dataUtil

data = dataUtil.load_data('../data/data_22.csv')
print('data shape:', data.shape)
# data = data.iloc[:, 2:]
# 标准化
# data = dataUtil.standardization(data)
input_num = 14
# 划分x,y
x, y = dataUtil.get_x_y(data)
print('x:', x.shape)
print('y:', y.shape)
# 正则化
# x = dataUtil.normalization(x)
# 标准化
x = dataUtil.standardization2(x)
# 归一化
# x = dataUtil.scale(x)
best = float(0.0)


def schaffer(p):  # 求a,b为何值时误差最小（a=1,b=0）
    p = pd.DataFrame(p)
    a = p.iloc[:input_num * 27]
    b = p.iloc[input_num * 27:]
    global best
    # p = np.array(p).reshape((12, 27))
    loss_and_metrics_train, loss_and_metrics_test, model, recall_score, prec_score = ANN.Ann(x, y, a, b, epoc_num=50)
    # test_loss = list(test_loss)
    print('test_loss:', loss_and_metrics_test)
    print('test_loss[1]:', loss_and_metrics_test[1])
    if loss_and_metrics_test[1] > best:  # 选择准确率最大的
        best = loss_and_metrics_test[1]
        pd.DataFrame(p).to_csv('../data/parm_acc.csv')
        print('p:', p)
    # '-----'
    # if recall_score > best:  # 选择查全率最大的
    #     best = recall_score
    #     pd.DataFrame(p).to_csv('../data/parm_recall.csv')
    #     print('查全率：', recall_score)
    #     print('p:', p)
    # '-----'
    # if prec_score > best:  # 选择查准率最大的
    #     best = prec_score
    #     pd.DataFrame(p).to_csv('../data/parm_prec.csv')
    #     print('查准率：', prec_score)
    #     print('p:', p)
    return loss_and_metrics_test[1]
    # return prec_score


def schaffer2(p):  # 求a,b为何值时误差最小（a=1,b=0）
    global best
    p = pd.DataFrame(p)
    a = p.iloc[:input_num * 27]
    b = p.iloc[input_num * 27:]
    # p = np.array(p).reshape((12, 27))
    test_loss, model, recall_score, prec_score = ANN.Ann2(x, y, a, b, epoc_num=15)
    # test_loss = list(test_loss)
    print('test_loss:', test_loss)
    print('test_loss:', test_loss[1])
    # print('test_loss:', test_loss[0][0])
    # print('test_loss:', type(test_loss[0][0]))
    if test_loss[1] > best:  # 选择准确率最大的
        best = test_loss[1]
        pd.DataFrame(p).to_csv('../data/parm_acc.csv')
        print('p:', p)
    # if recall_score > best:  # 选择查全率最大的
    #     best = recall_score
    #     pd.DataFrame(p).to_csv('../data/parm_recall.csv')
    #     print('查全率：', recall_score)
    #     print('p:', p)
    # '-----'
    # if prec_score > best:  # 选择查准率最大的
    #     best = prec_score
    #     pd.DataFrame(p).to_csv('../data/parm_prec.csv')
    #     print('查准率：', prec_score)
    #     print('p:', p)
    return test_loss[1]


# '--------------'
# lb为定义域的下限，ub为定义域的上限
ga = GA(func=schaffer2, n_dim=input_num * 27 + 27 * 1, size_pop=2, max_iter=1, precision=1e-7)
best_x, best_y = ga.run()
# '---'
# best_x = pd.read_csv('../data/parm_acc.csv')
# best_x = best_x.iloc[:, 1].values
# '--------------'
p = pd.DataFrame(best_x)
a = p.iloc[:input_num * 27]
b = p.iloc[input_num * 27:]
a = np.array(a).reshape((input_num, 27))
b = np.array(b).reshape((27, 1))
# 预测
en = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 140, 160, 180, 200, 220, 240, 280, 260, 300, 320, 340, 360,
      380, 400]
en1 = [50]
en2 = [30, 100, 300, 500, 700, 900, 1000, 1200, 1400]
k = 0
best_recall, best_loss, best_prec, best_acc = 0.0, 0.0, 0.0, 0.0
for n in en1:
    print('*' * 15, n)
    loss_and_metrics_train, loss_and_metrics_test, model, recall_score, prec_score = ANN.Ann(x, y, a, b, epoc_num=n)
    if loss_and_metrics_test[1] > best_acc:  # 根据精确率acc
        # if recall_score>best_recall:
        # if prec_score > best_prec:
        best_acc = loss_and_metrics_test[1]
        best_recall = recall_score
        best_prec = prec_score
        k = n

# print('循环次数:', k)
# print('精确率best_acc:', best_acc)
# print('查全率best_recall:', best_recall)
# print('查准率best_prec:', best_prec)
# print('a,b:', best_x, '\n', 'best_y:', best_y)

# Y_history = pd.DataFrame(ga.all_history_Y)
# fig, ax = plt.subplots(2, 1)
# ax[0].plot(Y_history.index, Y_history.values, '.', color='red')
# Y_history.min(axis=1).cummin().plot(kind='line')
# plt.show()
