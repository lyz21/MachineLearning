# encoding=utf-8
"""
@Time : 2020/4/3 15:03 
@Author : LiuYanZhe
@File : getKeyWords.py 
@Software: PyCharm
@Description: 获取关键词
"""

import pandas as pd
from textrank4zh import TextRank4Keyword


# 参数列表为每篇文章生成的最大词汇个数，数据读取起始行，结束行
def getKeyWordsBuNews(max_num=10, startColum=None, endColum=None):
    # 每天最多的关键词个数
    # max_num = 7

    # pd显示所有行、列
    pd.set_option('display.max_rows', None)  # 行
    pd.set_option('display.max_columns', None)  # 列

    # 加载需要的keyword
    keyword = pd.read_csv('../data/keyword_news.csv')['word'].values.tolist()
    # 加载news,一维
    data_list = pd.read_csv('../data/RenMIn_top_2020_03_30.csv').iloc[startColum:endColum, 1].values.flatten().tolist()
    print(data_list)
    # 生成日期列表
    # date_list = netUtil.getDateList(len(data_list))
    # 构建二维矩阵，按天存储关键词
    keywords_allday_list = []
    # 存储所有的关键词，用来构建连接矩阵
    keywords_all_set = set()
    # 获取每天的关键词
    for day_title in data_list:
        day_keywords_list = []
        words = TextRank4Keyword()
        words.analyze(text=day_title, lower=True, window=3)
        keywords_dic_list = words.get_keywords(40, word_min_len=2)
        for one_dic in keywords_dic_list:
            # 下面注释是为了挑选出名词
            # s_tags = SnowNLP(one_dic['word']).tags
            # print('---')
            # flag = 0
            # for tag in s_tags:
            #     if tag[1] == 'n':
            #         flag = 1
            #         print(tag)
            # if one_dic['word'] in keyword:
            #     if flag == 1:
            if one_dic['word'] in keyword:
                day_keywords_list.append(one_dic['word'])
                keywords_all_set.add(one_dic['word'])
                if len(day_keywords_list) >= max_num:
                    break
        keywords_allday_list.append(day_keywords_list)
    return keywords_allday_list


# 参数列表为每篇文章生成的最大词汇个数，数据读取起始行，结束行
def getKeyWordsByTitle(max_num=10, startColum=None, endColum=None):
    # 每天最多的关键词个数
    # max_num = 7

    # pd显示所有行、列
    pd.set_option('display.max_rows', None)  # 行
    pd.set_option('display.max_columns', None)  # 列
    # 加载需要的keyword
    keyword = pd.read_csv('../data/keyword_title.csv')['word'].values.tolist()
    # 加载title
    data_arr = pd.read_csv('../data/RenMinTitle_all_2020_04_06.csv').iloc[startColum:endColum, :30].values
    # 每天化为1条，转为1维数据
    data_list = []
    for arr in data_arr:
        data_list.append(' '.join(arr))
    print(data_list)
    # 生成日期列表
    # date_list = netUtil.getDateList(len(data_list))
    # 构建二维矩阵，按天存储关键词
    keywords_allday_list = []
    # 存储所有的关键词，用来构建连接矩阵
    keywords_all_set = set()
    # 获取每天的关键词
    for day_title in data_list:
        day_keywords_list = []
        words = TextRank4Keyword()
        words.analyze(text=day_title, lower=True, window=3)
        keywords_dic_list = words.get_keywords(40, word_min_len=2)
        for one_dic in keywords_dic_list:
            # 下面注释是为了挑选出名词
            # s_tags = SnowNLP(one_dic['word']).tags
            # print('---')
            # flag = 0
            # for tag in s_tags:
            #     if tag[1] == 'n':
            #         flag = 1
            #         print(tag)
            # if one_dic['word'] in keyword:
            #     if flag == 1:
            if one_dic['word'] in keyword:
                day_keywords_list.append(one_dic['word'])
                keywords_all_set.add(one_dic['word'])
                if len(day_keywords_list) >= max_num:
                    break
        keywords_allday_list.append(day_keywords_list)
    return keywords_allday_list
