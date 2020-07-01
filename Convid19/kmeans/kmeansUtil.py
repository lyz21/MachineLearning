# encoding=utf-8
"""
@Time : 2020/4/2 19:45
@Author : LiuYanZhe
@File : kmeansUtil.py
@Software: PyCharm
@Description: k-means工具类
"""
from random import randint

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from Convid19 import dateUtil


# 字体颜色方法(黑色)
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # h = randint(0, 50)
    h = 0  # 色域
    # s = randint(0, 20)
    # l = randint(0, 20)
    flag = randint(0, 1)
    if flag == 0:
        s = int(100.0 * float(randint(0, 200)) / 255.0)  # 饱和度
        l = int(100.0 * float(randint(0, 10)) / 255.0)  # 明亮度
    else:
        s = int(100.0 * float(randint(0, 10)) / 255.0)
        l = int(100.0 * float(randint(0, 230)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)


# kmeans方法 参数contenst为一维矩阵，['day1.info','day2.info'...]
def getKmeans(contens_list, n_clusters=2, name='k_means'):
    date_list = dateUtil.getDateList(len(contens_list))  # 生成日期列表备用
    c_data_list = []  # 将划分后的日期分类保存
    data = pd.DataFrame(contens_list)
    # 构建语料库，计算文档的TF-IDF矩阵
    transformer = TfidfVectorizer()
    tfidt = transformer.fit_transform(contens_list)
    # TF-IDF以稀疏矩阵的形式存储，将TF-IDF转化为数组形式，文档-词矩阵
    word_vectors = tfidt.toarray()
    print('word_vectors:\n', word_vectors)

    # 对word_vectors进行k均值聚类      参数聚类数目n_clusters，随机种子random_state = 0。
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(word_vectors)
    # 聚类得到的类别
    labels_list = kmeans.labels_
    kmean_labels = data
    kmean_labels['cluster'] = labels_list
    # print('kmean_labels.head(10):\n', kmean_labels.head(50))
    # 汇总分类后的日期
    for i in range(n_clusters):
        temp_list = []  # 暂存第i类日期
        for j in range(len(labels_list)):
            if labels_list[j] == i:
                temp_list.append(date_list[j])
        c_data_list.append(temp_list)
    DrawImShow2(labels_list)
    '''MDS降维'''
    # 使用MDS对数据进行降维
    mds = MDS(n_components=2, random_state=12)
    mds_results = mds.fit_transform(word_vectors)
    # print('mds_results.shape:\n', mds_results.shape)
    # print('mds_results:\n', mds_results)
    # 绘制降维后的结果
    plt.figure()
    plt.scatter(mds_results[:, 0], mds_results[:, 1], c=kmean_labels.cluster)
    for i in (np.arange(len(contens_list))):
        plt.text(mds_results[i, 0] + 0.02, mds_results[i, 1], date_list[i])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("K-means MDS")
    plt.savefig('../pic/k-mans_' + name + '_MDS.png', dpi=400, bbox_inches='tight')
    plt.show()

    '''PCA降维'''
    pca = PCA(n_components=2)
    pca.fit(word_vectors)
    # print('pca.explained_variance_ratio_:', pca.explained_variance_ratio_)
    pca_results = pca.fit_transform(word_vectors)
    # print('pca_results.shape:', pca_results.shape)
    # 绘制降维后的结果
    plt.figure()
    plt.scatter(pca_results[:, 0], pca_results[:, 1], c=kmean_labels.cluster)
    for i in (np.arange(len(contens_list))):
        plt.text(pca_results[i, 0] + 0.01, pca_results[i, 1], date_list[i], fontsize=5)
    plt.xlabel('principal component A')
    plt.ylabel('principal component B')
    plt.title("K-means PCA")
    plt.savefig('../pic/k-mans_' + name + '_PCA.png', dpi=400, bbox_inches='tight')
    plt.show()

    return labels_list


# 将日期划分后的绘制成网格
def DrawImShow2(div_data):
    # div_data = [0,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
    #             0,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,
    #             1,1,1,1,1,1,1,0,1,1,1,1,1,1]  # 长度为88
    div_arr = np.array(div_data).reshape((8, 11))
    date_list = dateUtil.getDateList(len(div_data), con_str='.')
    # for i in range(8):
    #     sub = 11 * i
    #     date = date_list[sub]
    #     # 设定颜色
    #     if div_data[sub] == 1:
    #         color = 'white'
    #     else:
    #         color = '#08306B'
    #     plt.text(-0.45, i+0.07, date, color=color)
    # plt.text(3-0.4, 2.07, '1.26', color='white')
    # plt.text(2-0.4, 4.07, '2.16', color='white')
    for i in range(len(div_data)):
        x = i % 11 - 0.35
        y = int(i / 11) + 0.07
        date = date_list[i]
        # 设定颜色
        if div_data[i] == 1:
            color = 'white'
        else:
            color = '#08306B'
        plt.text(x, y, date, color=color, fontsize=8)
    plt.xticks([])
    plt.yticks([])
    # 画分割线，纵线
    for i in np.arange(0.5, 9.6, 1):
        plt.plot([i, i], [-0.5, 7.5], color='black')
    for i in np.arange(0.5, 7.6, 1):
        plt.plot([-0.5, 10.5], [i, i], color='black')  ##08306B
    # 画标注线
    # lw = 1.5
    # alpha = 1
    # deviation = 0
    # plt.plot([2.5, 10.5], [1.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 10.5], [2.5 - deviation, 2.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 10.5], [3.5 - deviation, 3.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, 2.5], [4.5 - deviation, 4.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([-0.5, -0.5], [4.5 - deviation, 2.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([2.5, 2.5], [4.5 - deviation, 3.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([2.5, 2.5], [2.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    # plt.plot([10.5, 10.5], [3.5 - deviation, 1.5 - deviation], color='red', alpha=alpha, lw=lw)
    plt.imshow(div_arr, cmap='Blues', interpolation='none', vmin=0, vmax=1, aspect='equal')
    plt.savefig('../pic/kmeans_time.png', dpi=400, bbox_inches='tight')
    plt.show()


# 将日期划分后的绘制成网格
def DrawImShow3(div_data):
    div_arr = np.array(div_data).reshape((8, 11))
    date_list = dateUtil.getDateList(len(div_data), con_str='.')
    for i in range(len(div_data)):
        x = i % 11 - 0.35
        y = int(i / 11) + 0.07
        date = date_list[i]
        # 设定颜色
        if div_data[i] == 1:
            color = 'white'
        elif div_data[i] == 0:
            color = '#08306B'
        else:
            color = 'white'
        plt.text(x, y, date, color=color, fontsize=8)
    # 画分割线，纵线
    for i in np.arange(0.5, 9.6, 1):
        plt.plot([i, i], [-0.5, 7.5], color='black')
    for i in np.arange(0.5, 7.6, 1):
        plt.plot([-0.5, 10.5], [i, i], color='black')  ##08306B
    plt.xticks([])
    plt.yticks([])
    plt.imshow(div_arr, cmap='Blues', interpolation='none')
    plt.savefig('../pic/kmeans_time_3.png', dpi=400, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    div_data = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                0, 0,
                0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 长度为88
    DrawImShow3(div_data)
