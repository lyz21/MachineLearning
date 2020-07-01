# encoding=utf-8
"""
@Time : 2020/6/19 17:37 
@Author : LiuYanZhe
@File : Stacking.py 
@Software: PyCharm
@Description: 
"""
## 载入所需要的模块和函数
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew
from mlxtend.classifier import StackingClassifier

train = pd.read_csv('./input/train.csv')
## 查看所有特征的名称及数据类型
names = train.columns   ## 特征名称
types = train.dtypes    ## 数据类型

## 删除无用特征“ID”
train.drop('Id', axis=1, inplace=True)

## 寻找异常点
fig, ax = plt.subplots()
ax.scatter(x = train['GrLivArea'], y = train['SalePrice'])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)
plt.show()