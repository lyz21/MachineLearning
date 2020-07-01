# encoding=utf-8
"""
@Time : 2020/4/4 15:33 
@Author : LiuYanZhe
@File : SouGouDraw.py 
@Software: PyCharm
@Description: 绘制搜狗热次曲线
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from Convid19 import dateUtil

# 需要的条数范围
end = 1578
start = end - 88

pv1_list = pd.read_csv('../data/SouGou-BuWangChuXin-PV_2020_04_04.csv').iloc[start:end, 0].values.flatten().tolist()
pv2_list = pd.read_csv('../data/SouGou-epidemic-PV_2020_04_04.csv').iloc[start:end, 0].values.flatten().tolist()
pv3_list = pd.read_csv('../data/SouGou-fromPoverty-PV_2020_04_04.csv').iloc[start:end, 0].values.flatten().tolist()
pv4_list = pd.read_csv('../data/SouGou-pneumonia-PV_2020_04_04.csv').iloc[start:end, 0].values.flatten().tolist()
date_list = dateUtil.getDateList(len(pv1_list))
divlin1_sub = date_list.index('01_26')  # 分界线1
divlin2_sub = date_list.index('02_09')  # 分界线2
print(pv1_list)
font_size = 9

fig = plt.figure()
# fig.subplots_adjust(hspace=0.3, top=0.95)  # 子图之间保留的宽度，与顶部保持的宽度
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
# 第一个图
ax1 = fig.add_subplot(2, 2, 1)
plt.xticks(rotation=80, fontsize=font_size)
ax1.set_xlim(0, len(date_list))
ax1.set_ylim(0, max(pv1_list)+5000)
# 设置刻度间隔
x_major_locator = MultipleLocator(4)
ax1.xaxis.set_major_locator(x_major_locator)
ax1.plot(date_list, pv1_list, color='orange')  # 曲线图
ax1.fill_between(date_list, pv1_list, color='orange', alpha=0.2)
ax1.plot([divlin1_sub, divlin1_sub], [0, max(pv1_list)+5000], color='g')  # 分界线
ax1.set_title('(a) "不忘初心"搜索趋势', y=-0.2)

# 第二个图
ax4 = fig.add_subplot(2, 2, 2)
plt.xticks(rotation=80, fontsize=font_size)
ax4.set_xlim(0, len(date_list))
ax4.set_ylim(0, max(pv4_list)+1000000)
# 设置刻度间隔
x_major_locator = MultipleLocator(4)
ax4.xaxis.set_major_locator(x_major_locator)
ax4.plot(date_list, pv4_list, color='orange')  # 曲线图
ax4.fill_between(date_list, pv4_list, color='orange', alpha=0.2)
ax4.plot([divlin1_sub, divlin1_sub], [0, max(pv4_list)+1000000], [divlin2_sub, divlin2_sub], [0, max(pv4_list)+1000000],
         color='g')  # 分界线
ax4.set_title('(b) "肺炎"搜索趋势', y=-0.2)


# 第三个图
ax3 = fig.add_subplot(2, 2, 3)
plt.xticks(rotation=80, fontsize=font_size)
ax3.set_xlim(0, len(date_list))
ax3.set_ylim(0, max(pv3_list)+5000)
# 设置刻度间隔
x_major_locator = MultipleLocator(4)
ax3.xaxis.set_major_locator(x_major_locator)
ax3.plot(date_list, pv3_list, color='orange')  # 曲线图
ax3.fill_between(date_list, pv3_list, color='orange', alpha=0.2)
ax3.plot([divlin2_sub, divlin2_sub], [0, max(pv3_list)+5000], color='g')  # 分界线
ax3.set_title('(c) "脱贫"搜索趋势', y=-0.2)

# 第4个图
ax2 = fig.add_subplot(2, 2, 4)
plt.xticks(rotation=80, fontsize=font_size)
ax2.set_xlim(0, len(date_list))
ax2.set_ylim(0, max(pv2_list)+100000)
# 设置刻度间隔
x_major_locator = MultipleLocator(4)
ax2.xaxis.set_major_locator(x_major_locator)
ax2.plot(date_list, pv2_list, color='orange')  # 曲线图
ax2.fill_between(date_list, pv2_list, color='orange', alpha=0.2)
ax2.plot([divlin1_sub, divlin1_sub], [0, max(pv2_list)+100000], [divlin2_sub, divlin2_sub], [0, max(pv2_list)+100000],
         color='g')  # 分界线
ax2.set_title('(d) "疫情"搜索趋势', y=-0.2)
plt.show()
