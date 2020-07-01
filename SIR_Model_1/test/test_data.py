# encoding=utf-8
"""
@Time : 2020/4/20 18:02 
@Author : LiuYanZhe
@File : test_data.py 
@Software: PyCharm
@Description: 测试数据
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 60431283


def draw(infectious_real, recovered_real, days=100):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(0, days, days)

    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    # ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='infectious_real')
    # ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='recovered_real')
    ax.plot(t, infectious_real)
    ax.plot(t, recovered_real)
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.box(False)
    plt.show()


def load_data(path='../data/History_country_2020_03_27.csv', line_num1=1965, line_num2=2025):
    pd1 = pd.read_csv(path).iloc[line_num1:line_num2, :].loc[:, ('total_confirm', 'total_dead', 'total_heal')]
    recovered_real = pd1['total_dead'] + pd1['total_heal']  # 移除
    # infectious_real = pd1['total_confirm'] - recovered_real  # 感染
    infectious_real = pd1['total_confirm']  # 感染
    susceptible_real = N - recovered_real - infectious_real  # 易感
    return recovered_real, infectious_real, susceptible_real


day_num_add = 39  # 从3.10号封城开始
recovered_real, infectious_real, susceptible_real = load_data(path='../data/History_country_2020_04_19.csv',
                                                              line_num1=4193 + day_num_add, line_num2=4271)
print(recovered_real)
print(infectious_real)
draw(infectious_real, recovered_real, len(recovered_real))
