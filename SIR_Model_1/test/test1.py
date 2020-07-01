# encoding=utf-8
"""
@Time : 2020/4/19 16:32 
@Author : LiuYanZhe
@File : test1.py 
@Software: PyCharm
@Description: 
"""
import numpy as np
from scipy.optimize import minimize
import pandas as pd


def test_zip():
    np1 = np.random.rand(5, 2)
    print(np1)
    # a = [1, 2, 3]
    # b = [5, 6]
    # c = [7, 8, 9]
    for a, b, c in zip([np1[:, 0], np1[:, 1]], ['red', 'black'], ['line1', 'line2']):
        print(a, b, c)


def test_linspace():
    np1 = np.linspace(1, 360, 360)  # 1-360分成360份
    print(np1)


def test_lambda():
    y = lambda x: x ** 2
    print(y(9))  # 输出81


def test_asarry():
    x0 = np.asarray((5))
    print(x0)


def test_scipy_optimize_minimize():  # 反向传播求最优值。即求y最小时的x值
    def fun1(parameters, arg):  # 参数为要优化的变量
        a, b = parameters
        y = 0
        for x in arg:
            y += a ** 2 * x ** 2 + b ** 2
        return y

    # minimize(fun, x0, args=()),fun ：优化的目标函数,x0 ：初值，一维数组，shape (n,),args ： 元组，可选，额外传递给优化函数的参数
    min = minimize(fun1, x0=[0.1, 0.21], args=([1, 2, 3, 4]))  # 此方法求出不准确，且依赖初始值
    print(min)
    print('min_y=', min.fun, '; min(a,b)=', min.x)


def test_data1():
    add_days = 39  # 从封城开始
    pd1 = pd.read_csv('../data/History_country_2020_04_19.csv').iloc[4193 + add_days:4271, :].loc[:,
          ('date', 'total_confirm', 'total_dead', 'total_heal', 'name')]
    print(pd1.values)


def test_data2():
    add_days = 39  # 从封城开始
    pd1 = pd.read_csv('../data/History_country_2020_04_19.csv').iloc[4193 + add_days:4271, :].loc[:,
          ('date', 'today_confirm', 'today_heal', 'today_dead', 'name')]
    print(pd1.values)


def test_list():
    list1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    list2 = 2 * list1 + 3
    print(list2)


def test_list2():
    list1 = [1, 2, 3, 4]
    a = max(list1)
    sub = list1.index(a)
    print(sub)


def test_list3():
    list1 = [1, 2]
    list2 = [3, 4]
    list3 = list1 + list2
    print(list3)


def test_add(i):
    i += 1
    return i


def test_range():
    l = np.zeros([2, 2])
    print(l)


def test_list_0430():  # 二维数组求最大值
    list1 = [[1, 2], [3, 4]]
    print(min(list1))


def merge(s_list):
    size = len(s_list)
    for i in range(size):
        for j in range(size):
            x = list(set(s_list[i] + s_list[j]))
            y = len(s_list[i]) + len(s_list[j])
            if i == j or s_list[i] == 0 or s_list[j] == 0:
                break
            elif len(x) < y:
                s_list[i] = x
                s_list[j] = [0]
    for item in s_list:
        if item == [0]:
            s_list.remove(item)
    print(s_list)


if __name__ == '__main__':
    # test_zip()
    # test_linspace()
    # test_lambda()
    # test_asarry()
    # test_scipy_optimize_minimize()
    # test_data2()
    # test_list()
    # test_list2()
    # test_list3()

    # i = 1
    # j = test_add(i)
    # print(i, j)

    # test_range()
    # test_list_0430()

    merge([[1, 2], [3, 4], [0, 1]])
