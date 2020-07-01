# encoding=utf-8
"""
@Time : 2020/6/17 17:41 
@Author : LiuYanZhe
@File : util.py 
@Software: PyCharm
@Description: 图像处理工具类
"""
import numpy as np


# 取两个图像的交集
def intersection(pic1, pic2):
    th3 = np.array(np.array(pic1) + np.array(pic2))
    th3[th3 != 0] = 255
    return th3


# 取两个图像的并集
def union(pic1, pic2):
    th3 = np.array(np.array(pic1) * np.array(pic2))
    th3[th3 != 0] = 255
    return th3


# 以f1为底，去除三个图像中共同存在的黑色,黑色为0，三个相加为0则同为黑，删
def del_uni_b(f1, f2, f3):
    f1, f2, f3 = np.array(f1), np.array(f2), np.array(f3)
    f = f1 + f2 + f3
    index = f == 0
    f1[index] = 255
    return f1
