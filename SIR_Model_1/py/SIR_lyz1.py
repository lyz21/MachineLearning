# encoding=utf-8
"""
@Time : 2020/4/20 18:17 
@Author : LiuYanZhe
@File : SIR_lyz1.py 
@Software: PyCharm
@Description: 使用遗传算法求解最优beta,gamma值     -->效果不明显
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize  # 优化
from sko.GA import GA
from SIR_Model_1.util import DataUtil
N = 60431283  # 意大利


# 模型初始值
def get_init_data(N, I0, R0):
    S0 = N - I0 - R0
    return [S0, I0, R0]


def draw(predict_result, infectious_real, recovered_real, days=100):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(0, days, days)

    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='infectious_real')
    ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='recovered_real')
    # 绘制预测的I曲线、R曲线与S曲线
    ax.plot(tpredict, predict_result[:, 1], 'r', alpha=0.5, lw=2, label='infectious_predict')
    ax.plot(tpredict, predict_result[:, 2], 'g', alpha=0.5, lw=2, label='recovered_predict')

    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.box(False)
    plt.show()


class SIRModel:
    def __init__(self, beta, gamma, method, infected, recovered, y0):
        self.__beta = beta
        self.__gamma = gamma
        self.__method = method
        self.__optimal = None
        self.__predict_loss = None
        self.__infected = infected
        self.__recovered = recovered
        self.__y0 = y0

    def sir_model(self, y0, t, beta, gamma):
        S, I, R = y0
        print('S:', S, 'I:', I, 'R:', R)
        dSdt = -beta * S * I / (S + I + R)
        dIdt = beta * S * I / (S + I + R) - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    def loss_function(self, params, infected, recovered, y0):
        size = len(infected)
        t = np.linspace(1, size, size)
        beta, gamma = params
        solution = odeint(self.sir_model, y0, t, args=(beta, gamma))
        # pre_infected_total = DataUtil.calcu_total(infected.values[0], solution[:, 1])
        # pre_recovered_total = DataUtil.calcu_total(recovered.values[0], solution[:, 2])
        l1 = np.mean((solution[:, 1] - infected) ** 2)
        l2 = np.mean((solution[:, 2] - recovered) ** 2)
        # l1 = np.mean((pre_infected_total - infected) ** 2)
        # l2 = np.mean((pre_recovered_total - recovered) ** 2)
        print('solution[:, 1]', solution[:, 2])
        # print('pre_recovered_total:',pre_recovered_total)
        print('recovered:', recovered.values)
        print(l1 + l2)
        return l1 + l2

    def loss_function2(self, beta, gamma):
        size = len(self.__infected)
        t = np.linspace(1, size, size)
        # beta, gamma = params
        solution = odeint(self.sir_model, self.__y0, t, args=(beta, gamma))
        # print('solution[:1],infected:', solution[:1], self.__infected)
        l1 = np.mean((solution[:, 1] - self.__infected) ** 2)
        l2 = np.mean((solution[:, 2] - self.__recovered) ** 2)
        print('loss=', l1 + l2)
        return l1 + l2

    def loss_function2_beta(self, beta, gamma):
        size = len(self.__infected)
        t = np.linspace(1, size, size)
        # beta, gamma = params
        solution = odeint(self.sir_model, self.__y0, t, args=(beta, gamma))
        # print('solution[:1],infected:', solution[:1], self.__infected)
        l1 = np.mean((solution[:, 1] - self.__infected) ** 2)
        print('loss_l1=', l1)
        return l1

    def loss_function2_gamma(self, beta, gamma):
        size = len(self.__infected)
        t = np.linspace(1, size, size)
        # beta, gamma = params
        solution = odeint(self.sir_model, self.__y0, t, args=(beta, gamma))
        # print('solution[:1],infected:', solution[:1], self.__infected)
        l2 = np.mean((solution[:, 2] - self.__recovered) ** 2)
        print('loss_l2=', l2)
        return l2

    def fit(self, y0, infected, recovered):
        self.__optimal = minimize(self.loss_function, [self.__beta, self.__gamma],
                                  args=(infected, recovered, y0),
                                  method=self.__method,
                                  bounds=[(0.000001, 1), (0.000001, 1)])

    def fit2(self):
        # ga_beta = GA(func=self.loss_function2_beta, n_dim=2, size_pop=50, max_iter=1000, lb=[0, 0], ub=[1, 1], precision=1e-7)
        # ga_gamma = GA(func=self.loss_function2_gamma, n_dim=2, size_pop=50, max_iter=1000, lb=[0, 0], ub=[1, 1], precision=1e-7)
        # best_x_beta, best_y = ga_beta.run()
        # best_x_gamma, best_y = ga_gamma.run()
        ga = GA(func=self.loss_function2, n_dim=2, size_pop=50, max_iter=3000, lb=[0, 0], ub=[1, 1], precision=1e-7)
        best_x, best_y = ga.run()
        # self.__beta = best_x_beta[0]
        # self.__gamma = best_x_gamma[1]
        self.__beta = best_x[0]
        self.__gamma = best_x[1]
        print('best_x:', best_x)
        # print('best_beta:', best_x_beta)  # [0.16029371 0.09209991]
        # print('best_gamma:', best_x_gamma)  # [0.16029371 0.09209991]
        # self.__beta = 0.13043983
        # self.__gamma = 0.05632794

    def predict(self, test_y0, days):
        if self.__optimal == None:
            predict_result = odeint(self.sir_model, test_y0, np.linspace(1, days, days),
                                    args=tuple([self.__beta, self.__gamma]))
        else:
            predict_result = odeint(self.sir_model, test_y0, np.linspace(1, days, days),
                                    args=tuple(self.__optimal.x))
        return predict_result

    # def get_optimal_params(self):
    #     return self.__optimal.x
    #
    # def get_predict_loss(self):
    #     return self.__predict_loss


if __name__ == '__main__':
    day_num_add = 39  # 从3.10号封城开始
    # recovered_real, infectious_real, susceptible_real = DataUtil.load_data_taday(
    #     path='../data/History_country_2020_04_19.csv', line_num1=4193 + day_num_add, line_num2=4271)
    recovered_real, infectious_real, susceptible_real = DataUtil.load_data_total(
        path='../data/History_country_2020_04_19.csv', line_num1=4193 + day_num_add, line_num2=4271)
    # 参数
    days = len(recovered_real)  # 多预测20天
    I0 = infectious_real.values[10]
    R0 = recovered_real.values[10]
    y0 = get_init_data(N, I0, R0)
    # I0 = infectious_real
    # R0 = recovered_real
    # y0 = get_init_data(N, I0, R0)

    # 建立模型，设定beta gamma初始值
    # new_model = SIRModel(0.0001, 0.0001, 'L-BFGS-B')
    new_model = SIRModel(0.2, 0.3, 'L-BFGS-B', infectious_real, recovered_real, y0)
    infectious_train, recovered_train = infectious_real, recovered_real

    # 训练模型，输入参数：初始值，训练数据1,训练数据2
    new_model.fit(y0, infectious_train, recovered_train)
    # new_model.fit2()
    # 输出估计最优参数
    # best_params = new_model.get_optimal_params()
    # print(best_params)
    # 预测
    predict_result = new_model.predict(y0, days)
    draw(predict_result, infectious_real, recovered_real, days=days)
