# encoding=utf-8
"""
@Time : 2020/4/20 16:41 
@Author : LiuYanZhe
@File : test_lyz1.py 
@Software: PyCharm
@Description: lyz探索利用遗传算法求解 函数参数最优问题,y=ax+b
"""
from scipy.integrate import odeint
from sko.GA import GA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def schaffer(p):  # 求a,b为何值时误差最小（a=1,b=0）
    a, b = p
    # 训练数据
    train_x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    train_y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # 计算损失
    loss = 0
    for i in range(len(train_x)):
        p_y = a * train_x[i] + b
        loss += abs(p_y - train_y[i])  # 差的绝对值
    return loss


# lb为定义域的下限，ub为定义域的上限
ga = GA(func=schaffer, n_dim=2, size_pop=50, max_iter=800, lb=[-1, -1], ub=[1, 1], precision=1e-7)
best_x, best_y = ga.run()
print('a,b:', best_x, '\n', 'best_y:', best_y)

Y_history = pd.DataFrame(ga.all_history_Y)
fig, ax = plt.subplots(2, 1)
ax[0].plot(Y_history.index, Y_history.values, '.', color='red')
Y_history.min(axis=1).cummin().plot(kind='line')
plt.show()
