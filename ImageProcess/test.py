# encoding=utf-8
"""
@Time : 2020/2/27 11:35 
@Author : LiuYanZhe
@File : test.py 
@Software: PyCharm
@Description: 
"""
import matplotlib.pyplot as plt

data = [1, 2, 3, 4, 1]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.hist(data, bins=4, weights=[1.0 / len(data)]*len(data))
plt.show()
