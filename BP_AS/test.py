# encoding=utf-8
"""
Name:         test
Description:  
Author:       LiuYanZhe
Date:         2019/12/2
"""
import numpy as np
import matplotlib.pyplot as plt

# list=[]
# for i in range(10):
#     list.append(i)
# print(list)
# list=numpy.array(list)
# list=list*0.1
# list=list.tolist()
# print(list)
# list1=[1]
# numpy.savetxt('test.txt',list1)

# def test1():
#     list1=[1,2,3,4,5,6,7,1,2,4,8,8,8]
#     # a=list1.index(max(list1))
#     a=max(list1)
#     print(a)
#
# def test2():
#     list=[[1,2],[3,4]]
#     list1=list[0]
#     list1[0]=10
#     for i in list:
#         for j in i:
#             print(j)
# test1()
# test2()

# y = list(range(1, 501))
# print(y)


# a = np.array([1, 2, 3])
# b = np.array([2, 3, 5])
# c = np.array([[1], [2], [3]])
# print(a)
# print(b)
# print(c)
# print(b - a)
# print(b - c)

# a = 3
# b = a ** 2
# print(b)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.plot([0, 1], [1, 1], color='k', lw=1, linestyle='--', label='--')
ax1.plot([0, 1], [2, 2], color='k', lw=1, linestyle='-', label='-')
ax1.plot([0, 1], [3, 3], color='k', lw=1, linestyle='-.', label='-.')
ax1.plot([0, 1], [4, 4], color='k', lw=1, linestyle=':', label=':')
plt.show()
