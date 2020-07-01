# encoding=utf-8
"""
@Time : 2020/1/14 16:41 
@Author : LiuYanZhe
@File : way_plt.py 
@Software: PyCharm
@Description: 图形化表示路线
"""
import numpy as np
import matplotlib.pyplot as plt



class DrawWay:
    def __init__(self, data):
        # 创建画板
        self.ax = plt.subplot(1, 1, 1)  # 创建一个画板同时传建一个子图
        self.data = data

    def drawPoint(self):
        # 绘制点
        for i in range(len(self.data)):
            self.ax.scatter(self.data[i][0], self.data[i][1])  # 绘制各个点

    def update(self, best_path):
        self.ax.cla()  # 清空画面
        # 画点
        self.drawPoint()
        # 画线
        x_arr = []  # 存储路线的x坐标
        y_arr = []  # 存储路线的x坐标
        for i in range(len(best_path)):
            x_arr.append(self.data[best_path[i]][0])
            y_arr.append(self.data[best_path[i]][1])
        x_arr.append(self.data[best_path[0]][0])
        y_arr.append(self.data[best_path[0]][1])
        self.ax.plot(x_arr, y_arr)  # 绘制路线
        plt.pause(0.001)
    def drawFinal(self,best_path):
        self.ax.cla()  # 清空画面
        # 画点
        self.drawPoint()
        # 画线
        x_arr = []  # 存储路线的x坐标
        y_arr = []  # 存储路线的x坐标
        for i in range(len(best_path)):
            x_arr.append(self.data[best_path[i]][0])
            y_arr.append(self.data[best_path[i]][1])
        x_arr.append(self.data[best_path[0]][0])
        y_arr.append(self.data[best_path[0]][1])
        self.ax.plot(x_arr, y_arr)  # 绘制路线
        # 显示画板
        plt.show()
# data = np.loadtxt('citys_LOCATION.txt')
# best_path=[0]
# # # print(data)
# drawway(data,best_path)
