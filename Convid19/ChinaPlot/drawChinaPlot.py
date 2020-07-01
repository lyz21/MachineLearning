# encoding=utf-8
"""
@Time : 2020/4/4 13:39 
@Author : LiuYanZhe
@File : drawChinaPlot.py 
@Software: PyCharm
@Description: 绘制中国每日新增和现存曲线
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

data_df = pd.read_csv('../data/Chinahistory_today_now_20200328.csv')
# print(data_df)
date_list = data_df.loc[:, 'date'].values.flatten().tolist()  # 日期列表
today_confirm_list = data_df.loc[:, 'today_confirm'].values.flatten().tolist()  # 每日新增列表
now_list = data_df.loc[:, 'now'].values.flatten().tolist()  # 现存列表
dead_rate_list = data_df.loc[:, 'dead_rate'].values.flatten().tolist()  # 死亡率列表
heal_rate_list = data_df.loc[:, 'heal_rate'].values.flatten().tolist()  # 治愈率列表

divlin1_sub = date_list.index('2020-01-26')  # 分界线1
divlin2_sub = date_list.index('2020-02-09')  # 分界线2
max_y = max(now_list)  # 当日现存最高点纵坐标
max_x = now_list.index(max(now_list))  # 当日现存最高点横坐标
print('date_list:', date_list)
print('today_confirm_list:', today_confirm_list)
print('now_list:', now_list)
print('divlin1_sub:', now_list)
print('divlin2_sub:', now_list)
print('max_y:', max_y)
print('max_x:', max_x)

fig = plt.figure()
fig.subplots_adjust(hspace=0.3, top=0.95)  # 子图之间保留的宽度，与顶部保持的宽度
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
x_major_locator = MultipleLocator(4)    # 刻度间隔
fontsize=9
# 第一个图
ax1 = fig.add_subplot(2, 2, 3)
plt.xticks(rotation=80, fontsize=fontsize)
ax1.xaxis.set_major_locator(x_major_locator)
ax1.set_xlim(0, len(date_list))
ax1.set_ylim(0, max(today_confirm_list) + 1500)
ax1.plot(date_list, today_confirm_list, color='orange')  # 曲线图
ax1.fill_between(date_list, today_confirm_list, color='orange', alpha=0.2)
ax1.plot([divlin1_sub, divlin1_sub], [0, max(today_confirm_list)+ 1500], [divlin2_sub, divlin2_sub],
         [0, max(today_confirm_list)+ 1500], color='g')  # 分界线
ax1.set_title('(a) 每日新增人数曲线',y=-0.28)
# 第二个图
ax2 = fig.add_subplot(2, 2, 1)
plt.xticks(rotation=80, fontsize=fontsize)
ax2.xaxis.set_major_locator(x_major_locator)
ax2.set_xlim(0, len(date_list))
ax2.set_ylim(0, max(now_list) + 8000)
ax2.plot(date_list, now_list, color='orange')
ax2.fill_between(date_list, now_list, color='orange', alpha=0.2)
ax2.plot([divlin1_sub, divlin1_sub], [0, max(now_list) + 8000], [divlin2_sub, divlin2_sub],
         [0, max(now_list) + 8000], color='g')  # 分界线
ax2.set_title('(b) 当日现存人数曲线',y=-0.28)

# 第三个图
ax3 = fig.add_subplot(2, 2, 2)
plt.xticks(rotation=80, fontsize=fontsize)
ax3.xaxis.set_major_locator(x_major_locator)
ax3.set_xlim(0, len(date_list))
ax3.set_ylim(0, 1)
ax3.plot(date_list, dead_rate_list, color='orange')
ax3.fill_between(date_list, dead_rate_list, color='orange', alpha=0.2)
ax3.plot([divlin1_sub, divlin1_sub], [0, 1], [divlin2_sub, divlin2_sub],
         [0, 1], color='g')  # 分界线
ax3.set_title('(c) 病死率曲线',y=-0.28)

# 第四个图
ax4 = fig.add_subplot(2, 2, 4)
plt.xticks(rotation=80, fontsize=fontsize)
ax4.xaxis.set_major_locator(x_major_locator)
ax4.set_xlim(0, len(date_list))
ax4.set_ylim(0, 1)
ax4.plot(date_list, heal_rate_list, color='orange')
ax4.fill_between(date_list, heal_rate_list, color='orange', alpha=0.2)
ax4.plot([divlin1_sub, divlin1_sub], [0, 1], [divlin2_sub, divlin2_sub],
         [0, 1], color='g')  # 分界线
ax4.set_title('(d) 治愈率曲线',y=-0.28)

# plt.savefig('../pic/china_plot.png',dpi=600, bbox_inches='tight')
plt.show()
