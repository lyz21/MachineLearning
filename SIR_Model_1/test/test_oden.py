# encoding=utf-8
"""
@Time : 2020/4/21 18:37 
@Author : LiuYanZhe
@File : test_oden.py 
@Software: PyCharm
@Description: 
"""
from scipy.integrate import odeint  # 求解微分方程
import numpy as np
from scipy.optimize import minimize  # 优化


def SIR(y, t, beta, gamma):
    S, I, R = y
    dSdt = -S * (I / (S + I + R)) * beta
    dIdt = beta * S * I / (S + I + R) - gamma * I
    dRdt = gamma * I
    # print('beta:', beta, 'gamma:', gamma)
    return [dSdt, dIdt, dRdt]


def loss_function(params, infected, recovered, y0):
    size = len(infected)
    t = np.linspace(1, size, size)
    beta, gamma = params
    solution = odeint(SIR, y0, t, args=(beta, gamma))
    l1 = np.mean((solution[:, 1] - infected) ** 2)
    l2 = np.mean((solution[:, 2] - recovered) ** 2)

    print(solution)
    print(l1 + l2)
    return l1 + l2


def fit(y0, infected, recovered, beta, gamma):
    optimal = minimize(loss_function, [beta, gamma],
                       args=(infected, recovered, y0),
                       method='L-BFGS-B',
                       bounds=[(0.000001, 1), (0.000001, 1)])
    print('optimal.x:', optimal.x)
    return optimal.x


if __name__ == '__main__':
    # 设置人群总人数为N
    N = 58000000
    # 设置初始时的感染人数I0为239
    I0 = 239
    # 设置初始时的恢复人数R0为31
    R0 = 31
    # 所以，初始易感者人群人数 = 总人数 - 初始感染人数 - 初始治愈人数
    S0 = N - I0 - R0
    # 设置初始值
    y0 = [S0, I0, R0]
    # 设置估计疫情的时间跨度为60天
    t = np.linspace(1, 2, 2)

    # 设置beta值等于0.125        beta/gamma=a,a的区间约为[1.4-5.5]
    # beta = 0.125
    beta = 0
    # 设置gamma的值等于0.05
    # gamma = 0.05
    gamma = 0.5
    # 训练
    train_I = [239, 245]
    train_R = [31, 45]
    beta, gamma = fit(y0, train_I, train_R, beta, gamma)
    print('beta:', beta, 'gamma:', gamma)
    # 求解
    solution = odeint(SIR, y0, t, args=(beta, gamma))
    # 要求Python的所有输出不用科学计数法表示
    np.set_printoptions(suppress=True)
    # 输出结果的前四行进行查看
    # print(solution[0:4, 0:3])
    print(solution)
