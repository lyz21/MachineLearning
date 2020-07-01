# encoding=utf-8
"""
@Time : 2020/4/2 17:01 
@Author : LiuYanZhe
@File : dateUtil.py 
@Software: PyCharm
@Description: 关于日期的工具类
"""
import pandas as np

m31 = [1, 3, 5, 7, 8, 10, 12]
m30 = [4, 6, 9, 11]


# 获取日期
def getDateList(day_num, year='2020', start_month=1, start_day=1, con_str='_'):
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





def reDate():
    df = np.read_csv('data/RenMIn_top_2020_03_30.csv').iloc[:, 1]
    df.index = getDateList(len(df))
    df.to_csv('data/Ren.csv')



if __name__ == '__main__':
    reDate()
    # print(getDateList(100))
