# encoding=utf-8
"""
@Time : 2020/5/7 15:32 
@Author : LiuYanZhe
@File : SIR_IN.py 
@Software: PyCharm
@Description: 带有输入输出（人口流动）的SIR模型
"""
import numpy as np
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize, curve_fit  # 优化
from SIR_in_model_2.util import DataUtil, picUtil
import logging

'''日志设置'''


# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class SIR_IN:
    # 初始化
    def __init__(self, country_name, N, start_add=0, end_reduce=0):
        self.country_name = country_name
        self.N = N
        self.start_add = start_add
        self.end_reduce = end_reduce
        self.data_path = '../data/History_country_2020_05_06.csv'
        # 设定beta和gamma的训练及拟合函数
        self.beat_fun = self.func_lyz_ln
        self.beta_fit = self.fit_lyz_3
        self.gamma_fun = self.func_lyz_line
        self.gamma_fit = self.fit_lyz_2
        # 设定移民数，自然死亡率

    # 获取该国家总数据
    def get_data(self):
        path = self.data_path
        name = self.country_name
        N = self.N
        start_index = self.start_add
        end_index = self.end_reduce
        remove_real, infectious_real, susceptible_real, date = DataUtil.load_data_SIR_total(path, name, N, start_index,
                                                                                            end_index)
        infectious_real = infectious_real.values
        remove_real = remove_real.values
        date = date.values
        return infectious_real, remove_real, date

    # 获取总数据长度
    def get_data_length(self):
        path = self.data_path
        name = self.country_name
        N = self.N
        remove_real, infectious_real, susceptible_real, date = DataUtil.load_data_SIR_total(path, name, N)
        return len(remove_real)

    # 拆出训练数据
    def get_train_data(self, test_num):
        infectious_real, remove_real, date = self.get_data()
        infectious_train = infectious_real[:len(infectious_real) - test_num]
        remove_train = remove_real[:len(remove_real) - test_num]
        return infectious_train, remove_train

    # 计算总误差(均方误差)
    def count_err(self, real, pre):
        print('-' * 10, 'SIR_IN.count_err 开始', '-' * 10)
        print('real', len(real))
        print('pre:', len(pre))
        err = 0
        for i in range(len(real)):
            err += (real[i] - pre[i]) ** 2
        err = err / len(real)
        print('-' * 10, 'SIR_IN.count_err 结束', '-' * 10)
        return err

    # 设置起始数据
    def set_start_sub(self, start_add):
        self.start_add = start_add

    # 更改数据读取路径
    def set_data_path(self, path):
        self.data_path = path

    '''下面是SIR方法'''

    # 带有输入输出的sir主方法 beta患病率，gamma治愈率；p移民患病率；q移民中已治愈率；a因病死亡率；d自然死亡率；b移出移民率,
    def sir(self, y, t, A, beta, gamma, a, p, q, d, b):
        S, I, R = y  # N 总人口；A:移民总数
        N = S + I + R
        # dNdt = A - (d + b) * N - a * I
        dSdt = (1 - p - q) * A - (d + b + beta * I / N) * S
        dIdt = p * A + beta * S * I / N - (d + gamma + a + b) * I
        dRdt = gamma * I - (d + b) * R + q * A
        return [dSdt, dIdt, dRdt]

    # 损失函数
    def loss_function(self, params, infected, recovered, y0, influence):
        size = len(infected)
        t = np.linspace(1, size, size)
        beta, gamma = params
        A, a, p, q, d, b = influence
        solution = odeint(self.sir, y0, t, args=(A, beta, gamma, a, p, q, d, b))
        l1 = np.mean((solution[:, 1] - infected) ** 2)
        l2 = np.mean((solution[:, 2] - recovered) ** 2)
        return l1 + l2

    # 优化函数
    def fit(self, y0, infected, recovered, beta, gamma, influence):
        optimal = minimize(self.loss_function, [beta, gamma],
                           args=(infected, recovered, y0, influence),
                           method='L-BFGS-B',
                           bounds=[(0.000001, 1), (0.000001, 1)])
        # print('optimal.x:', optimal.x)
        return optimal.x

        # 获取beta和gamma

    def get_beta_gamma(self, infectious_real, remove_real, influence, beta=0.125, gamma=0.05):
        list_beta = []
        list_gamma = []
        # 获得beta、gamma值
        for i in range(len(infectious_real) - 1):
            I0 = infectious_real[i]
            R0 = remove_real[i]
            S0 = self.N - I0 - R0
            y0 = [S0, I0, R0]
            train_I = [I0, infectious_real[i + 1]]
            train_R = [R0, remove_real[i + 1]]
            beta, gamma = self.fit(y0, train_I, train_R, beta, gamma, influence)
            list_beta.append(beta)  # 比infectious_real长度小1
            list_gamma.append(gamma)
        return list_beta, list_gamma

        # 更改beta的拟合曲线方程

    def set_beta_line(self, fun_name):
        if fun_name == 'func_lyz_ln':
            self.beat_fun = self.func_lyz_ln
            self.beta_fit = self.fit_lyz_3

        # 更改gamma的拟合曲线方程

    def set_gamma_line(self, fun_name):
        if fun_name == 'func_lyz_line':
            self.gamma_fun = self.func_lyz_line
            self.gamma_fit = self.fit_lyz_2

        # 对数拟合曲线

    def func_lyz_ln(self, x, a, b, c):
        y = a * np.log(b * x) + c
        return y

        # 设定线性拟合曲线

    def func_lyz_line(self, x, a, b):
        y = a * x + b
        return y

    # 两个参数的拟合方程
    def fit_lyz_2(self, method, train_x, train_y, pre_x):
        popt, pcov = curve_fit(method, train_x, train_y,
                               bounds=([0.0000000001, -10], [10, 10.]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
        a, b = popt
        print('拟合方程为：y=', a, '*x+', b)
        pre_y = method(pre_x, a, b)
        return pre_y

        # 找到最高点

    def find_maxPoint(self, x_list, y_list):
        max_y = max(y_list)
        max_sub = y_list.index(max_y)
        max_x = x_list[max_sub]
        return max_x, max_y, max_sub

        # 三个参数的拟合方程

    def fit_lyz_3(self, method, train_x, train_y, pre_x):
        print('train_x:', train_x)
        print('train_y:', train_y)
        popt, pcov = curve_fit(method, train_x, train_y,
                               bounds=(
                                   [-10, 0.000001, -20], [10, 10., 20]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
        a, b, c = popt
        # print('拟合方程为：y=', a, '*ln', b, '*x+', c)
        print(a, b, c)
        pre_y = method(pre_x, a, b, c)
        return pre_y

    # 主方法
    def sir_main(self, forecast_add=0, test_num=0):  # 默认使用全部数据训练，并多预测0天
        # a因病死亡率；p移民患病率；q移民中已治愈率；d自然死亡率；b移出移民率
        A, a, p, q, d, b = 0, 0, 0, 0, 0, 0
        # 获取数据
        infectious_real, remove_real, date = self.get_data()
        # 获取训练数据
        if test_num == 0:
            infectious_train, remove_train = infectious_real, remove_real
        else:
            infectious_train, remove_train = self.get_train_data(test_num)
        # 根据训练数据获取beta和gamma
        list_beta, list_gamma = self.get_beta_gamma(infectious_train, remove_train, [0, 0, 0, 0, 0, 0])
        # 获得beta预测参数
        list_beta2 = self.beta_fit(self.beat_fun, np.arange(1, len(list_beta) + 1), list_beta,
                                   np.arange(1, len(list_beta) + 1 + forecast_add))
        # 获得gamma预测参数
        list_gamma2 = self.gamma_fit(self.gamma_fun, np.arange(1, len(list_gamma) + 1), list_gamma,
                                     np.arange(1, len(list_gamma) + 1 + forecast_add))
        # 获取使用线性回归的预测结果
        infectious_pre = [infectious_real[0]]
        remove_pre = [remove_real[0]]
        t = np.linspace(1, 2, 2)
        print('list_gamma2', list_gamma2)
        print('infectious_pre', infectious_pre)
        for i in range(len(list_gamma2)):
            I0 = infectious_pre[i]
            R0 = remove_pre[i]
            S0 = self.N - I0 - R0
            y0 = [S0, I0, R0]
            beta = list_beta2[i]
            gamma = list_gamma2[i]
            if i > 60:
                # a因病死亡率；p移民患病率；q移民中已治愈率；d自然死亡率；b移出移民率
                A, a, p, q, d, b = 5070 * 10000 / 365, 0, 2264396 / (
                            70.57 * 100000000), 0, 7.13 / 1000, 6260 * 10000 / (
                                           365 * self.N)
            # 求解
            solution = odeint(self.sir, y0, t, args=(A, beta, gamma, a, p, q, d, b))
            infectious_pre.append(solution[1, 1])
            remove_pre.append(solution[1, 2])
        '''绘制图像'''
        # 获取起始日期
        month, day = DataUtil.get_m_d(date)
        # 生成日期
        date_list = DataUtil.getDateList(len(infectious_train) + forecast_add, month, day)
        # 找最高点
        max_x, max_y, max_sub = self.find_maxPoint(date_list, infectious_pre)
        x_ticks = DataUtil.getDateList_interval(date_list, 20)
        picUtil.draw_four(list_beta, list_gamma, list_beta2, list_gamma2, x_ticks, 'beta_real', 'gamma_real',
                          'beta_pre',
                          'gamma_pre')
        # picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_train, remove_train)
        picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_real, remove_real,
                                 xticks=x_ticks, max_x_sub=max_sub, max_x=max_x, max_y=max_y,
                                 train_sub=len(infectious_train) - 0.5)
        err = self.count_err(infectious_real, infectious_pre)
        print('总误差：', err)
        return err


if __name__ == '__main__':
    # China = SIR_IN('中国', 1400000000)
    # China.sir_main(forecast_add=80, test_num=70)

    Italy = SIR_IN('意大利', 60431283, start_add=40)
    Italy.sir_main(forecast_add=60, test_num=30)  # 25656122.19997323

    # American = SIR('美国', 330000000, start_add=40)
    # American.sir_main(forecast_add=60, test_num=20)
