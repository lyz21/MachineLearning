# encoding=utf-8
"""
@Time : 2020/6/20 22:12 
@Author : LiuYanZhe
@File : hotMap.py 
@Software: PyCharm
@Description: 热力图
"""
import matplotlib.pyplot as plt
from math_model.util import dataUtil
import seaborn as sns
import numpy as np

data0 = dataUtil.load_data('../data/data.csv')
data = data0.iloc[:, :len(data0.columns) - 1]
print(data.shape)
data = dataUtil.scale(data0)
# data0.loc[:, ['sex', 'label']]
# 横轴年龄，纵轴性别
data = [[
    len(data0[(data0['sex'] == 0) & (data0['age'] < 10) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 10) & (data0['age'] < 20) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 20) & (data0['age'] < 30) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 30) & (data0['age'] < 40) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 40) & (data0['age'] < 50) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 50) & (data0['age'] < 60) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 60) & (data0['age'] < 70) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] >= 70) & (data0['age'] < 80) & (data0['label'] == 1)]),
    len(data0[(data0['sex'] == 0) & (data0['age'] > 80) & (data0['label'] == 1)]),
],
    [
        len(data0[(data0['sex'] == 1) & (data0['age'] < 10) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 10) & (data0['age'] < 20) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 20) & (data0['age'] < 30) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 30) & (data0['age'] < 40) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 40) & (data0['age'] < 50) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 50) & (data0['age'] < 60) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 60) & (data0['age'] < 70) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] >= 70) & (data0['age'] < 80) & (data0['label'] == 1)]),
        len(data0[(data0['sex'] == 1) & (data0['age'] > 80) & (data0['label'] == 1)]),
    ]
]
# data = [[1,len(data0['label']==0) ,1,len(data0['label']==1) ],[,len(data0['label']==0) ,1,len(data0['label']==1) ]]
# data = [
#     [1, 2, 10],
#     [2, 1]
# ]

# fig, ax = plt.subplots(1, 1, figsize=(6, 6))
# heatmap = ax.pcolormesh(np.array(data).T, cmap=plt.cm.Blues, alpha=0.7)
# fig.colorbar(heatmap)
# plt.show()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文黑体
fig, ax = plt.subplots(figsize=(8, 3))
color_map = sns.cubehelix_palette(as_cmap=True)
sns.heatmap(data, cmap=color_map, linewidths=0.05, ax=ax)
ax.xaxis.tick_top()
columns = ['10岁以下', '10岁-19岁', '20岁-29岁', '30岁-39岁', '40岁-49岁', '50岁-59岁', '60岁-69岁', '70岁-79岁', '80岁以上']
index = ['女', '男']
ax.set_xticklabels(columns, minor=False, rotation=30)
ax.set_yticklabels(index, minor=False, rotation=0)

ax.xaxis.tick_top()
ax.invert_yaxis()
plt.savefig('../pic/hot_map.png', dpi=400, bbox_inches='tight')
plt.show()
