# encoding=utf-8
"""
@Time : 2020/4/4 13:18 
@Author : LiuYanZhe
@File : cleanData.py 
@Software: PyCharm
@Description: 清洗数据
"""
import pandas as pd

df1 = pd.read_csv('../data/China_history_2020_04_04.csv')
print(df1.columns)
print(df1.loc[:68, ['date', 'today_confirm', 'total_confirm', 'total_heal', 'total_dead']])
df2 = df1.loc[:68, ['date', 'today_confirm']]
temp_df = df1['total_confirm'] - df1['total_heal'] - df1['total_dead']  # 计算出的当日现存人数
df2['now'] = temp_df
dead_rate = df1['total_dead'] / (df1['total_dead'] + df1['total_heal'])
df2['dead_rate'] = dead_rate
heal_rate = df1['total_heal'] / (df1['total_dead'] + df1['total_heal'])
df2['heal_rate'] = heal_rate
print(df2)
df2.to_csv('../data/Chinahistory_today_now_20200328.csv')
# print(type(df2))
