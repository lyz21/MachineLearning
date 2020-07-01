# encoding=utf-8
"""
@Time : 2020/1/10 17:57 
@Author : LiuYanZhe
@File : demo3.py 
@Software: PyCharm
@Description: 柱形图，直方图,散点图，气泡图
"""
import numpy as np
import matplotlib.pyplot as plt

# 绘制柱状图
ax1 = plt.subplot(1, 1, 1)  # 创建一个画板，同时创建一个子图
x_index = np.arange(5)  # 用来做柱的索引
x_data = ('A', 'B', 'C', 'D', 'E')  # 元组，与列表类似，但不可更改
y1_data = (20, 35, 30, 35, 27)
y2_data = (25, 32, 34, 20, 25)
bar_width = 0.35  # 每个柱的宽度
ax1.bar(x_index, y1_data, width=bar_width, alpha=0.6, label='bar2')
ax1.bar(x_index + bar_width, y2_data, width=bar_width, alpha=0.6, label='bar2')
plt.legend()  # 显示图例
plt.xticks(x_index + bar_width / 2, x_data)  # 调整x轴刻度标签
plt.savefig('./pic/demo3.1.png', dpi=400, bbox_inches='tight')
# 绘制直方图
fig, (ax2, ax3) = plt.subplots(nrows=2)  # 创建一个窗口，同时创建两个子图
sigma = 1  # 标准差
avg = 0  # 均值
x = avg + sigma * np.random.randn(10000)  # 正态分布随机数
ax2.hist(x, bins=40, density=False, histtype='bar', )  # bins柱子个数，'auto'自动设定，默认为10；normed是否归一化；histtype直方图
ax3.hist(x, bins='auto', density=True, histtype='bar', facecolor='yellowgreen', alpha=0.8, cumulative=True,
         rwidth=0.8)  # cumulative是否计算累加分布，rwidth柱子宽度
plt.savefig('./pic/demo3.2.png', dpi=400, bbox_inches='tight')
# 绘制气泡图-散点图
fig2 = plt.figure()  # 新建画板
ax4 = fig2.add_subplot(1, 2, 1)  # 新建子图
ax5 = fig2.add_subplot(1, 2, 2)  # 新建子图
x4 = np.random.random(100)  # 产生随机数据
y4 = np.random.random(100)
# 气泡图
ax4.scatter(x4, y4, s=x * 1000, c='g', marker='o', alpha=0.6, lw=1)  # s:图像大小，c:颜色，marker：图片，lw：图片宽度
# 散点图
ax5.scatter(x4, y4, c='g', marker='o', alpha=0.6, lw=1)  # s:图像大小，c:颜色，marker：图片，lw：图片宽度
plt.savefig('./pic/demo3.3.png', dpi=400, bbox_inches='tight')
# 显示画板
plt.show()
