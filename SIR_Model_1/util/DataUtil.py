# encoding=utf-8
"""
@Time : 2020/4/20 18:39 
@Author : LiuYanZhe
@File : DataUtil.py 
@Software: PyCharm
@Description: 数据集工具类
"""
import pandas as pd


# 加载数据
def load_data_total(path='../data/History_country_2020_04_19.csv', line_num1=4193, line_num2=4271, N=60431283):
    pd1 = pd.read_csv(path).iloc[line_num1:line_num2, :].loc[:, ('date', 'total_confirm', 'total_dead', 'total_heal')]
    # print(pd1)
    recovered_real = pd1['total_dead'] + pd1['total_heal']  # 移除
    infectious_real = pd1['total_confirm'] - recovered_real  # 感染
    # infectious_real = pd1['total_confirm']  # 感染
    susceptible_real = N - recovered_real - infectious_real  # 易感
    date = pd1['date']
    return recovered_real, infectious_real, susceptible_real, date


# 加载每日数据
def load_data_taday(path='../data/History_country_2020_04_19.csv', line_num1=4193, line_num2=4271, N=60431283):
    pd1 = pd.read_csv(path).iloc[line_num1:line_num2, :].loc[:, ('date', 'today_confirm', 'today_dead', 'today_heal')]
    recovered_real = pd1['today_dead'] + pd1['today_heal']  # 移除
    infectious_real = pd1['today_confirm'] - recovered_real  # 感染
    # infectious_real = pd1['today_confirm']  # 感染
    susceptible_real = N - recovered_real - infectious_real  # 易感
    date = pd1['date']
    return recovered_real, infectious_real, susceptible_real, date


# 将增加转变为总的
def calcu_total(x0, dxdt_list):
    total_list = [x0]
    for i in range(1, len(dxdt_list)):
        x = total_list[i - 1] + dxdt_list[i]
        total_list.append(x)
    return total_list


# 获取日期
def getDateList(day_num, start_month=1, start_day=1, con_str='_', year='2020', ):
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
    # recovered_real, infectious_real, susceptible_real, date = load_data_taday()
    # recovered_real_total, infectious_real_total, susceptible_real_total, date = load_data_total()
    # total = calcu_total(infectious_real_total.values[0], infectious_real.values)
    # print('infectious_real:', infectious_real)
    # print('total:', total)
    # print('total:', date)
    # print('infectious_real_total:', infectious_real_total)
    data_list = getDateList(160)
    data_list = getDateList_interval(data_list, 20)
    print(data_list)
