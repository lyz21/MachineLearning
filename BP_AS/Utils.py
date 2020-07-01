# encoding=utf-8
"""
@Time : 2020/2/9 15:45 
@Author : LiuYanZhe
@File : Utils.py 
@Software: PyCharm
@Description: 工具类
"""
import matplotlib.pyplot as plt


# 绘制两条曲线并存储
def draw2Line(x1, y1, name1, x2, y2, name2, filename):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x1, y1, color='darkorange', lw=1, label=name1)
    ax1.plot(x2, y2, color='seagreen', lw=1, label=name2)
    # ax1.legend((line1, line2), ('name1', 'name2'))
    plt.legend(loc="upper right")
    ax1.set_xlabel('Train times')
    ax1.set_ylabel('E')
    ax1.set_title('Times - E curve')
    plt.savefig('pic/' + filename + '.png', dpi=400, bbox_inches='tight')
# 绘制1条曲线并存储
def draw1Line(x, y, name, filename,x_label='x',y_label='y'):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x, y, color='darkorange', lw=1, label=name)
    plt.legend(loc="upper right")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(name)
    plt.savefig('pic/' + filename + '.png', dpi=400, bbox_inches='tight')