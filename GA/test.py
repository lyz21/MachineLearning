# encoding=utf-8
"""
Name:         test
Description:  
Author:       LiuYanZhe
Date:         2019/11/28
"""
import random
import math


def test1():
    for i in range(30):
        i = random.randint(1, 2)
        print(i)  # 1 ,2


def test2():
    i = 0
    while True:
        print(i)
        i += 1
        if i == 4:
            print(i)
            break


def test3():
    list = []
    list.append(-1.1)
    print(list)


def test4():
    print(math.ceil(4.1))


def test5():
    list = []
    list1 = [1, 2, 3, 4, 5, 6, 7]
    list2 = [10, 20, 30, 40, 50, 60, 70]
    list.append(list1)
    list.append(list2)
    temp_list = list2.copy()
    for i in range(2, 4):
        list2[i] = list1[i]
        list1[i] = temp_list[i]
    print(list1)
    print(list2)
    print(list)


def test6():
    for j in range(10 - 1, -1, -1):
        print(j)


test6()
