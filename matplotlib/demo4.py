# encoding=utf-8
"""
@Time : 2020/1/10 19:25 
@Author : LiuYanZhe
@File : demo4.py 
@Software: PyCharm
@Description: 饼图,图形
"""
import numpy as np
import matplotlib.pyplot as plt

'''饼图'''
# 数据
n = 10
Z = np.random.rand(n)
lable = ['data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8', 'data9', 'data10']

# 创建画板
fig = plt.figure(figsize=(7.5, 4))
fig.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95)
# 第一个子图
ax1 = fig.add_subplot(1, 2, 1)
ax1.pie(Z)  # 饼图
plt.axis('equal')
# 第二个子图
ax2 = fig.add_subplot(1, 2, 2)
ax2.pie(Z, explode=np.ones(n) * 0.01, labels=lable, colors=['%f' % (i / float(n)) for i in range(n)],
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

plt.axis('equal')
plt.xticks([])
plt.yticks([])
# 存储图像
plt.savefig('./pic/demo4.1.png', dpi=200, bbox_inches='tight')

'''多边形'''
# 新建画板
fig2 = plt.figure()
# 添加子图
ax3 = fig2.add_subplot(1, 1, 1)
# 画多边形
rect = plt.Rectangle((0.1, 0.6), 0.2, 0.3, color='r')  # 矩形 参数：（左下点坐标），长，高
circ1 = plt.Circle((0.7, 0.2), 0.15, color='b', alpha=0.6)  # 椭圆  参数：（椭圆心坐标），半径
circ2 = plt.Circle((0.3, 0.4), 0.1, color='g', alpha=0.6)  # 圆
pgon = plt.Polygon([[0.9, 0.9], [0.7, 0.6], [0.6, 0.8], [0.4, 0.7], [0.5, 0.9]], color='y', alpha=0.7)  # 多边形，参数：每个顶点的坐标
ax3.add_patch(rect)
ax3.add_patch(circ1)
ax3.add_patch(circ2)
ax3.add_patch(pgon)
fig2.canvas.draw()
# 存储图像
plt.savefig('./pic/demo4.2.png', dpi=200, bbox_inches='tight')
# 显示画板
plt.show()
'''
pie()参数：
x       :(每一块)的比例，如果sum(x) > 1会使用sum(x)归一化；
labels  :(每一块)饼图外侧显示的说明文字；
explode :(每一块)离开中心距离；
startangle :起始绘制角度,默认图是从x轴正方向逆时针画起,如设定=90则从y轴正方向画起；
shadow  :在饼图下面画一个阴影。默认值：False，即不画阴影；
labeldistance :label标记的绘制位置,相对于半径的比例，默认值为1.1, 如<1则绘制在饼图内侧；
autopct :控制饼图内百分比设置,可以使用format字符串或者format function
        '%1.1f'指小数点前后位数(没有用空格补齐)；
pctdistance :类似于labeldistance,指定autopct的位置刻度,默认值为0.6；
radius  :控制饼图半径，默认值为1；
counterclock ：指定指针方向；布尔值，可选参数，默认为：True，即逆时针。将值改为False即可改为顺时针。
wedgeprops ：字典类型，可选参数，默认值：None。参数字典传递给wedge对象用来画一个饼图。例如：wedgeprops={'linewidth':3}设置wedge线宽为3。
textprops ：设置标签（labels）和比例文字的格式；字典类型，可选参数，默认值为：None。传递给text对象的字典参数。
center ：浮点类型的列表，可选参数，默认值：(0,0)。图标中心位置。
frame ：布尔类型，可选参数，默认值：False。如果是true，绘制带有表的轴框架。
rotatelabels ：布尔类型，可选参数，默认为：False。如果为True，旋转每个label到指定的角度。

其中：
colors=['%f' % (i / float(n)) for i in range(n)]
等同于
colors=['0.000000', '0.100000', '0.200000', '0.300000', '0.400000', '0.500000', '0.600000', '0.700000', '0.800000', '0.900000']
'''
