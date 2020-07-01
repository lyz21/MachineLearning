# encoding=utf-8
"""
@Time : 2020/5/6 17:08 
@Author : LiuYanZhe
@File : test_data.py 
@Software: PyCharm
@Description: 关于数据的测试
"""
import pandas as pd
import numpy as np


def test_pd1():
    df = pd.read_csv('../data/History_country_2020_05_06.csv')
    list1 = df[df.name == '突尼斯'].index.tolist()
    df2 = df.iloc[list1[0]:list1[len(list1) - 1], :]
    print(df2)
    return df2


def test_pd2():
    df = test_pd1()
    date = str(df.loc[0, 'date'])
    print(date, type(date))
    date_list = date.split('-')
    print(date_list)
    print(int(date_list[0]))
    print(int(date_list[1]))


def test_list():
    list1 = np.array([1, 2, 3])
    list2 = np.array([2, 6, 9])
    b = 10
    list2 = list1 / list2 * b
    print(list2)


if __name__ == '__main__':
    # test_pd1()
    # test_pd2()
    test_list()
