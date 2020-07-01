# encoding=utf-8
"""
@Time : 2020/3/29 14:57 
@Author : LiuYanZhe
@File : testNp.py 
@Software: PyCharm
@Description: 
"""
from random import randint

import numpy as np
import pandas as pd

# arr = np.empty((2))
# np.append(arr, [2,2])
# print(arr)

# a = ['1', '2', '3', '1']
# # a.remove('1')
# a = list(set(a))
# print(a)
#
# contens1_arr = pd.read_csv('data/RenMInTitle_2020_03_29.csv')
# contens1_arr = contens1_arr[~contens1_arr['0'].isin(['无'])]
# print(contens1_arr)

# arr=np.array(['1','2'])
# np.delete(arr,['1'])
# print(arr)

# dic = {'1': 1, '2': 2,'3': 2}
# for item in ['1', '2']:
#     dic.pop(item)
# print(dic)

# a = randint(0, 1)
# print(a)

# 连接dic
# dic1 = {'1': 1, '2': 2, '3': 3}
# dic2 = {'4': 4, '5': 5}
# dic = dict(dic1, **dic2)
# print(dic)
#
# dic1 = {'1': 1, '2': 2, '3': 3}
# if dic1.keys() in ['1', '2']:
#     print(dic1)
#
# str1 = ' a b   c '
# str1=str1.replace(' ','')
# print(str1)

# list1 = [[1, 2, 3], ['a', 'b', 'c']]
#
# print(list1[1][1])

# stopwords = pd.read_csv('../data/notKeywords.csv').columns.tolist()
# print('stopwords:', type(stopwords))
# print('stopwords:', stopwords)

# keyword = pd.read_csv('../data/keyword_title.csv')['word'].values.tolist()
# print(keyword)

# key = set()
# key.add('1')
# key.add('2')
# key.add('1')
# print(key)

list1 = [['1', '2', '3'], ['a', 'b', 'c'], ['m', 'n', 'q']]
list2 = list1[:2]
print(list2)
