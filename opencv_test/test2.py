# encoding=utf-8
"""
@Time : 2020/6/17 17:03 
@Author : LiuYanZhe
@File : test2.py 
@Software: PyCharm
@Description: 使用k-means对图像分割
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np


def seg_kmeans_gray():
    # 读取图片
    img = cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)

    # 展平
    img_flat = img.reshape((img.shape[0] * img.shape[1], 1))
    img_flat = np.float32(img_flat)

    # 迭代参数
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 20, 0.5)
    flags = cv2.KMEANS_RANDOM_CENTERS

    # 进行聚类，cv2.kmeans(数据data, 分类数k, 预设的标签bestLabels, 迭代停止的模式选择criteria, 重复试验kmeans算法次数attempts, 初始中心选择flags)
    compactness, labels, centers = cv2.kmeans(img_flat, 2, None, criteria, 30, flags)

    # 显示结果
    img_output = labels.reshape((img.shape[0], img.shape[1]))
    plt.subplot(121), plt.imshow(img, 'gray'), plt.title('input')
    plt.subplot(122), plt.imshow(img_output, 'gray'), plt.title('kmeans')
    plt.show()


if __name__ == '__main__':
    seg_kmeans_gray()