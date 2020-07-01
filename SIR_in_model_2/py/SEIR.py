# encoding=utf-8
"""
@Time : 2020/5/9 17:50 
@Author : LiuYanZhe
@File : SEIR.py 
@Software: PyCharm
@Description: SEIR模型 lyz
"""
import numpy as np
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize, curve_fit  # 优化
from sko.GA import GA
from SIR_in_model_2.util import DataUtil, picUtil

'''日志设置'''


# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class SEIR:
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
        # 设定参数
        self.gamma1 = 1 / 4

    # 获取该国家总数据
    def get_data(self):
        path = self.data_path
        name = self.country_name
        N = self.N
        start_index = self.start_add
        end_index = self.end_reduce
        remove_real, suscept_real, infectious_real, susceptible_real, date = DataUtil.load_data_SEIR_total(path, name,
                                                                                                           N,
                                                                                                           start_index,
                                                                                                           end_index)
        infectious_real = infectious_real.values  # I
        suscept_real = suscept_real.values  # E
        remove_real = remove_real.values  # R
        date = date.values
        return infectious_real, suscept_real, remove_real, date

    # 获取总数据长度
    def get_data_length(self):
        path = self.data_path
        name = self.country_name
        N = self.N
        remove_real, infectious_real, susceptible_real, date = DataUtil.load_data_SIR_total(path, name, N)
        return len(remove_real)

    # 拆出训练数据
    def get_train_data(self, test_num):
        infectious_real, suscept_real, remove_real, date = self.get_data()
        infectious_train = infectious_real[:len(infectious_real) - test_num]
        suscept_train = suscept_real[:len(suscept_real) - test_num]
        remove_train = remove_real[:len(remove_real) - test_num]
        return infectious_train, suscept_train, remove_train

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

    # 设置gamme1
    def set_gamme1(self, gamme1):
        self.gamma1 = gamme1

    # 更改数据读取路径
    def set_data_path(self, path):
        self.data_path = path

    '''下面是SIR方法'''

    # alpha 疑似中患病率[0,1]；beta1, beta2 易感个体与患病（潜伏）接触并被传染概率[0,1]；gamma1 移除潜伏期，潜伏期倒数； gamma2 移除确诊
    def seir(self, y, t, alpha, beta1, beta2, gamma2):
        gamma1 = self.gamma1  # 从疑似移入确诊的概率，潜伏期倒数
        S, E, I, R = y
        N = S + E + I + R
        dSdt = gamma1 * (1 - alpha) * E - S * I * beta1 / N - alpha * S * E * beta2 / N
        dEdt = S * I * beta1 / N + alpha * S * E * beta2 / N - gamma1 * (1 - alpha) * E - alpha * gamma1 * E
        dIdt = alpha * gamma1 * E - gamma2 * I
        dRdt = gamma2 * I
        return [dSdt, dEdt, dIdt, dRdt]

    def seir_2(self, y, t, beta, gamma2):
        gamma1 = self.gamma1  # 从疑似移入确诊的概率，潜伏期倒数
        S, E, I, R = y
        N = S + E + I + R
        dSdt = -S * I * beta / N
        dEdt = S * I * beta / N - gamma1 * E
        dIdt = gamma1 * E - gamma2 * I
        dRdt = gamma2 * I
        return [dSdt, dEdt, dIdt, dRdt]

    # 损失函数
    def loss_function(self, params, E, I, R, y0):
        size = len(I)
        t = np.linspace(1, size, size)
        alpha, beta1, beta2, gamma2 = params
        solution = odeint(self.seir, y0, t, args=(alpha, beta1, beta2, gamma2))
        l1 = np.mean((solution[:, 1] - E) ** 2)
        l2 = np.mean((solution[:, 2] - I) ** 2)
        l3 = np.mean((solution[:, 3] - R) ** 2)
        return l1 + l2 + l3

    def loss_function_2(self, params, E, I, R, y0):
        size = len(I)
        t = np.linspace(1, size, size)
        alpha, gamma2 = params
        solution = odeint(self.seir_2, y0, t, args=(alpha, gamma2))
        l1 = np.mean((solution[:, 1] - E) ** 2)
        l2 = np.mean((solution[:, 2] - I) ** 2)
        l3 = np.mean((solution[:, 3] - R) ** 2)
        return l1 + l2 + l3

    # 优化函数
    def fit(self, y0, E, I, R, alpha, beta1, beta2, gamma2):
        optimal = minimize(self.loss_function, [alpha, beta1, beta2, gamma2],
                           args=(E, I, R, y0),
                           method='L-BFGS-B',
                           bounds=[(0.000001, 1), (0.000001, 1), (0.000001, 1), (0.000001, 1)])
        # print('optimal.x:', optimal.x)
        return optimal.x

    def fit_2(self, y0, E, I, R, alpha, gamma2):
        optimal = minimize(self.loss_function_2, [alpha, gamma2],
                           args=(E, I, R, y0),
                           method='L-BFGS-B',
                           bounds=[(0.000001, 1), (0.000001, 1)])
        # print('optimal.x:', optimal.x)
        return optimal.x

    # 损失函数
    def loss_function_ga(self, alpha, beta1, beta2, gamma2):
        E, I, R, y0 = self.parameter
        size = len(I)
        t = np.linspace(1, size, size)
        solution = odeint(self.seir, y0, t, args=(alpha, beta1, beta2, gamma2))
        l1 = np.mean((solution[:, 1] - E) ** 2)
        l2 = np.mean((solution[:, 2] - I) ** 2)
        l3 = np.mean((solution[:, 3] - R) ** 2)
        return l1 + l2 + l3

    # 损失函数
    def loss_function_ga_2(self, alpha, gamma2):
        E, I, R, y0 = self.parameter
        size = len(I)
        t = np.linspace(1, size, size)
        solution = odeint(self.seir_2, y0, t, args=(alpha, gamma2))
        l1 = np.mean((solution[:, 1] - E) ** 2)
        l2 = np.mean((solution[:, 2] - I) ** 2)
        l3 = np.mean((solution[:, 3] - R) ** 2)
        return l1 + l2 + l3

    # 通过遗传算法获取参数估计值
    def fit_ga(self, y0, E, I, R, n):
        self.parameter = [E, I, R, y0]
        self.y0 = y0
        if n == 4:
            ga = GA(func=self.loss_function_ga, n_dim=4, size_pop=50, max_iter=300, lb=[0, 0, 0, 0],
                    ub=[1, 1, 1, 1])
        elif n == 2:
            ga = GA(func=self.loss_function_ga_2, n_dim=2, size_pop=50, max_iter=300, lb=[0, 0],
                    ub=[1, 1])  # 遗传算法求解
        best_x, best_y = ga.run()
        if n == 4:
            alpha, beta1, beta2, gamma2 = best_x[0], best_x[1], best_x[2], best_x[3]
            return alpha, beta1, beta2, gamma2
        elif n == 2:
            alpha, gamma2 = best_x[0], best_x[1]
            return alpha, gamma2

    # 获取beta和gamma

    def get_SEIR_parameter(self, E_real, I_real, R_real, n):
        list_alpha = []
        list_beta1 = []
        list_beta2 = []
        list_gamma2 = []
        # 获得beta、gamma值
        for i in range(len(I_real) - 1):
            I0 = I_real[i]
            E0 = E_real[i]
            R0 = R_real[i]
            S0 = self.N - I0 - E0 - R0
            y0 = [S0, E0, I0, R0]
            train_E = [I0, E_real[i + 1]]
            train_I = [I0, I_real[i + 1]]
            train_R = [R0, R_real[i + 1]]
            if n == 4:
                # alpha, beta1, beta2, gamma2 = self.fit_ga(y0, train_E, train_I, train_R, n)
                alpha, beta1, beta2, gamma2 = self.fit(y0, train_E, train_I, train_R, alpha=0.1, beta1=0.11, beta2=0.07,
                                                       gamma2=0.03)
                list_alpha.append(alpha)  # 比infectious_real长度小1
                list_beta1.append(beta1)
                list_beta2.append(beta2)
                list_gamma2.append(gamma2)
            elif n == 2:
                # alpha, gamma2 = self.fit_ga(y0, train_E, train_I, train_R, n)
                alpha, gamma2 = self.fit_2(y0, train_E, train_I, train_R, alpha=0.1, gamma2=0.2)
                list_alpha.append(alpha)  # 比infectious_real长度小1
                list_gamma2.append(gamma2)

        if n == 4:
            return list_alpha, list_beta1, list_beta2, list_gamma2
        elif n == 2:
            return list_alpha, list_gamma2

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
        n = 2
        self.gamma1 = 1/4
        # 获取数据
        infectious_real, suscept_real, remove_real, date = self.get_data()

        # 获取训练数据
        if test_num == 0:
            infectious_train, suscept_train, remove_train = infectious_real, suscept_real, remove_real
        else:
            infectious_train, suscept_train, remove_train = self.get_train_data(test_num)
        # 根据训练数据获取参数
        if n == 4:
            list_alpha, list_beta1, list_beta2, list_gamma2 = self.get_SEIR_parameter(suscept_train, infectious_train,
                                                                                      remove_train, n)
        elif n == 2:
            list_alpha, list_gamma2 = self.get_SEIR_parameter(suscept_train, infectious_train,
                                                              remove_train, n)
        # # 获得beta预测参数
        # list_beta2 = self.beta_fit(self.beat_fun, np.arange(1, len(list_beta) + 1), list_beta,
        #                            np.arange(1, len(list_beta) + 1 + forecast_add))
        # # 获得gamma预测参数
        # list_gamma2 = self.gamma_fit(self.gamma_fun, np.arange(1, len(list_gamma) + 1), list_gamma,
        #                              np.arange(1, len(list_gamma) + 1 + forecast_add))
        # 获取使用线性回归的预测结果
        suscept_pre = [suscept_real[0]]
        infectious_pre = [infectious_real[0]]
        remove_pre = [remove_real[0]]
        t = np.linspace(1, 2, 2)
        print('list_gamma2:', list_gamma2)
        print('suscept_pre:', suscept_pre)
        print('infectious_pre:', infectious_pre)
        for i in range(len(list_gamma2)):
            E0 = suscept_pre[i]
            I0 = infectious_pre[i]
            R0 = remove_pre[i]
            S0 = self.N - I0 - R0
            y0 = [S0, E0, I0, R0]
            if n == 4:
                alpha, beta1, beta2, gamma2 = list_alpha[i], list_beta1[i], list_beta2[i], list_gamma2[i]
                # 求解
                solution = odeint(self.seir, y0, t, args=(alpha, beta1, beta2, gamma2))
            elif n == 2:
                alpha, gamma2 = list_alpha[i], list_gamma2[i]
                # 求解
                solution = odeint(self.seir_2, y0, t, args=(alpha, gamma2))
            suscept_pre.append(solution[1, 1])
            infectious_pre.append(solution[1, 2])
            remove_pre.append(solution[1, 3])
        '''绘制图像'''
        # 获取起始日期
        month, day = DataUtil.get_m_d(date)
        # 生成日期
        date_list = DataUtil.getDateList(len(infectious_train) + forecast_add, month, day)
        # 找最高点
        max_x, max_y, max_sub = self.find_maxPoint(date_list, infectious_pre)
        x_ticks = DataUtil.getDateList_interval(date_list, 20)
        if n == 4:
            picUtil.draw_four(list_alpha, list_beta1, list_beta2, list_gamma2,
                              np.linspace(1, len(list_alpha) + 1, len(list_alpha) + 1), 'list_alpha',
                              'list_beta1', 'list_beta2', 'list_gamma2')
        elif n == 2:
            picUtil.draw_two(list_alpha, list_gamma2, np.linspace(1, len(list_alpha) + 1), 'list_alpha', 'list_gamma2')
        # picUtil.draw_four(list_beta, list_gamma, list_beta2, list_gamma2, x_ticks, 'beta_real', 'gamma_real',
        #                   'beta_pre',
        #                   'gamma_pre')
        # picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_train, remove_train)
        # picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_real, remove_real,
        #                          xticks=x_ticks, max_x_sub=max_sub, max_x=max_x, max_y=max_y,
        #                          train_sub=len(infectious_train) - 0.5)
        picUtil.draw_preAndreal3(np.array(suscept_pre), np.array(infectious_pre), np.array(remove_pre), suscept_real,
                                 infectious_real, remove_real,
                                 xticks=x_ticks, max_x_sub=max_sub, max_x=max_x, max_y=max_y,
                                 train_sub=len(infectious_train) - 0.5)
        err = self.count_err(infectious_real, infectious_pre)
        print('总误差：', err)
        return err


if __name__ == '__main__':
    China = SEIR('中国', 1400000000)
    # China.sir_main(forecast_add=80, test_num=70)
    China.sir_main()

    # Italy = SEIR('意大利', 60431283, start_add=40)
    # Italy.sir_main(forecast_add=60, test_num=30)  # 25656122.19997323
    # Italy.sir_main()  # 25656122.19997323

    # American = SIR('美国', 330000000, start_add=40)
    # American.sir_main(forecast_add=60, test_num=20)
