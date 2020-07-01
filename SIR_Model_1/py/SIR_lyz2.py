# encoding=utf-8
"""
@Time : 2020/4/21 18:25 
@Author : LiuYanZhe
@File : SIR_lyz2.py 
@Software: PyCharm
@Description: 分别得到每天beta和gamma，对beta和gamma做预测
"""

import numpy as np
import pandas as pd
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize, curve_fit  # 优化
from sko.GA import GA
from SIR_Model_1.util import DataUtil
from SIR_Model_1.util import picUtil
from sklearn import linear_model  # 线性回归模型
from SIR_Model_1.py import LSTM_lyz1


# 模型初始值
def get_init_data(N, I0, R0):
    S0 = N - I0 - R0
    return [S0, I0, R0]


def SIR(y, t, beta, gamma):
    S, I, R = y
    dSdt = -S * (I / (S + I + R)) * beta
    dIdt = beta * S * I / (S + I + R) - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def loss_function(params, infected, recovered, y0):
    size = len(infected)
    t = np.linspace(1, size, size)
    beta, gamma = params
    solution = odeint(SIR, y0, t, args=(beta, gamma))
    l1 = np.mean((solution[:, 1] - infected) ** 2)
    l2 = np.mean((solution[:, 2] - recovered) ** 2)
    return l1 + l2


def fit(y0, infected, recovered, beta, gamma):
    optimal = minimize(loss_function, [beta, gamma],
                       args=(infected, recovered, y0),
                       method='L-BFGS-B',
                       bounds=[(0.000001, 1), (0.000001, 1)])
    # print('optimal.x:', optimal.x)
    return optimal.x


def sklearn_line(train_x, train_y, pre_x):
    train_x = np.array(train_x).reshape(-1, 1)
    train_y = np.array(train_y).reshape(-1, 1)
    pre_x = np.array(pre_x).reshape(-1, 1)

    regr = linear_model.LinearRegression()
    regr.fit(train_x, train_y)
    a, b = regr.coef_, regr.intercept_
    # print('a=', a, 'b=', b)
    list_beta2 = regr.predict(pre_x)
    return np.array(list_beta2).flatten()


def np_line(train_x, train_y, pre_x, n):  # n为n阶线性模型
    coef = np.polyfit(train_x, train_y, n)
    poly_fit = np.poly1d(coef)
    pre_y = poly_fit(pre_x)
    return pre_y


def func_lyz_line(x, a, b):
    y = a * x + b
    return y


def func_lyz_e1(x, a, b, c):
    y = a * np.exp(b / x) + c
    return y


def func_lyz_e2(x, a, b, c):
    y = a * np.exp(b * x) + c
    return y


def func_lyz_mi(x, a, b, c):
    y = a * np.power(x, b) + c
    return y


def func_lyz_ln(x, a, b, c):
    y = a * np.log(b * x) + c
    return y


def fit_lyz_2(method, train_x, train_y, pre_x):
    popt, pcov = curve_fit(method, train_x, train_y,
                           bounds=([0.0000000001, -10], [10, 10.]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
    a, b = popt
    print('拟合方程为：y=', a, '*x+', b)
    pre_y = method(pre_x, a, b)
    return pre_y


def fit_lyz_3(method, train_x, train_y, pre_x):
    popt, pcov = curve_fit(method, train_x, train_y,
                           bounds=([-10, 0.000001, -20], [10, 10., 20]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
    a, b, c = popt
    # print('拟合方程为：y=', a, '*ln', b, '*x+', c)
    print(a, b, c)
    pre_y = method(pre_x, a, b, c)
    return pre_y


def get_beta_gamma(infectious_real, remove_real, beta=0.125, gamma=0.05):
    list_beta = []
    list_gamma = []
    # 获得beta、gamma值
    for i in range(len(infectious_real) - 1):
        I0 = infectious_real[i]
        R0 = remove_real[i]
        S0 = N - I0 - R0
        y0 = [S0, I0, R0]
        train_I = [I0, infectious_real[i + 1]]
        train_R = [R0, remove_real[i + 1]]
        beta, gamma = fit(y0, train_I, train_R, beta, gamma)
        list_beta.append(beta)  # 比infectious_real长度小1
        list_gamma.append(gamma)
    return list_beta, list_gamma


def get_data(start_num=4195, end_num=4272, day_num_add=0):  # 默认获取意大利数据
    remove_real, infectious_real, susceptible_real, date = DataUtil.load_data_total(
        path='../data/History_country_2020_04_19.csv', line_num1=start_num - 2 + day_num_add,
        line_num2=end_num - 1)  # 4193-4271意大利
    infectious_real = infectious_real.values
    remove_real = remove_real.values
    date = date.values
    return infectious_real, remove_real, date


def find_maxPoint(x_list, y_list):
    max_y = max(y_list)
    max_sub = y_list.index(max_y)
    max_x = x_list[max_sub]
    return max_x, max_y, max_sub


if __name__ == '__main__':
    # 设置人群总人数为N
    # N, month, day = 60431283, 3, 5  # 意大利
    # N,month,day = 66488991,3,25  # 英国
    N, month, day = 46730000, 3, 14  # 西班牙
    # N=82927922    # 德国
    # N, month, day = 140005000, 2, 5  # 中国
    # N = 82000000  # 土耳其
    # N, month, day = 330000000, 3, 18  # 美国

    # infectious_real, remove_real, date = get_data(day_num_add=34)  # 获取意大利数据 3.10日开始(39)
    # infectious_real, remove_real,date = get_data(start_num=4141, end_num=4194, day_num_add=30)  # 获取英国数据(封国4169)
    infectious_real, remove_real, date = get_data(start_num=4494, end_num=4529)  # 获取西班牙数据（按封国时间）
    # infectious_real, remove_real,date = get_data(start_num=523, end_num=553)  # 获取德国数据（按封国时间）
    # infectious_real, remove_real, date = get_data(start_num=79, end_num=153)  # 获取中国数据（按封国时间）
    # infectious_real, remove_real,date = get_data(start_num=3720, end_num=3759,day_num_add=20)  # 获取土耳其数据（无确切封城时间）
    # infectious_real, remove_real, date = get_data(start_num=554, end_num=613, day_num_add=27)  # 获取美国数据（无确切封城时间）
    # 训练获取beta、gamma列表
    test_num = 0  # 划分测试集数目
    infectious_train = infectious_real[:len(infectious_real) - test_num]
    # infectious_train = infectious_real[:30]
    remove_train = remove_real[:len(remove_real) - test_num]
    # remove_train = remove_real[:30]

    # 根据训练数据获取beta和gamma
    list_beta, list_gamma = get_beta_gamma(infectious_train, remove_train)
    print('len(list_beta):', len(list_beta))
    print('len(list_gamma):', len(list_gamma))
    # 使用线性回归模型预测结果
    add_days = 90  # 多预测的天数
    list_beta2 = fit_lyz_3(func_lyz_ln, np.arange(1, len(list_beta) + 1), list_beta,
                           np.arange(1, len(list_beta) + 1 + add_days))
    # list_beta2 = LSTM_lyz1.LSTM_lyz(list_beta, add_days, n_steps=5, loop_num=300)     # 使用循环神经网络LSTM训练算法获得预测结果
    print('len(list_beta2):', len(list_beta2))
    list_gamma2 = fit_lyz_2(func_lyz_line, np.arange(1, len(list_gamma) + 1), list_gamma,
                            np.arange(1, len(list_gamma) + 1 + add_days))
    print('len(list_gamma2):', len(list_gamma2))
    # list_gamma2 = np_line(np.arange(1, len(list_gamma) + 1), list_gamma, np.arange(1, len(list_gamma) + 1 + add_days),
    #                       1)
    # list_beta2 = sklearn_line(train_t, list_beta, pre_t)  # 一元一次线性
    # list_beta2 = np_line(train_t, list_beta, pre_t, 5)  # 5 7     # 一元n次线性
    # list_gamma2 = sklearn_line(np.arange(1, len(list_gamma) + 1), list_gamma,
    #                            np.arange(1, len(list_gamma) + 1 + add_days))
    # 获取使用线性回归的预测结果
    infectious_pre = [infectious_real[0]]
    remove_pre = [remove_real[0]]
    t = np.linspace(1, 2, 2)
    for i in range(len(list_gamma2)):
        I0 = infectious_pre[i]
        R0 = remove_pre[i]
        S0 = N - I0 - R0
        y0 = [S0, I0, R0]
        beta = list_beta2[i]
        gamma = list_gamma2[i]
        # 求解
        solution = odeint(SIR, y0, t, args=(beta, gamma))
        infectious_pre.append(solution[1, 1])
        remove_pre.append(solution[1, 2])
    # print('预测I:', infectious_pre)
    # print('真实I:', list(infectious_real))
    # print('预测R:', np.array(remove_pre))
    # print('真实R:', remove_real)
    print('beta:', list_beta)
    print('gamma:', list_gamma)

    # 绘制图像
    print(date)
    date_list = DataUtil.getDateList(len(infectious_train) + add_days, month, day)
    # 找最高点
    max_x, max_y, max_sub = find_maxPoint(date_list, infectious_pre)
    print(infectious_pre)
    print(max_x, max_y, max_sub)
    x_ticks = DataUtil.getDateList_interval(date_list, 20)
    picUtil.draw_four(list_beta, list_gamma, list_beta2, list_gamma2, x_ticks, 'beta_real', 'gamma_real', 'beta_pre',
                      'gamma_pre')
    # picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_train, remove_train)
    picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_real, remove_real,
                             xticks=x_ticks, max_x_sub=max_sub, max_x=max_x, max_y=max_y)
