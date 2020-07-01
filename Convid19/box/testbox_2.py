# encoding=utf-8
"""
@Time : 2020/3/31 10:58 
@Author : LiuYanZhe
@File : testbox_2.py 
@Software: PyCharm
@Description: 绘制盒图测试2
"""

import pandas as pd
import matplotlib.pyplot as plt
from Convid19 import PltUtil
import numpy as np
import time

# 天数
# day=50

# 读取文件
all_province_his_data = pd.read_csv('data/History_province_2020_03_27.csv')
# 按照省和分区分
i = 0
# 获取省份名称列表
province_name_arr = all_province_his_data['name'].unique()  # type=numpy.ndarray ['湖北' '广东' '河南' ...]
for every_name in province_name_arr:
    temp_all_data = all_province_his_data[all_province_his_data['name'].isin([every_name])]  # 切割获得每个省份数据
    temp_data = temp_all_data.loc[:, ['date', 'today_confirm']]  # 切割获取每个省份数据中的date数据和today_confirm数据
    # 连接每个省份数据
    if i == 0:
        province_data = temp_data
        i = 1
    else:
        province_data = pd.merge(province_data, temp_data, on='date',
                                 how='outer')  # on='date'，按照date列连接，how='outer'，出现不重合键时，取并集
province_data = province_data.fillna(0.0)  # 填充缺失值
date_arr = province_data.loc[:, ['date']].values  # pd类型转np类型，日期列表
province_data.index = province_data.loc[:, 'date']
province_data = province_data.iloc[:, 1:]
province_data.columns = province_name_arr
province_data.to_csv(
    'data/province_all_today_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv')  # 保存文件
#####################################################

# date_arr = province_data.loc[:, ['date']].values  # pd类型转np类型，日期列表

# print(province_data.index)
data_arr = province_data.iloc[:, 1:]  # pd类型转np类型，纯数据列表，行为时间，列为省份
# print(data_arr.columns)
print(data_arr)
data2_arr = province_data.iloc[:, 1:].T  # pd类型转np类型，纯数据列表，
# print(data2_arr)
date_list = date_arr.reshape(1, -1).tolist()[0]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# plt.boxplot(data_arr,
#             notch=False,  # 中位线处不设置凹陷
#             widths=0.2,  # 设置箱体宽度
#             medianprops={'color': 'red'},  # 中位线设置为红色
#             boxprops=dict(color="blue"),  # 箱体边框设置为蓝色
#             labels=date_list[:42],  # 设置标签
#             whiskerprops={'color': "black"},  # 设置须的颜色，黑色
#             capprops={'color': "green"},  # 设置箱线图顶端和末端横线的属性，颜色为绿色
#             flierprops={'color': 'purple', 'markeredgecolor': "purple", 'markersize': 3}  # 异常值属性，这里没有异常值，所以没表现出来
#             )
plt.boxplot(data_arr,
            labels=date_list[:],  # 设置标签
            flierprops={'markersize': 2},  # 异常值属性
            )
plt.xticks(rotation=60, fontsize=5.0)
plt.savefig('./pic/box1.png', dpi=400, bbox_inches='tight')
# plt.show()

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
plt.boxplot(data2_arr,
            labels=province_name_arr[1:],  # 设置标签
            flierprops={'markersize': 2},  # 异常值属性
            )
plt.xticks(rotation=60, fontsize=5.0)
# plt.savefig('./pic/box2.png', dpi=400, bbox_inches='tight')
plt.show()
# 绘制盒图
# PltUtil.DrawBox(data2_arr, xticks=date_list[:42], pic_name='box1', rotation=60)  # 按时间
# PltUtil.DrawBox(data2_arr, pic_name='box1', rotation=60)
# PltUtil.DrawBox(data_arr, xticks=date_list[:42], pic_name='box1', rotation=60)
# PltUtil.DrawBox(province_data, pic_name='box3', rotation=60)
# 绘制折线图
# wuhan_arr = province_data.iloc[:, 1].values
# PltUtil.DrawPlot(data_y=wuhan_arr, xticks=date_list, pic_name='hubei_line', rotation=60)
# print('完成！')
