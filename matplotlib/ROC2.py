# encoding=utf-8
"""
@Time : 2020/2/8 16:31 
@Author : LiuYanZhe
@File : ROC2.py 
@Software: PyCharm
@Description: 
"""


def roc_draw(predict, ground_truth):
    nums = len(predict)

    x, y = 1, 1

    # 对列表排序
    index = np.argsort(predict)  # 返回排序后的下标
    ground = ground_truth[index]

    x_step = 1.0 / (nums - sum(ground_truth))  # 负样本步长
    y_step = 1. / sum(ground_truth)

    res_x = []
    res_y = []
    # 依次生成每个点的坐标，若为正例，则（x,y+1/m正），若为反例，则（x+1/m反,y）
    for i in range(nums):
        if ground[i] == 1:
            y -= y_step
        else:
            x -= x_step

        res_x.append(x)
        res_y.append(y)
    return res_x, res_y


import numpy as np

# predict = np.arange(0, 1, 0.01)  # 生成间隔为0.01的预测阈值
# ground_truth = np.random.randint(0, 2, 100)
predict = [1, 2, 3, 4, 5, 6, 7, 8, 9]
predict = np.array(predict)
ground_truth = [1, 1, 1, 1, 0, 0, 0, 0, 0]
ground_truth = np.array(ground_truth)
print('predict', predict)
print('ground_truth', ground_truth)

import matplotlib.pyplot as plt

x, y = roc_draw(predict, ground_truth)

ax1 = plt.subplot(1, 1, 1)
ax1.set_xlim(0, 1)  # 设置横纵坐标范围
ax1.set_ylim(0, 1)
ax1.plot(x, y)
plt.show()
