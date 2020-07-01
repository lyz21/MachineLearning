# encoding=utf-8
"""
@Time : 2020/1/10 16:42 
@Author : LiuYanZhe
@File : demo2.py
@Software: PyCharm
@Description: 极坐标系
"""
import numpy as np
import matplotlib.pyplot as plt

# 数据
x1 = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
x2 = np.arange(0, 2 * np.pi, 0.02)
print('x2:', x2)

# 创建画布
fig = plt.figure(figsize=(8, 7))    # 创建一个画板，设定大小，后期添加子图
fig.subplots_adjust(top=0.95, bottom=0.05)  # 设置画板
# 添加子图
ax1 = fig.add_subplot(2, 2, 1)  # 添加一个子图，将画板分成1行5列，该子图为第1个,直角坐标系
ax2 = fig.add_subplot(2, 2, 2, polar=True)  # 添加一个子图，横1纵3，第2个,极坐标系
ax3 = fig.add_subplot(2, 2, 3, polar=True)  # 添加一个子图，横1纵3，第3个,极坐标系
ax4 = fig.add_subplot(2, 2, 4, polar=True)  # 添加一个子图，横1纵3，第3个,极坐标系
# 绘制
ax1.plot(x1, np.sin(x1))
ax1.plot(x1, np.cos(x1))
ax2.plot(x2, np.ones_like(x2))  # np.ones_like()函数返回1，类型和输入值类型相同
ax2.plot(x2, x2 / 6, linestyle='--', lw=1.5)  # lw为线宽
ax3.plot(x2, np.sin(x2), color='b', alpha=0.7, linestyle='-.')
ax3.plot(x2, np.cos(x2), color='g', linestyle=':')
ax4.plot(x2, np.cos(4 * x2))
ax4.plot(x2, np.cos(5 * x2), linestyle='--')
# 设置子图
ax4.set_rgrids(np.arange(0.1, 2, 0.4), angle=45)  # 设置网格
# ax4.set_yticks(np.arange(0.1, 2, 0.4))  # 与上面效果相同
# 保存图像
plt.savefig('./pic/demo2.png', dpi=400, bbox_inches='tight')
# 显示画布
plt.show()
