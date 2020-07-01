# encoding=utf-8
"""
@Time : 2020/3/27 20:48 
@Author : LiuYanZhe
@File : Util.py 
@Software: PyCharm
@Description: 工具类
"""
import pandas as pd
import time


# 提取数据的方法封装为函数
def get_data(data, info_list):
    info = pd.DataFrame(data)[info_list]  # 可以直接取出的数据

    today_data = pd.DataFrame([item_data['today'] for item_data in data])  # 取出当天数据
    today_data.columns = ['today_' + columns_name for columns_name in today_data.columns]  # 重命名列名

    total_data = pd.DataFrame([item_data['total'] for item_data in data])  # 取出总数据
    total_data.columns = ['total_' + columns_name for columns_name in total_data]  # 重命名列名

    # 合并三个表并返回
    return pd.concat([info, today_data, total_data], axis=1)


# 封装保存数据方法
def save_data(data, name, filename='../data/', index=None):
    # file_name = '../data/' + name + '_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
    file_name = filename + name + '_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
    data.to_csv(file_name, index=index, encoding='utf_8_sig')
    print('保存文件', file_name, '成功！')
