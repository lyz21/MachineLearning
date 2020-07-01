# encoding=utf-8
"""
Name:         test
Description:  
Author:       LiuYanZhe
Date:         2019/11/1
"""

# list=[1,2,3,4,5,6,7,8,1,2,13,24,14,32,54]
# dic1={}
#
# for i in list:
#     list1 = []
#     dic1.setdefault(i,list1)
#     dic1[i].append(i)
# print(dic1)

# str='12'
# s=str.split('/')
# print(s)
import numpy
l=[1,2,3,4,5,65,6,77,7,8,8,0]
numpy.savetxt('temp.txt',l)