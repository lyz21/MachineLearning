# encoding=utf-8
"""
@Time : 2020/3/28 19:02 
@Author : LiuYanZhe
@File : box.py 
@Software: PyCharm
@Description: 
"""
import numpy as np
import matplotlib.pyplot as plt

data = np.array(
    [13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70])
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.boxplot(data)
# plt.show()
plt.savefig('./pic/demobox.png', dpi=400, bbox_inches='tight')