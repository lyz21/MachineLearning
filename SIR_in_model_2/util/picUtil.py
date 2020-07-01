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
    # 保存图像
    plt.savefig('../pic/draw_preAndreal.png', dpi=400, bbox_inches='tight')
    plt.show()


# 绘制预测和真实曲线，各两条
def draw_preAndreal2(infectious_pre, recovered_pre, infectious_real, recovered_real, xticks, max_x_sub, max_x, max_y,
                     train_sub=0, file_name='draw_preAndreal2.png', title=' '):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(1, len(infectious_pre), len(infectious_pre))
    fig = plt.figure(facecolor='w', dpi=120, figsize=(6, 4))
    ax = fig.add_subplot(111)
    # 绘制真实的I曲线与真实的R曲线
    ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='infectious_real')
    ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='remove_real')
    # 绘制预测的I曲线、R曲线与S曲线
    ax.plot(tpredict, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_pre')
    ax.plot(tpredict, recovered_pre, 'g', alpha=0.5, lw=2, label='remove_pre')
    # 绘制最高曲线
    print('max_x_sub:', max_x_sub)
    ax.plot([max_x_sub + 1, max_x_sub + 1], [0, max_y], '-.', alpha=0.5, lw=1)
    # 标注最高点
    ax.annotate('Highest point of forecast\n (' + str(max_x) + ',' + str(int(max_y)) + ')', xy=(max_x_sub + 1, max_y),
                xytext=(max_x_sub - 3, max_y + max_y / 5),
                arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
    # 绘制分界线
    y_max = max(max(recovered_pre), max(infectious_pre))
    ax.plot([train_sub + 1, train_sub + 1], [0, y_max], alpha=0.5, lw=1)
    # 绘制训练和预测的标注
    ax.text(train_sub - len(recovered_pre) / 7, y_max * 1 / 3, '← Fitting')
    ax.text(train_sub + 3, y_max * 1 / 3, 'Prediction →')
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(1, max(len(t), len(tpredict)), 20), xticks, rotation=-30)
    plt.box(False)
    plt.title(title, y=-0.35)
    # 保存图像
    plt.savefig('../pic/' + file_name, dpi=400, bbox_inches='tight')
    # plt.show()


# 绘制预测和真实曲线，各3条
def draw_preAndreal3(suscept_pre, infectious_pre, recovered_pre, suscept_real, infectious_real, recovered_real, xticks,
                     max_x_sub, max_x, max_y,
                     train_sub=0):
    t = np.linspace(1, len(infectious_real), len(infectious_real))
    tpredict = np.linspace(1, len(infectious_pre), len(infectious_pre))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    # 绘制真实的E,IR曲线
    ax.scatter(t, suscept_real, c='b', marker='o', alpha=0.6, lw=0.3, label='E_real')
    ax.scatter(t, infectious_real, c='r', marker='o', alpha=0.6, lw=0.3, label='I_real')
    ax.scatter(t, recovered_real, c='g', marker='o', alpha=0.6, lw=0.3, label='R_real')
    # 绘制预测的I曲线、R曲线与S曲线
    ax.plot(tpredict, suscept_pre, 'b', alpha=0.5, lw=2, label='E_pre')
    ax.plot(tpredict, infectious_pre, 'r', alpha=0.5, lw=2, label='I_pre')
    ax.plot(tpredict, recovered_pre, 'g', alpha=0.5, lw=2, label='R_pre')
    # 绘制最高曲线
    print('max_x_sub:', max_x_sub)
    ax.plot([max_x_sub + 1, max_x_sub + 1], [0, max_y], '-.', alpha=0.5, lw=1)
    # 标注最高点
    ax.annotate('Highest point of forecast\n (' + str(max_x) + ',' + str(int(max_y)) + ')', xy=(max_x_sub + 1, max_y),
                xytext=(max_x_sub - 3, max_y + max_y / 5),
                arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
    # 绘制分界线
    ax.plot([train_sub + 1, train_sub + 1], [0, max(max(recovered_pre), max(infectious_pre))], alpha=0.5, lw=1)
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(1, max(len(t), len(tpredict)), 20), xticks)
    plt.box(False)
    # 保存图像
    plt.savefig('../pic/draw_preAndreal3.png', dpi=400, bbox_inches='tight')
    plt.show()


def draw_two(list1, list2, xticks, name1='1', name2='2', style='scatter'):
    t1 = np.linspace(1, len(list1), len(list1))
    t2 = np.linspace(1, len(list2), len(list2))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax.scatter(t1, list1, c='r', marker='o', alpha=0.6, lw=0.3, label=name1)
        ax.scatter(t2, list2, c='g', marker='o', alpha=0.6, lw=0.3, label=name2)
    elif style == 'line':
        ax.plot(t1, list1, 'r', alpha=0.5, lw=2, label=name1)
        ax.plot(t2, list2, 'g', alpha=0.5, lw=2, label=name2)
    else:
        print('样式设置出错')
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
    # 保存图像
    plt.savefig('../pic/draw_two.png', dpi=400, bbox_inches='tight')
    plt.show()


def draw_one(list1, xticks, style='scatter', file_name='draw_four.png', title=' '):
    t1 = np.linspace(1, len(list1), len(list1))
    fig = plt.figure(facecolor='w', dpi=100)
    ax = fig.add_subplot(111)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax.scatter(t1, list1, c='r', marker='o', alpha=0.6, lw=0.3)
    elif style == 'line':
        ax.plot(t1, list1, 'r', alpha=0.5, lw=2)
    else:
        print('样式设置出错')
    # ax.plot(t, infectious_pre, 'r', alpha=0.5, lw=2, label='infectious_predict')
    # ax.plot(t, recovered_pre, 'g', alpha=0.5, lw=2, label='recovered_predict')
    # 画一条y=1的线
    ax.plot([0, len(list1)], [1, 1])
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 添加图例
    # ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(0, len(t1), 20), xticks, rotation=-30)
    plt.box(False)
    # 设置标题
    plt.title(title, y=-0.3)
    # 保存图像
    plt.savefig('../pic/' + file_name, dpi=400, bbox_inches='tight')
    # plt.show()


def draw_R0_4(country1, country2, country3, country4, style='scatter'):
    R01, R02, R03, R04 = country1.R0, country2.R0, country3.R0, country4.R0
    title1, title2, title3, title4 = country1.title, country2.title, country3.title, country4.title
    xticks1, xticks2, xticks3, xticks4 = country1.x_ticks, country2.x_ticks, country3.x_ticks, country4.x_ticks
    fig = plt.figure(facecolor='w', dpi=120, figsize=(14, 10))
    t1 = np.linspace(1, len(R01), len(R01))
    ax1 = fig.add_subplot(2, 2, 1)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax1.scatter(t1, R01, c='r', marker='o', alpha=0.6, lw=0.3)
    elif style == 'line':
        ax1.plot(t1, R01, 'r', alpha=0.5, lw=2)
    else:
        print('样式设置出错')
    # 画一条y=1的线
    ax1.plot([0, len(R01)], [1, 1])
    ax1.text(len(R01) / 2, 1.5, 'y=1')
    # 设置横纵坐标轴
    ax1.set_xlabel('Time/days')
    ax1.set_ylabel('R0')
    # 绘制分界线
    y_max = max(R01)
    y_min = min(R01)
    ax1.plot([country1.train_sub + 1, country1.train_sub + 1], [y_min, y_max], alpha=0.5, lw=1)
    # 添加图例
    # ax.legend()
    ax1.grid(axis='y')
    plt.xticks(range(0, len(t1), 20), xticks1, rotation=-30)
    plt.box(False)
    # 设置标题
    plt.title(title1, y=-0.3)
    '''第二个'''
    t2 = np.linspace(1, len(R02), len(R02))
    ax2 = fig.add_subplot(2, 2, 2)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax2.scatter(t2, R02, c='r', marker='o', alpha=0.6, lw=0.3)
    elif style == 'line':
        ax2.plot(t2, R02, 'r', alpha=0.5, lw=2)
    else:
        print('样式设置出错')
    # 画一条y=1的线
    ax2.plot([0, len(R02)], [1, 1])
    ax2.text(len(R02) / 2, 1.5, 'y=1')
    # 标注第一个小于0的点
    sub, x, y = country2.first_sub, country2.first_x, country2.first_y
    ax2.annotate('(' + str(x) + ',' + str(int(y)) + ')', xy=(sub + 1, y),
                 xytext=(sub, y + max(R02) / 3),
                 arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
    # 设置横纵坐标轴
    ax2.set_xlabel('Time/days')
    ax2.set_ylabel('R0')
    # 绘制分界线
    y_max = max(R02)
    y_min = min(R02)
    ax2.plot([country2.train_sub + 1, country2.train_sub + 1], [y_min, y_max], alpha=0.5, lw=1)
    # 添加图例
    # ax.legend()
    ax2.grid(axis='y')
    plt.xticks(range(0, len(t2), 20), xticks2, rotation=-30)
    plt.box(False)
    # 设置标题
    plt.title(title2, y=-0.3)
    '''第3个'''
    t3 = np.linspace(1, len(R03), len(R03))
    ax3 = fig.add_subplot(2, 2, 3)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax3.scatter(t3, R03, c='r', marker='o', alpha=0.6, lw=0.3)
    elif style == 'line':
        ax3.plot(t3, R03, 'r', alpha=0.5, lw=2)
    else:
        print('样式设置出错')
    # 画一条y=1的线
    ax3.plot([0, len(R03)], [1, 1])
    ax3.text(len(R03) / 2, 1.5, 'y=1')
    # 标注第一个小于0的点
    sub, x, y = country3.first_sub, country3.first_x, country3.first_y
    ax3.annotate('(' + str(x) + ',' + str(int(y)) + ')', xy=(sub + 1, y),
                 xytext=(sub, y + max(R03) / 3),
                 arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
    # 设置横纵坐标轴
    ax3.set_xlabel('Time/days')
    ax3.set_ylabel('R0')
    # 绘制分界线
    y_max = max(R03)
    y_min = min(R03)
    ax3.plot([country3.train_sub + 1, country3.train_sub + 1], [y_min, y_max], alpha=0.5, lw=1)
    # 添加图例
    # ax.legend()
    ax3.grid(axis='y')
    plt.xticks(range(0, len(t3), 20), xticks3, rotation=-30)
    plt.box(False)
    # 设置标题
    plt.title(title3, y=-0.3)
    '''第4个'''
    t4 = np.linspace(1, len(R04), len(R04))
    ax4 = fig.add_subplot(2, 2, 4)
    if style == 'scatter':
        # 绘制真实的I曲线与真实的R曲线
        ax4.scatter(t4, R04, c='r', marker='o', alpha=0.6, lw=0.3)
    elif style == 'line':
        ax4.plot(t4, R04, 'r', alpha=0.5, lw=2)
    else:
        print('样式设置出错')
    # 画一条y=1的线
    ax4.plot([0, len(R04)], [1, 1])
    ax4.text(len(R04) / 2, 1.5, 'y=1')
    # 标注第一个小于0的点
    sub, x, y = country4.first_sub, country4.first_x, country4.first_y
    ax4.annotate('(' + str(x) + ',' + str(int(y)) + ')', xy=(sub + 1, y),
                 xytext=(sub, y + max(R04) / 3),
                 arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
    # 设置横纵坐标轴
    ax4.set_xlabel('Time/days')
    ax4.set_ylabel('R0')
    # 绘制分界线
    y_max = max(R04)
    y_min = min(R04)
    ax4.plot([country4.train_sub + 1, country4.train_sub + 1], [y_min, y_max], alpha=0.5, lw=1)

    # 添加图例
    # ax.legend()
    ax4.grid(axis='y')
    plt.xticks(range(0, len(t4), 20), xticks4, rotation=-30)
    plt.box(False)
    # 设置标题
    plt.title(title4, y=-0.3)
    # 保存图像
    plt.savefig('../pic/R0.png', dpi=400, bbox_inches='tight')
    plt.show()


def draw_four(list1, list2, list3, list4, xticks, name1='1', name2='2', name3='3', name4='4',
              file_name='draw_four.png', title=' '):
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
    # # 绘制分界线
    # ax.plot([train_sub + 1, train_sub + 1], [0, max(list3)], alpha=0.5, lw=1)
    # 设置横纵坐标轴
    ax.set_xlabel('Time/days')
    ax.set_ylabel('Number')
    # 设置纵坐标
    # 添加图例
    ax.legend()
    ax.grid(axis='y')
    plt.xticks(range(1, max(len(t), len(t2)), 20), xticks, rotation=-30)
    plt.box(False)
    plt.title(title, y=-0.3)
    # 保存图像
    plt.savefig('../pic/' + file_name, dpi=400, bbox_inches='tight')
    # plt.show()
