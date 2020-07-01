# encoding=utf-8
"""
@Time : 2020/5/6 17:35 
@Author : LiuYanZhe
@File : SIR.py
@Software: PyCharm
@Description: SIR模型对象化
"""
import numpy as np
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize, curve_fit  # 优化
from SIR_in_model_2.util import DataUtil, picUtil


# from SIR_in_Model_1.py import LSTM_lyz1


class SIR:
    # 初始化
    def __init__(self, country_name, N, start_add=0, end_reduce=0):
        self.country_name = country_name
        self.N = N
        self.start_add = start_add
        self.end_reduce = end_reduce
        self.data_path = '../data/History_country_2020_05_06.csv'
        # self.data_path = '../data/History_country_2020_06_01.csv'
        self.title = ''
        # 设定beta和gamma的训练及拟合函数
        self.beat_fun = self.func_lyz_ln
        self.beta_fit = self.fit_lyz_3
        self.gamma_fun = self.func_lyz_line
        self.gamma_fit = self.fit_lyz_2

    # 设置标题
    def set_title(self, title):
        self.title = title

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

    # 定义sir主方法
    def sir(self, y, t, beta, gamma):
        S, I, R = y
        dSdt = -S * (I / (S + I + R)) * beta
        dIdt = beta * S * I / (S + I + R) - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    # 损失函数
    def loss_function(self, params, infected, recovered, y0):
        size = len(infected)
        t = np.linspace(1, size, size)
        beta, gamma = params
        solution = odeint(self.sir, y0, t, args=(beta, gamma))
        l1 = np.mean((solution[:, 1] - infected) ** 2)
        l2 = np.mean((solution[:, 2] - recovered) ** 2)
        return l1 + l2

    # 优化函数
    def fit(self, y0, infected, recovered, beta, gamma):
        optimal = minimize(self.loss_function, [beta, gamma],
                           args=(infected, recovered, y0),
                           method='L-BFGS-B',
                           bounds=[(0.000001, 1), (0.000001, 1)])
        # print('optimal.x:', optimal.x)
        return optimal.x

    # 获取beta和gamma
    def get_beta_gamma(self, infectious_real, remove_real, beta=0.125, gamma=0.05):
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
            beta, gamma = self.fit(y0, train_I, train_R, beta, gamma)
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

    # 寻找第一个小于0的点,返回该值和下标
    def find_first(self, x_list, y_list):
        print('y_list=',y_list)
        y_list=list(y_list)
        for i in range(len(y_list)):
            if y_list[i] < 0:
                return i, x_list[i], y_list[i]

    # 三个参数的拟合方程
    def fit_lyz_3(self, method, train_x, train_y, pre_x):
        print('train_x:', train_x)
        print('train_y:', train_y)
        popt, pcov = curve_fit(method, train_x, train_y,
                               bounds=([-10, 0.000001, -20], [10, 10., 20]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
        a, b, c = popt
        print('拟合方程为：y=', a, '*ln(', b, '*x)+', c)
        print(a, b, c)
        pre_y = method(pre_x, a, b, c)
        return pre_y

    # 主方法
    def sir_main(self, forecast_add=0, test_num=0):  # 默认使用全部数据训练，并多预测0天
        # 获取数据
        infectious_real, remove_real, date = self.get_data()
        # 获取训练数据
        if test_num == 0:
            infectious_train, remove_train = infectious_real, remove_real
        else:
            infectious_train, remove_train = self.get_train_data(test_num)
        print('训练数据长度：', len(infectious_train))
        # 根据训练数据获取beta和gamma
        list_beta, list_gamma = self.get_beta_gamma(infectious_train, remove_train)
        # 使用卷积对数据降噪
        # kernel = np.hanning(3)  # 随机生成一个卷积核（对称的）
        # kernel /= kernel.sum()
        # list_beta = np.convolve(list_beta, kernel, 'valid')
        # list_gamma = np.convolve(list_gamma, kernel, 'valid')
        # picUtil.draw_two(list_beta, list_beta_, np.arange(1, len(list_beta) + 1), style='line')
        # print('len(list_beta):',len(list_beta),'len(list_beta_):',len(list_beta_))
        # 获得beta预测参数
        list_beta2 = self.beta_fit(self.beat_fun, np.arange(1, len(list_beta) + 1), list_beta,
                                   np.arange(1, len(list_beta) + 1 + forecast_add))
        # list_beta2 = LSTM_lyz1.LSTM_lyz(list_beta, forecast_add, n_steps=5, loop_num=300)  # 使用循环神经网络LSTM训练算法获得预测结果
        # 获得gamma预测参数
        list_gamma2 = self.gamma_fit(self.gamma_fun, np.arange(1, len(list_gamma) + 1), list_gamma,
                                     np.arange(1, len(list_gamma) + 1 + forecast_add))
        # 获取使用线性回归的预测结果
        infectious_pre = [infectious_real[0]]
        remove_pre = [remove_real[0]]
        t = np.linspace(1, 2, 2)
        for i in range(len(list_gamma2)):
            I0 = infectious_pre[i]
            R0 = remove_pre[i]
            S0 = self.N - I0 - R0
            y0 = [S0, I0, R0]
            beta = list_beta2[i]
            gamma = list_gamma2[i]
            # 求解
            solution = odeint(self.sir, y0, t, args=(beta, gamma))
            infectious_pre.append(solution[1, 1])
            remove_pre.append(solution[1, 2])
        # R0 = np.array(list_beta2) / np.array(list_gamma2) * (self.N - infectious_pre[0] - remove_pre[0])
        self.R0 = (np.array(list_beta2) / (np.array(list_gamma2) * self.N)) * (
                self.N - infectious_pre[0] - remove_pre[0])
        # print('R0:', R0)
        '''绘制图像'''
        # 获取起始日期
        month, day = DataUtil.get_m_d(date)
        # 生成日期
        date_list = DataUtil.getDateList(len(infectious_train) + forecast_add, month, day)
        # 找最高点
        max_x, max_y, max_sub = self.find_maxPoint(date_list, infectious_pre)
        # 寻找第一个小于0的点
        self.first_sub, self.first_x, self.first_y = self.find_first(date_list, list(self.R0))
        x_ticks = DataUtil.getDateList_interval(date_list, 20)
        self.x_ticks = x_ticks
        self.train_sub = len(infectious_train) - 0.5
        # picUtil.draw_one(self.R0, x_ticks, file_name=self.country_name + '-参数', title=self.title)
        # picUtil.draw_four(list_beta, list_gamma, list_beta2, list_gamma2, x_ticks, 'beta_real', 'gamma_real',
        #                   'beta_pre',
        #                   'gamma_pre', file_name=self.country_name + '-参数', title=self.title)
        # picUtil.draw_preAndreal2(np.array(infectious_pre), np.array(remove_pre), infectious_real, remove_real,
        #                          xticks=x_ticks, max_x_sub=max_sub, max_x=max_x, max_y=max_y,
        #                          train_sub=len(infectious_train) - 0.5,
        #                          file_name=self.country_name + '-人数', title = self.title
        # )
        err = self.count_err(infectious_real, infectious_pre)
        print('总误差：', err)
        return err


if __name__ == '__main__':
    China = SIR('中国', 1400000000, start_add=0, end_reduce=0)
    China.set_title('(a) China')
    China.sir_main(forecast_add=70, test_num=70)
    #
    Italy = SIR('意大利', 60431283, start_add=40)  # yes
    Italy.set_title('(b) Italy')
    Italy_err = Italy.sir_main(forecast_add=80, test_num=30)  # 25656122.19997323
    #
    Britain = SIR('英国', 66488991, start_add=40)
    Britain.set_title('(c) Britain')
    Britain.sir_main(forecast_add=100, test_num=0)
    #
    America = SIR('美国', 330000000, start_add=45)
    America.set_title('(d) America')
    America.sir_main(forecast_add=100, test_num=0)

    picUtil.draw_R0_4(China, Italy, Britain, America)

    # Russia = SIR('俄罗斯', 146000000, start_add=40)   # no
    # Russia.set_title('Russia')
    # Russia.sir_main(forecast_add=200, test_num=0)

    # Brazil = SIR('巴西', 210000000, start_add=30)   # no
    # Brazil.set_title('Brazil')
    # Brazil.sir_main(forecast_add=60, test_num=0)

    # Japan = SIR('日本', 124776364, start_add=10)    # no
    # Japan.set_title('Japan')
    # Japan.sir_main(forecast_add=20)
    #
    # Korean = SIR('韩国', 51635256, start_add=10)    # no
    # Korean.set_title('Korean')
    # Korean.sir_main(forecast_add=20)
    #
    # Spain = SIR('西班牙', 46730000, start_add=10)    # no
    # Spain.set_title('Spain')
    # Spain.sir_main(forecast_add=30, test_num=20)
    #
    # France = SIR('法国', 66987244, start_add=30)    # no
    # France.set_title('France')
    # France.sir_main(forecast_add=40, test_num=20)
    #
    # Netherlands = SIR('荷兰', 17260000, start_add=20) # no
    # Netherlands.set_title('Netherlands')
    # Netherlands.sir_main(forecast_add=30, test_num=5)

    # India = SIR('印度', 1324000000, start_add=40)   # no
    # India.sir_main(forecast_add=100)

    # Singapore = SIR('新加坡', 5640000, start_add=0)  # no
    # Singapore.sir_main(forecast_add=100)
