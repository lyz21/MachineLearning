# encoding=utf-8
"""
@Time : 2020/6/16 20:32 
@Author : LiuYanZhe
@File : test1.py.py 
@Software: PyCharm
@Description: 测试opencv，滤波和阈值
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np

# 读取，0、1、-1分别代表灰度图、彩图、包含透明通道的彩图
pic = cv2.imread('1.jpg', 0)
print(pic)
# 先定义窗口，再显示图片
cv2.namedWindow('win1', cv2.WINDOW_FREERATIO)
# 显示图片
cv2.imshow('win1', pic)
cv2.waitKey(1000)  # 0不自动退出
# 均值滤波,卷积核大小3*3
# blur = cv2.blur(pic, (3, 3))
# cv2.imshow('win1', blur)
# cv2.waitKey(0)
# 高斯滤波,cv2.GaussianBlur(src,ksize,sigmaX) ,指定的高斯核的宽和高必须为奇数
gaussian = cv2.GaussianBlur(pic, (5, 5), 1)  # 高斯滤波
cv2.imshow('win1', gaussian)
cv2.waitKey(1000)
# 中值滤波
# median = cv2.medianBlur(pic, 5)  # 中值滤波
# cv2.imshow('win1', median)
# cv2.waitKey(0)
cv2.destroyAllWindows()

print('-' * 10)
fig, axs = plt.subplots(2, 2)
plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
# 固定阈值(要处理的原图一般是灰度图,设定的阈值,最大阈值一般为255,阈值的方式主要有5种)
ret, th1 = cv2.threshold(gaussian, 130, 255, cv2.THRESH_BINARY)
print('ret:', ret)
print('th1:', th1)
ax1 = axs[0, 0]
ax1.imshow(th1, 'gray')
ax1.set_title('固定阈值')
ax1.set_xticks([]), ax1.set_yticks([])  # 隐藏坐标轴
# 自适应阈值
th2 = cv2.adaptiveThreshold(gaussian, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
ax2 = axs[0, 1]
print('th2:', th2)
ax2.imshow(th2, 'gray')
ax2.set_title('自适应阈值')
ax2.set_xticks([]), ax2.set_yticks([])  # 隐藏坐标轴

# 两个相乘
th3 = np.array(np.array(th1) + np.array(th2))
print('th3:', th3)
ax3 = axs[1, 0]
ax3.imshow(th3, 'gray')
ax3.set_title('改动前')
th3[th3 != 0] = 255
print('th3:', th3)
ax4 = axs[1, 1]
ax4.imshow(th3, 'gray')
ax4.set_title('改动后')
plt.xticks([]), plt.yticks([])  # 隐藏坐标轴
plt.show()

