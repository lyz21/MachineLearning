# encoding=utf-8
"""
@Time : 2020/2/4 14:49 
@Author : LiuYanZhe
@File : test.py 
@Software: PyCharm
@Description: 小测试
"""
import numpy as np

# a=np.ceil(10/3)
# a=np.random.randint(10)
# print(a)

# data=np.loadtxt('data.txt')
# print(len(data))
# print(len(data))

# range1=range(10)
# print(range1)
# range1=list(range1)
# print(range1)

# a0=[]
# a = [1, 2, 3]
# a0.append(a)
# print(a0)

# a=[]
# print(a!=[])

# a = [['.', '.', '.', '0', '.', '.', '.', ],
#      ['.', '.', '0', '0', '0', '.', '.', ],
#      ['.', '0', '0', '0', '0', '0', '.', ],
#      ['.', '0', '0', '0', '0', '0', '.', ],
#      ['.', '.', '0', '0', '0', '.', '.', ],
#      ['.', '.', '.', '0', '.', '.', '.', ],
#      ]
# # 原版输出
# print('原版输出')
# for i in range(len(a)):
#     for j in range(len(a[0])):
#         print(a[i][j],end='')
#     print()
# # 转置输出
# print('转置输出')
# for i in range(len(a[0])):
#     for j in range(len(a)):
#         print(a[j][i],end='')
#     print()

# a = [1, 2, 3]
# b = a.copy()
# b.remove(1)
# print(a, ';', b)

# a是两层结构的字典，即字典的键（key）为字符串类型，值为字典类型
# a = {'a': {'a1': 1, 'a2': 2},
#      'b': {'b1': 1, 'b2': 2},
#      'c': {'c1': 1, 'c2': 2}
#      }
# # .items()方法为字典的遍历方法，即读s出键给k，值给v。则此处读取的k为字符串类型，v为字典类型。
# for k, v in a.items():
#     print('-----------')
#     print('k:', k)
#     print('v:', v)
#     # v为字典类型，则v.get()为通过键获取值（字典数据的读取方式）
#     print('a1', v.get('a1'))

a = {'name': '未改进', 'maxIter': 0, 'learn_rate': 0, 'rightrate': 0}
a['maxIter']=1
print(a)