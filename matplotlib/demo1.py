# encoding=utf-8
"""
@Time : 2020/1/9 17:15 
@Author : LiuYanZhe
@File : demo1.py 
@Software: PyCharm
@Description: 直线坐标系
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# 数据
x = np.arange(-10, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.power(x, 2)
y4 = np.power(x, 3)

# 创建画布
fig, ax_arr = plt.subplots(2, 1)  # 同时创建一个窗口和2个子图
# 创建子图
ax1 = ax_arr[0]
ax2 = ax_arr[1]
axes = plt.axes([0.2, 0.3, 0.1, 0.1], facecolor='y')  # 添加子图，不挤压原图空间，覆盖在原图之上
# 画布设置
# fig=plt.gcf()   # 获取当前figure
# fig.set_size_inches(5, 6)   # 设置画布大小
fig.subplots_adjust(hspace=0.3, top=0.95)  # 子图之间保留的宽度，与顶部保持的宽度
# 子图设置
ax1.set_title('sin/cos')  # 设置标题
ax2.set_title('x^2/x^3')
ax1.set_xlim(-5, 5)  # 设置横纵坐标范围
ax1.set_ylim(-1, 1)
ax2.set_xlim(-3, 3)
ax2.set_ylim(0, 9)
xmajorLocator = MultipleLocator(2)  # 设置坐标显示格式，刻度差为2的倍数
ax2.xaxis.set_major_locator(xmajorLocator)
ax1.grid(b=True, which='major', axis='both', alpha=0.5,
         color='skyblue', linestyle='--', linewidth=1)  # 绘制网格 参数:which=major(绘制大刻度)/minor(小刻度)/both,axis=x/y/both
ax2.xaxis.grid(True, which='major')  # 设置网格-xy单独设置
ax2.yaxis.grid(True, which='major')
ax1.set_xticks([])  # 手动设置坐标轴刻度（无刻度）
ax1.set_xticks([-5, -2.5, 0, 2.5, 5])  # 手动设置坐标轴刻度（无刻度）
# ax2.set_xticklabels(labels=['', 'x1', 'x2', 'x3', 'x4'], rotation=-30, fontsize='small')  # 设置坐标轴显示文本，倾斜角度，字体
# ax1.legend(loc='legned_lyz')    # 显示图例
ax1.text(-0.6, 0.1, 'y=sin(x)')  # 指定位置显示文本
ax1.text(-2, 0.6, 'y=cos(x)')
ax2.annotate('import point (2,4)', xy=(2, 4), xytext=(-1, 7),
             arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）

# 在子图中绘制图像
ax1.plot(x, y1)
ax1.plot(x, y2, linestyle='--', color='r', label='line')  # 绘制点图并设置格式
ax2.plot(x, y3, marker='.', alpha=0.5, color='g', label='point')
axes.plot(x, y4)
# 保存图像
plt.savefig('./pic/demo1.png', dpi=400, bbox_inches='tight')
# 显示画布
plt.show()
