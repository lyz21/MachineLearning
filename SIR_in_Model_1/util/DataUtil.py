# encoding=utf-8
"""
@Time : 2020/5/6 16:54 
@Author : LiuYanZhe
@File : DataUtil.py 
@Software: PyCharm
@Description: 关于数据的工具类
"""
import requests
import json
import pandas as pd
import time


# 从互联网爬取数据
def get_data_fron_net():
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

    ###算法开始###
    province_data = pd.read_csv('../data/AllCountry_2020_03_27.csv')  # 此文件为所有国家当天数据，加载目的为需要里面的id号
    province_dict = {num: name for num, name in zip(province_data['id'], province_data['name'])}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }  # 请求头

    i = 0
    start = time.time()
    for province_id in province_dict:
        try:
            url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + str(province_id)  # 访问链接
            data_requests = requests.get(url, headers=headers)  # 发起请求，获得响应数据
            data_json = json.loads(data_requests.text)  # 格式转为json
            # 解析数据
            data = data_json['data']['list']  # list类型
            history_data = get_data(data, ['date', 'lastUpdateTime'])
            history_data['name'] = province_dict[province_id]

            # 合并数据
            if i == 0:
                history_all_data = history_data
                i += 1
            else:
                history_all_data = pd.concat([history_all_data, history_data], axis=0)
                i += 1
            print('*' * 10, '第', str(i), '个', province_dict[province_id], '成功。该数据大小：', history_data.shape, '，总数据大小：',
                  history_all_data.shape, '累计耗时：', round(time.time() - start), '*' * 10)
            save_data(history_all_data, 'History_country')
            time.sleep(10)
        except:
            print('*' * 10, province_dict[province_id], 'wrong!', '*' * 10)
    print('结束！')


# 根据国家名寻找索引
def get_index_by_name(path, name, start_index, end_index):
    print('-' * 10, 'DataUtil.get_index_by_name 开始', '-' * 10)
    print('start_index:', start_index)
    print('end_index:', end_index)
    df = pd.read_csv(path)
    list1 = df[df.name == name].index.tolist()
    end_index = len(list1) - 1 - end_index
    print('len(list1):', len(list1))
    print('数据长度：', len(list1))
    print('数据：', list1)
    print('新的起始结束下标', list1[start_index], list1[end_index])
    print('-' * 10, 'DataUtil.get_index_by_name 结束', '-' * 10)
    return list1[start_index], list1[end_index]


# 加载SIR所需要的数据_当日所存数据
def load_data_SIR_today(path='../data/History_country_2020_05_06.csv', name='中国', N=140005000, start_index=0,
                        end_index=0):
    start_index, end_index = get_index_by_name(path, name, start_index, end_index)
    pd1 = pd.read_csv(path).iloc[start_index:end_index, :].loc[:, ('date', 'today_confirm', 'today_dead', 'today_heal')]
    print(pd1)
    remove_real = pd1['today_dead'] + pd1['today_heal']  # 移除 R
    infectious_real = pd1['today_confirm'] - remove_real  # 感染 I
    susceptible_real = N - remove_real - infectious_real  # 易感 S
    date = pd1['date']  # 日期
    return remove_real, infectious_real, susceptible_real, date


# 加载SIR所需要的数据_当日总数据
def load_data_SIR_total(path='../data/History_country_2020_05_06.csv', name='中国', N=140005000, start_index=0,
                        end_index=0):
    print('-' * 10, 'DataUtil.load_data_SIR_total 开始', '-' * 10)
    print('path:', path)
    print('name:', name)
    print('N:', N)
    print('start_index:', start_index)
    print('end_index:', end_index)
    start_index, end_index = get_index_by_name(path, name, start_index, end_index)
    if start_index > end_index:
        print('错误！ 数据行数设置出错，起始行大于结束行。start_index, end_index:', start_index, end_index)
    pd1 = pd.read_csv(path).iloc[start_index:end_index, :].loc[:, ('date', 'total_confirm', 'total_dead', 'total_heal')]
    print('加载数据：', pd1)
    remove_real = pd1['total_dead'] + pd1['total_heal']  # 移除 R
    infectious_real = pd1['total_confirm'] - remove_real  # 感染 I
    susceptible_real = N - remove_real - infectious_real  # 易感 S
    date = pd1['date']  # 日期
    print('-' * 10, 'DataUtil.load_data_SIR_total 结束', '-' * 10)
    return remove_real, infectious_real, susceptible_real, date


# 获取第一个日期的月和日
def get_m_d(date_list):
    date = str(date_list[0])
    list = date.split('-')
    return int(list[1]), int(list[2])


# 获取日期列表
def getDateList(day_num, start_month=1, start_day=1, con_str='_', year='2020'):
    m31 = [1, 3, 5, 7, 8, 10, 12]
    m30 = [4, 6, 9, 11]
    month, day = start_month, start_day
    date_list = []
    for i in range(day_num):
        if month in m31 and day > 31:  # 1月结束，到第2月,1.31没有
            month += 1
            day = 1
        elif month == 2 and day > 29:
            month += 1
            day = 1
        elif month in m30 and day > 30:
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
        date = year + con_str + month_str + con_str + day_str
        date_list.append(date)
        day += 1
    return date_list


# 获得固定间隔的日期列表
def getDateList_interval(date_list, interval):
    new_date_list = []
    for i in range(0, len(date_list), interval):
        new_date_list.append(date_list[i])
    return new_date_list


if __name__ == '__main__':
    # get_data_fron_net()   # 爬取所有国家历史数据
    load_data_SIR_total()
