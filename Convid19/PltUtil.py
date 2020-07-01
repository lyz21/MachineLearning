# encoding=utf-8
"""
@Time : 2020/3/28 17:18 
@Author : LiuYanZhe
@File : PltUtil.py 
@Software: PyCharm
@Description: 绘图工具类
"""
import matplotlib.pyplot as plt
import numpy as np
from Convid19 import dateUtil


def DrawBox(data, xticks=0, yticks=0, rotation=0, pic_name='box'):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # ax = plt.subplot(1, 1, 1)
    # fig, ax_arr = plt.subplots(1, 1)
    # ax1 = ax_arr[0]
    # ax2 = ax_arr[1]

    ######################################################################################
    # plt.rcParams['font.sans-serif']=['STSong']     ## 中文宋体
    # plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    # plt.rcParams['font.sans-serif']=['Kaiti']      ## 中文楷体
    # plt.rcParams['font.sans-serif']=['Lisu']       ## 中文隶书
    # plt.rcParams['font.sans-serif']=['FangSong']   ## 中文仿宋
    # plt.rcParams['font.sans-serif']=['YouYuan']    ## 中文幼圆

    # styles = ['normal', 'italic', 'oblique']
    # weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
    ######################################################################################

    # if xticks != 0:
    #     plt.xticks(range(len(xticks)), xticks, rotation=rotation, fontsize=5.0)
    #     # plt.xticks(xticks, rotation=rotation)
    # else:
    #     plt.xticks(rotation=rotation, fontsize=5.0)
    # if yticks != 0:
    #     plt.yticks(range(1, len(yticks)), yticks, rotation=rotation)
    # ax.boxplot(data)
    if xticks != 0:
        plt.boxplot(data, flierprops={'markersize': 5}  # 异常值属性
                    )
    else:
        plt.boxplot(data, labels=xticks,  # 设置标签
                    flierprops={'markersize': 5}  # 异常值属性
                    )
    plt.xticks(rotation=rotation, fontsize=7.0)
    plt.savefig('./pic/' + pic_name + '.png', dpi=400, bbox_inches='tight')
    plt.show()
    # plt.pause(10)


def DrawBox_pd(data, rotation=0, pic_name='box'):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # ax = plt.subplot(1, 1, 1)
    # fig, ax_arr = plt.subplots(1, 1)
    # ax1 = ax_arr[0]
    # ax2 = ax_arr[1]

    ######################################################################################
    # plt.rcParams['font.sans-serif']=['STSong']     ## 中文宋体
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    # plt.rcParams['font.sans-serif']=['Kaiti']      ## 中文楷体
    # plt.rcParams['font.sans-serif']=['Lisu']       ## 中文隶书
    # plt.rcParams['font.sans-serif']=['FangSong']   ## 中文仿宋
    # plt.rcParams['font.sans-serif']=['YouYuan']    ## 中文幼圆

    styles = ['normal', 'italic', 'oblique']
    weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
    ######################################################################################

    data.boxplot()
    plt.xticks(rotation=60, fontsize=6.0)
    plt.savefig('./pic/' + pic_name + '.png', dpi=400, bbox_inches='tight')
    plt.show()


def DrawPlot(data_y, data_x=0, xticks=0, yticks=0, rotation=0, pic_name='plot'):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if data_x == 0:
        data_x = range(0, len(data_y))
    if xticks != 0:
        plt.xticks(range(0, len(data_y)), xticks, rotation=rotation, fontsize=5.0)
    ax.plot(data_x, data_y, label='line')
    plt.savefig('./pic/' + pic_name + '.png', dpi=400, bbox_inches='tight')


# 将日期划分后的绘制成网格
def DrawImShow():
    div_data = [0,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
                0,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,
                1,1,1,1,1,1,1,0,1,1,1,1,1,1]  # 长度为88
    div_arr = np.array(div_data).reshape((8, 11))
    date_list = dateUtil.getDateList(len(div_data), con_str='.')
    # for i in range(8):
    #     sub = 11 * i
    #     date = date_list[sub]
    #     # 设定颜色
    #     if div_data[sub] == 1:
    #         color = 'white'
    #     else:
    #         color = '#08306B'
    #     plt.text(-0.45, i+0.07, date, color=color)
    # plt.text(3-0.4, 2.07, '1.26', color='white')
    # plt.text(2-0.4, 4.07, '2.16', color='white')
    for i in range(len(div_data)):
        x = i % 11 - 0.35
        y = int(i / 11) + 0.07
        date = date_list[i]
        # 设定颜色
        if div_data[i] == 1:
            color = 'white'
        else:
            color = '#08306B'
        plt.text(x, y, date, color=color, fontsize=8)
    plt.xticks([])
    plt.yticks([])
    # 画分割线，纵线
    for i in np.arange(0.5, 9.6, 1):
        plt.plot([i, i], [-0.5, 7.5], color='black')
    for i in np.arange(0.5, 7.6, 1):
        plt.plot([-0.5, 10.5], [i, i], color='black')  ##08306B
    # 画标注线
    # lw = 1.5
    # alpha = 1
    # deviation = 0
    # plt.plot([2.5, 10.5], [1.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 10.5], [2.5 - deviation, 2.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 10.5], [3.5 - deviation, 3.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 2.5], [4.5 - deviation, 4.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, -0.5], [4.5 - deviation, 2.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([2.5, 2.5], [4.5 - deviation, 3.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([2.5, 2.5], [2.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([10.5, 10.5], [3.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    plt.imshow(div_arr, cmap='Blues', interpolation='none', vmin=0, vmax=1, aspect='equal')
    plt.savefig('./pic/kmeans_time.png', dpi=400, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    DrawImShow()
