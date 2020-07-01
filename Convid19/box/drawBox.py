# encoding=utf-8
"""
@Time : 2020/3/30 23:14 
@Author : LiuYanZhe
@File : drawBox.py 
@Software: PyCharm
@Description: 绘制箱线图
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from Convid19 import PltUtil


# 生成日期方法
def getDateList(day_num, start_month=1, start_day=1):
    month, day = start_month, start_day
    date_list = []
    for i in range(day_num):
        if day >= 31:  # 1月结束，到第2月,1.31没有
            month += 1
            day = 1
        if day < 10:
            day_str = '0' + str(day)
        else:
            day_str = str(day)
        if month < 10:
            month_str = '0' + str(month)
        else:
            month_str = str(month)
        date = month_str + '-' + day_str
        date_list.append(date)
        day += 1
    return date_list


# np.random.seed(2)  # 设置随机种子
# df = pd.DataFrame(np.random.rand(5, 4), columns=['A', 'B', 'C', 'D'])  # 先生成0-1之间的5*4维度数据，再装入4列DataFrame中
# print(df.columns)
# print(df)
# df.boxplot()  # 也可用plot.box()
# plt.show()
# 读取文件
all_province_his_data = pd.read_csv('../data/History_province_2020_03_27.csv')
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
province_data.index = province_data.loc[:, 'date']
province_data = province_data.iloc[:, 2:]
province_data.columns = province_name_arr[1:]
province_data.to_csv(
    '../data/province_all_today_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv')  # 保存文件
# province_data.iloc[:, 2:22].T.boxplot()
# province_data.iloc[:, 2:22].boxplot()
# plt.xticks(rotation=60, fontsize=7.0)
# 方法1
# PltUtil.DrawBox_pd(province_data.iloc[:, 1:], pic_name='box1', rotation=60)
# PltUtil.DrawBox_pd(province_data.iloc[:, 1:].T, pic_name='box2', rotation=60)
# 方法2
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
plt.boxplot(province_data, labels=getDateList(len(province_data),start_month=1,start_day=20),
            flierprops={'markersize': 2}  # 异常值属性
            )
plt.xticks(rotation=90, fontsize=7.0)
# plt.savefig('../pic/box3.png', dpi=400, bbox_inches='tight')
plt.show()

print('结束')
