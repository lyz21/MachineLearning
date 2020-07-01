# encoding=utf-8
"""
@Time : 2020/3/31 11:16 
@Author : LiuYanZhe
@File : RenMin_title.py 
@Software: PyCharm
@Description: 按天（每天标题）生成人民日报词汇连接矩阵，用来绘制无向网络图
"""
import pandas as pd
from textrank4zh import TextRank4Keyword
import numpy as np
from Convid19.netpic import netUtil

# 每天最多的关键词个数
max_num = 8

# pd显示所有行、列
pd.set_option('display.max_rows', None)  # 行
pd.set_option('display.max_columns', None)  # 列

# 加载需要的keyword
# keyword = pd.read_csv('../data/keyword_title.csv')['word'].values.tolist()
keyword = pd.read_csv('../data/RenMin_keyWords_data_2020_03_29.csv')['word'].values.tolist()
# 加载title
data_arr = pd.read_csv('../data/RenMinTitle_all_2020_03_30.csv').iloc[:, :30].values
# 每天化为1条，转为1维数据
data_list = []
for arr in data_arr:
    data_list.append(' '.join(arr))
# 生成日期列表
date_list = netUtil.getDateList(len(data_list))
# 构建二维矩阵，按天存储关键词
keywords_allday_list = []
# 存储所有的关键词，用来构建连接矩阵
keywords_all_set = set()
# 获取每天的关键词
for day_title in data_list:
    day_keywords_list = []
    words = TextRank4Keyword()
    words.analyze(text=day_title, lower=True, window=3)
    keywords_dic_list = words.get_keywords(20, word_min_len=2)
    for one_dic in keywords_dic_list:
        if one_dic['word'] in keyword:
            day_keywords_list.append(one_dic['word'])
            keywords_all_set.add(one_dic['word'])
            if len(day_keywords_list) >= max_num:
                break
    keywords_allday_list.append(day_keywords_list)
# print(keywords_allday_list)
# print(keywords_all_set)
# 构建连接矩阵
keyword_matrix = pd.DataFrame(np.zeros((len(keywords_all_set), len(keywords_all_set))), columns=keywords_all_set,
                              index=keywords_all_set)
# 为连接矩阵赋值
for day_list in keywords_allday_list:
    for i in range(len(day_list) - 1):
        for j in range(i + 1, len(day_list)):
            keyword_matrix[day_list[i]][day_list[j]] += 1
keyword_matrix.to_csv('./netdata/keyword_matrix.csv')
print('完成')
# print(keyword_matrix)
# 绘制
netUtil.draw(csv_path='./netdata/keyword_matrix.csv', pic_path='../pic/network_title.png')
