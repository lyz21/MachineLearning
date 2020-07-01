# encoding=utf-8
"""
@Time : 2020/4/19 17:59 
@Author : LiuYanZhe
@File : SIR_test2.py 
@Software: PyCharm
@Description: 数据酷客，SIR模型学习2，封装
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize  # 优化
import pandas as pd

N = 60431283  # 意大利


class SIRModel:
    def __init__(self, beta, gamma, method):
        self.__beta = beta
        self.__gamma = gamma
        self.__method = method
        self.__optimal = None
        self.__predict_loss = None

    def sir_model(self, y0, t, beta, gamma):
        S, I, R = y0
        dSdt = -beta * S * I / (S + I + R)
        dIdt = beta * S * I / (S + I + R) - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    def loss_function(self, params, infected, recovered, y0):
        size = len(infected)
        t = np.linspace(1, size, size)
        beta, gamma = params
        solution = odeint(self.sir_model, y0, t, args=(beta, gamma))
        l1 = np.mean((solution[:, 1] - infected) ** 2)
        l2 = np.mean((solution[:, 2] - recovered) ** 2)
        return l1 + l2

    def fit(self, y0, infected, recovered):
        self.__optimal = minimize(self.loss_function, [self.__beta, self.__gamma],
                                  args=(infected, recovered, y0),
                                  method=self.__method,
                                  bounds=[(0.00000001, 1), (0.00000001, 1)])

    def predict(self, test_y0, days):
        predict_result = odeint(self.sir_model, test_y0, np.linspace(1, days, days), args=tuple(self.__optimal.x))
        return predict_result

    def get_optimal_params(self):
        return self.__optimal.x

    def get_predict_loss(self):
        return self.__predict_loss


# 模型初始值
def get_init_data(N, I0, R0):
    S0 = N - I0 - R0
    return [S0, I0, R0]


# 加载数据
def load_data(path='../data/History_country_2020_03_27.csv', line_num1=1965, line_num2=2025):
    pd1 = pd.read_csv(path).iloc[line_num1:line_num2, :].loc[:, ('total_confirm', 'total_dead', 'total_heal')]
    recovered_real = pd1['total_dead'] + pd1['total_heal']  # 移除
    # infectious_real = pd1['total_confirm'] - recovered_real  # 感染
    infectious_real = pd1['total_confirm']  # 感染
    susceptible_real = N - recovered_real - infectious_real  # 易感
    return recovered_real, infectious_real, susceptible_real


def draw(predict_result, infectious_real, recovered_real, days=100):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(0, days, days)

    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    # ax.plot(t, infectious_real, 'o', alpha=0.5, lw=1, label='infectious_real')
    # ax.plot(t, recovered_real, 'o', alpha=0.5, lw=1, label='recovered_real')
    ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='infectious_real')
    ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='recovered_real')
    # ax.scatter(t, infectious_real, 'black', alpha=0.5, label='infectious_real')
    # ax.scatter(t, recovered_real, 'black', alpha=0.5, label='recovered_real')
    # 绘制预测的I曲线、R曲线与S曲线
    ax.plot(tpredict, predict_result[:, 1], 'r', alpha=0.5, lw=2, label='infectious_predict')
    ax.plot(tpredict, predict_result[:, 2], 'g', alpha=0.5, lw=2, label='recovered_predict')
    # ax.plot(tpredict, predict_result[:, 0], 'b-.', alpha=0.5, lw=2, label='susceptible_predict')

    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.box(False)
    plt.show()


if __name__ == '__main__':
    day_num_add = 39    # 从3.10号封城开始
    recovered_real, infectious_real, susceptible_real = load_data(path='../data/History_country_2020_04_19.csv',
                                                                  line_num1=4193 + day_num_add, line_num2=4271)
    # 参数
    days = len(recovered_real)+20    # 多预测20天
    I0 = infectious_real.values[0]
    R0 = recovered_real.values[0]
    y0 = get_init_data(N, I0, R0)

    # 建立模型，设定beta gamma初始值
    new_model = SIRModel(0.0001, 0.0001, 'L-BFGS-B')
    infectious_train, recovered_train = infectious_real, recovered_real

    # 训练模型，输入参数：初始值，训练集
    new_model.fit(y0, infectious_train, recovered_train)
    # 输出估计最优参数
    # best_params = new_model.get_optimal_params()
    # print(best_params)
    # 预测
    predict_result = new_model.predict(y0, days)

    draw(predict_result, infectious_real, recovered_real, days=days)
