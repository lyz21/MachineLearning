# encoding=utf-8
"""
@Time : 2020/3/31 10:51 
@Author : LiuYanZhe
@File : everyContentNoUse.py 
@Software: PyCharm
@Description: 目的是找出每天的关键字，进行连续性分析，结果不够好，弃用
"""
import pandas as pd
import numpy as np
from textrank4zh import TextRank4Keyword
from snownlp import SnowNLP


# 生成日期方法
def getDateList(day_num, start_month=1, start_day=1):
    month, day = start_month, start_day
    date_list = []
    for i in range(day_num):
        if day >= 31:  # 1月结束，到第2月,1.31没有
            month += 1
            day = 1
        if day < 10:
            day_str = '0' + str(day)
        else:
            day_str = str(day)
        if month < 10:
            month_str = '0' + str(month)
        else:
            month_str = str(month)
        date = month_str + '.' + day_str
        date_list.append(date)
        day += 1
    return date_list


# stopwords = ['主席', '习近平', '国家', '发表', '启示', '迈向', '收获', '举行', '只争朝夕', '温暖', '万众一心','']
stopwords = pd.read_csv('data/notKeywords.csv').columns.tolist()
data_pd = pd.read_csv('data/RenMInTitle_2020_03_29.csv')  # 加载的标题
date_list = getDateList(50)
# data_list = data_pd.iloc[:, 1:].values.flatten().tolist()
data_list = data_pd.iloc[:, :].values.tolist()

word_list = []
i = 0
for days_title in data_list:
    print('-' * 10)
    day_list_temp = []
    for title in days_title:
        print('+' * 10)
        print(title)
        if title == '空' or title == '广告':
            continue
        words = TextRank4Keyword()
        words.analyze(text=title, lower=True, window=3)
        keywords_list = words.get_keywords(num=10, word_min_len=2)
        if len(keywords_list) == 0:
            continue
        for item in keywords_list:
            if item['word'] not in stopwords:
                day_list_temp.append(item['word'])
                break
    word_list.append([date_list[i], day_list_temp])
    # word_list.append(day_list_temp)
    i += 1
    if i == 10:
        break
print(word_list)
print(word_list[0])
print(word_list[1])
#     keywords_list = words.get_keywords(10, word_min_len=2)
#     if len(keywords_list) != 0:
#         temp_list += keywords_list
# keyWord_weight_list.append(temp_list)
# i += 1
# if i == 10:
#     break

# print(keyWord_weight_list)
# for item in keyWord_weight_list:
#     words = TextRank4Keyword()
#     words.analyze(text=item, lower=True, window=3)
#     keywords_list = words.get_keywords(10, word_min_len=2)
#     print(item)
#     print(keywords_list)

#     for keywords in keywords_list:
#         dic_keyWord_weight.setdefault(keywords.word, 0)
#         dic_keyWord_weight[keywords.word] += keywords.weight * 40  # 按权重统计
#         # dic_keyWord_weight[keywords.word] += 1  # 按词频统计
# 对字典排序
