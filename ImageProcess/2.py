# encoding=utf-8
"""
@Time : 2020/2/27 9:40 
@Author : LiuYanZhe
@File : 2.py 
@Software: PyCharm
@Description: 第二单元习题
"""
import numpy as np
import matplotlib.pyplot as plt

data = np.array([[0], [1], [1], [2], [3], [1], [3], [2],
                 [7], [6], [5], [0], [6], [2], [5], [7],
                 [6], [6], [0], [1], [1], [6], [4], [3],
                 [2], [7], [6], [5], [5], [3], [6], [5],
                 [3], [2], [2], [7], [2], [6], [6], [1],
                 [2], [6], [5], [0], [2], [7], [5], [0],
                 [1], [2], [3], [2], [1], [2], [1], [2],
                 [3], [2], [1], [3], [1], [1], [2], [2]
                 ])
# 存储各个比值
arr = []
# 元素总个数
count = data.size
# 计算比值
for i in range(0, 8):
    arr.append(sum(data == i)[0] / count)
print(arr)

# 绘制图像
# 创建画布
fig = plt.figure(figsize=(12, 5))  # 创建一个画板
# 添加子图
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
# 直方图
ax1.hist(data, bins=8, weights=[1.0 / data.size] * data.size)
# 折线图
ax2.plot(range(0, 8), arr)
plt.savefig('./pic/2.png')
plt.show()
