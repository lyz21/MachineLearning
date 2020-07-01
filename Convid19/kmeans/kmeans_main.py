# encoding=utf-8
"""
@Time : 2020/4/2 19:53 
@Author : LiuYanZhe
@File : kmeans_main.py 
@Software: PyCharm
@Description: 
"""
import pandas as pd
from Convid19.kmeans import kmeansUtil
import jieba


# cav_path里面的数据为1维['day1.info','day2.info']，n_clusters为划分种类个数
def get_kmeans_news(csv_path='../data/RenMIn_top_2020_03_30.csv', n_clusters=2):
    contens_list = pd.read_csv(csv_path).iloc[:, 1].values.tolist()  # 加载的新闻
    c_data_list = kmeansUtil.getKmeans(contens_list, n_clusters=n_clusters, name='RenMinNews')
    return c_data_list


# cav_path里面的数据为2维['day1.info','day2.info'],n_clusters为划分种类个数
def get_kmeans_title(csv_path='../data/RenMinTitle_all_2020_04_06.csv', n_clusters=2):
    contens0_list = pd.read_csv(csv_path).iloc[:, :30].values.tolist()  # 加载的标题
    contens_list = []
    for content_list in contens0_list:
        content_list = ' '.join(content_list)
        list1 = ' '.join(jieba.cut(content_list, cut_all=False))
        print('jieba：', list1)
        # list1 = jieba.cut(content_list, cut_all=True)
        # list1 = jieba.cut_for_search(content_list)
        contens_list.append(list1)
    print('contens_list:',contens_list)

    c_data_list = kmeansUtil.getKmeans(contens_list, n_clusters, name='RenMinTitle')
    return c_data_list


if __name__ == '__main__':
    n_clusters = 3
    # c_data_list = get_kmeans_news(n_clusters=n_clusters)
    c_data_list = get_kmeans_title(n_clusters=n_clusters)
    print(c_data_list)
    # for i in range(n_clusters):
    #     print(c_data_list[i])
