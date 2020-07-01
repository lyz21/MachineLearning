# encoding=utf-8
"""
@Time : 2020/6/17 17:13 
@Author : LiuYanZhe
@File : test3.py 
@Software: PyCharm
@Description: 
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from opencv_test import util


# 读取图片
def load_pic(path=0):
    if path == 0:
        path = '1.jpg'
    # 读取图片
    img = cv2.imread(path)
    return img


# 提取梯度
def get_grad(fig):
    # 提取梯度
    gradX = cv2.Sobel(fig, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(fig, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    return gradient


# 获得图形形态学
def fig_phology(fig):
    # 返回指定形状和尺寸的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (25, 25))
    # 形态学变化
    closed = cv2.morphologyEx(fig, cv2.MORPH_CLOSE, kernel)
    return closed


# 寻找需截取的区域,返回带边框的图像，和截取后的图像
def find_area(img, closed):
    (cnts, _) = cv2.findContours(
        # 参数一： 二值化图像
        closed.copy(),
        # 参数二：轮廓类型
        cv2.RETR_EXTERNAL,  # 表示只检测外轮廓
        # cv2.RETR_CCOMP,                #建立两个等级的轮廓,上一层是边界
        # cv2.RETR_LIST,                 #检测的轮廓不建立等级关系
        # cv2.RETR_TREE,                 #建立一个等级树结构的轮廓
        # cv2.CHAIN_APPROX_NONE,         #存储所有的轮廓点，相邻的两个点的像素位置差不超过1
        # 参数三：处理近似方法
        # cv2.CHAIN_APPROX_SIMPLE  # 例如一个矩形轮廓只需4个点来保存轮廓信息
        cv2.CHAIN_APPROX_TC89_L1,
        # cv2.CHAIN_APPROX_TC89_KCOS
    )
    # 画出轮廓
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    # 计算最大轮廓的旋转包围盒
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    # 画边框
    frame = cv2.drawContours(img.copy(), [box], -1, (0, 0, 255), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    crop_img = img[y1:y1 + hight, x1:x1 + width]
    return frame, crop_img


# 裁剪图像
def crop_fig(img, threshold=10):
    # 转换灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 去噪声
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    # 提取梯度
    gradient = get_grad(blurred)
    # cv2.imshow('gradient', gradient)
    # 去噪声
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)  # 高斯滤波
    # 固定阈值切割
    (ret, thresh) = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    # cv2.imshow('l', thresh)
    # 图形形态学
    closed = fig_phology(thresh)
    # 执行4次形态学腐蚀与膨胀
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    # cv2.imshow('closed', closed)
    # 找出区域
    frame, crop_fig = find_area(img, closed)
    return frame, crop_fig


# k-means聚类分割算法
def k_means_fig(img):
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
    print('img_output:', img_output)
    # plt.subplot(121), plt.imshow(img, 'gray'), plt.title('input')
    # plt.subplot(122), plt.imshow(img_output, 'gray'), plt.title('kmeans')
    # plt.show()
    return img_output


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    # 加载图片
    img = load_pic('1.jpg')
    figure = plt.figure(figsize=(6, 5))
    figure.add_subplot(2, 2, 1)
    plt.imshow(img, 'gray'), plt.title('原图')
    # 裁剪图片
    frame, fig = crop_fig(img, threshold=10)
    # cv2.imshow('frame', frame)
    figure.add_subplot(2, 2, 2)
    plt.imshow(frame, 'gray'), plt.title('最大轮廓旋转包围盒')
    figure.add_subplot(2, 2, 3)
    plt.imshow(fig, 'gray'), plt.title('裁剪图像')
    plt.savefig('pic.png', dpi=400, bbox_inches='tight')
    # cv2.imshow('crop_fig', fig)
    # 试用切割好的图片再做分割
    # 转换灰度
    gray = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
    # 去噪声
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    # 提取梯度
    # gradient = get_grad(blurred)
    # 去噪声
    blurred = cv2.GaussianBlur(blurred, (9, 9), 0)  # 高斯滤波
    # 固定阈值切割
    (ret, thresh) = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    # 自适应阈值
    adth = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
    # k-means分割
    k_fig = k_means_fig(blurred)

    print('thresh:', thresh)
    # cv2.imshow('thresh', thresh)
    cv2.imwrite('thresh.png', thresh)
    # cv2.imshow('adth', adth)
    cv2.imwrite('adth.png', adth)
    fig = util.del_uni_b(adth, thresh, k_fig)
    # cv2.imshow('fig', fig)
    cv2.imwrite('fig.png', fig)
    cv2.waitKey(0)  # 0不自动退出
    # 绘制
    figure = plt.figure(figsize=(8, 6))
    plt.subplot(231)
    plt.imshow(gray, 'gray')
    plt.title('原图')
    plt.subplot(232)
    plt.imshow(blurred, 'gray')
    plt.title('预处理图')
    plt.subplot(233)
    plt.imshow(thresh, 'gray')
    plt.title('固定阈值')
    plt.subplot(234)
    plt.imshow(adth, 'gray')
    plt.title('自适应阈值')
    plt.subplot(235)
    plt.imshow(k_fig, 'gray')
    plt.title('k-means分割')
    plt.subplot(236)
    plt.imshow(fig, 'gray')
    plt.title('最终图')
    # plt.show()
    plt.savefig('fig.png', dpi=400, bbox_inches='tight')
    # 最终对比图
    figure = plt.figure()
    figure.add_subplot(1, 2, 1)
    plt.imshow(img, 'gray'), plt.title('原图')
    plt.xticks([])
    plt.yticks([])
    figure.add_subplot(1, 2, 2)
    plt.imshow(fig, 'gray'), plt.title('结果')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('contrast.png', dpi=400, bbox_inches='tight')

    # a, b = find_area(frame, fig)
    # cv2.imshow('a',a)
    # cv2.imshow('b',b)
    # cv2.waitKey(0)  # 0不自动退出