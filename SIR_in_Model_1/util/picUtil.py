# encoding=utf-8
"""
@Time : 2020/4/21 18:28 
@Author : LiuYanZhe
@File : picUtil.py 
@Software: PyCharm
@Description: 绘制图像工具类
"""
import matplotlib.pyplot as plt
import numpy as np


def draw_preAndreal(predict_result, infectious_real, recovered_real, xticks, days=100):
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
    plt.xticks(range(0, max(len(t), len(tpredict)), 20), xticks)
    plt.box(False)
    plt.show()


def draw_preAndreal2(infectious_pre, recovered_pre, infectious_real, recovered_real, xticks, max_x_sub, max_x, max_y):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(1, len(infectious_pre), len(infectious_pre))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='infectious_real')
    ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='recovered_real')
    # 绘制预测的I曲线、R曲线与S曲线
    ax.plot(tpredict, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_predict')
    ax.plot(tpredict, recovered_pre, 'g', alpha=0.5, lw=2, label='recovered_predict')
    # 绘制最高曲线
    # print('max_x_sub:',max_x_sub)
    # print('max_y:',max_x_sub)
    ax.plot([max_x_sub + 1, max_x_sub + 1], [0, max_y], '-.', alpha=0.5, lw=1)
    ax.text(max_x_sub+1+2, max_y+2, 'Max_point:('+str(max_x)+','+str(int(max_y))+')')
    # ax.plot([0, 0], [0, max_y], '-.', alpha=0.5, lw=1)
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(1, max(len(t), len(tpredict)), 20), xticks)
    plt.box(False)
    plt.show()


def draw_two(list1, list2, xticks, name1='1', name2='2'):
    t1 = np.linspace(1, len(list1), len(list1))
    t2 = np.linspace(1, len(list2), len(list2))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    ax.scatter(t1, list1, c='r', marker='o', alpha=0.6, lw=0.3, label=name1)
    ax.scatter(t2, list2, c='g', marker='o', alpha=0.6, lw=0.3, label=name2)
    # 绘制预测的I曲线、R曲线与S曲线
    # ax.plot(tpredict, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_predict')
    # ax.plot(tpredict, recovered_pre, 'g', alpha=0.5, lw=2, label='recovered_predict')
    # ax.plot(t, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_predict')
    # ax.plot(t, recovered_pre, 'g', alpha=0.5, lw=2, label='recovered_predict')

    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(0, max(len(t1), len(t2)), 20), xticks)
    plt.box(False)
    plt.show()


def draw_four(list1, list2, list3, list4, xticks, name1='1', name2='2', name3='3', name4='4'):
    t = np.linspace(1, len(list1), len(list1))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    ax.scatter(t, list1, c='r', marker='o', alpha=0.6, lw=0.3, label=name1)
    ax.scatter(t, list2, c='g', marker='o', alpha=0.6, lw=0.3, label=name2)
    t2 = np.linspace(1, len(list3), len(list3))
    # 绘制预测的I曲线、R曲线与S曲线
    # ax.plot(tpredict, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_predict')
    # ax.plot(tpredict, recovered_pre, 'g', alpha=0.5, lw=2, label='recovered_predict')
    ax.plot(t2, list3, 'r', alpha=0.5, lw=2, label=name3)
    ax.plot(t2, list4, 'g', alpha=0.5, lw=2, label=name4)
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 设置纵坐标
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(1, max(len(t), len(t2)), 20), xticks)
    plt.box(False)
    plt.show()
