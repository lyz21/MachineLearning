# encoding=utf-8
"""
@Time : 2020/3/27 21:55 
@Author : LiuYanZhe
@File : test.py 
@Software: PyCharm
@Description: 
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# df1 = pd.DataFrame([{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'c': 6}])
# df2 = pd.DataFrame([{'a': 10, 'b': 20, 'c': 30}, {'a': 40, 'b': 50}])
# print(df1)
# print(df2)
# # axis=0或1是按行合并还是按列合并，axis=0，列不变，行增多
# df3 = pd.concat([df1, df2], axis=0)
# df4 = pd.concat([df1, df2], axis=1)
# print(df3)
# print(df4)

# data = pd.read_csv('China_province_2020_03_27.csv')
# province_dict = {num: name for num, name in zip(data['id'], data['name'])}
# print(province_dict)
fig = plt.figure()
data = np.array([[1, 2, 3], [4, 5, 6]])
ax = fig.add_subplot(1, 1, 1)
lable = ['10', '20', '30']
lablei = [10, 20, 30]
# 解决ticklabel字重叠：
# ax = sns.countplot(x="downNetwork", data=offline_data_shuffle)
# ax.set_xlim([1, 2])
# ax.set_xticks(range(1, 4), lablei)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_xticks(np.linspace(1, 3, 3))
ax.set_xticklabels(('10', '20', '30'))

# plt.xticks(range(1, len(lable)+1), ['10', '20', '30'])
ax.boxplot(data)
plt.show()
