# encoding=utf-8
"""
@Time : 2020/1/11 15:18 
@Author : LiuYanZhe
@File : demo5.py 
@Software: PyCharm
@Description: 3D图
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 数据
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
# 生成网格数据
X, Y = np.meshgrid(X, Y)
# 计算每个点对的长度
R = np.sqrt(X ** 2 + Y ** 2)
Z = np.sin(R)
'''sin()'''
# 创建画板
fig = plt.figure()
# 创建子图
ax = Axes3D(fig)
# 画3d图
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hot)  # rstride：行之间的跨度；cstride：列之间的跨度；camp：颜色映射表
# 设置Z轴维度（区间范围）
ax.set_zlim(-2, 2)
# 保存图像
plt.savefig('./pic/demo5.1.png', dpi=400, bbox_inches='tight')
'''cos()'''
# 创建画板
fig2 = plt.figure()
# 创建3d子图
ax2 = Axes3D(fig2)
# 画图
ax2.plot_surface(X, Y, np.cos(R), rstride=1, cstride=1, cmap=plt.cm.coolwarm)  # 画3d图
ax2.contourf(X, Y, Z, zdir='z', offset=-2)  # 曲面到底部的投影，zdir：投影到哪个面（x/y/z）;offset:表示投影到z=-2
# 设置Z轴维度（区间范围）
ax2.set_zlim(-2, 2)
# 保存图像
plt.savefig('./pic/demo5.2.png', dpi=400, bbox_inches='tight')
# 显示图像
plt.show()
