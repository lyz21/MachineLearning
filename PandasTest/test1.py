# encoding=utf-8
"""
@Time : 2020/3/20 18:59 
@Author : LiuYanZhe
@File : test1.py 
@Software: PyCharm
@Description: pd使用
"""
import pandas as pd
import numpy as np

# 创建
df1 = pd.DataFrame(np.random.rand(3, 3), index=list('abc'), columns=['A', 'B', 'c'])
print(df1)
print('----------')
df2 = pd.DataFrame(np.random.rand(3))
print(df2)
print('----------')
dic = {'name': ['lyz1', 'lyz2', 'lyz3'], 'age': [10, 11, 12], 'gender': ['男', '男', '女']}
df3 = pd.DataFrame(dic)

# 读取
print(df3)  # 看全部
print('----------')
print(df3.head(2))  # 看前两行
print('----------')
print(df3.tail(2))  # 看后两行
print('----------')
print(df3.values)  # 看值
print('----------')
print(df3.index)  # 看行号
print(df3.columns)  # 看列号
print('----------')
print(df3['name'].values)  # 看一列的值
print('----------')
