# encoding=utf-8
"""
@Time : 2020/1/7 17:29 
@Author : LiuYanZhe
@File : libtest.py 
@Software: PyCharm
@Description: 
"""
import numpy as np
import matplotlib.pyplot as plt

# 产生数据
x = np.arange(-10, 11, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)
# =========创建子图，窗口（三种方法）=============
# 方法一：先创建窗口再创建子图
# fig = plt.figure(num=1, figsize=(15, 8), dpi=80)  # 创建一个窗口，设置大小，分辨率
# ax1 = fig.add_subplot(2, 1, 1)  # 通过fig添加子图，参数  行，列，第几个
# ax2 = fig.add_subplot(2, 1, 2)  # 通过fig添加子图，参数  行，列，第几个
# 方法二：一次性创建窗口和多个子图
fig, ax_arr = plt.subplots(4, 1)  # 创建一个窗口和四个子图
ax1 = ax_arr[0]
# ax2 = ax_arr[1]
# 方法三：一次创建一个窗口一个子图
# ax1=plt.subplot(1,1,1,facecolor='white')
# 设置子图基本元素
ax1.set_title('python-drawing')
ax1.set_xlabel('x-name')
ax1.set_ylabel('y-name')
# ax2.set_xlabel('x-name')
# ax2.set_ylabel('y-name')
# 绘制
ax1.plot(x, y1)
ax1.plot(x, y2)
# plot2 = ax2.plot(x, y)
# 显示图像
plt.show()
