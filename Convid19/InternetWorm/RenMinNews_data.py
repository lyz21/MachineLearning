# encoding=utf-8
"""
@Time : 2020/3/29 14:35 
@Author : LiuYanZhe
@File : RenMinNews_data.py 
@Software: PyCharm
@Description: 人民日报每日头条
"""
# 下载页面模块
import requests
# 分析页面
import bs4
# 控制运行时间
import time
from Convid19.InternetWorm import Util
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}  # 请求头

month, day = 1, 1
article_list = []
date_list = []
for i in range(88):
    if (month == 1 or month == 3) and day > 31:  # 1月结束，到第2月,1.31没有
        month += 1
        day = 1
    if month == 2 and day > 29:
        month += 1
        day = 1
    if month == 4 and day > 30:
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

    url = 'http://paper.people.com.cn/rmrb/html/2020-' + month_str + '/' + day_str + '/nw.D110000renmrb_2020' + month_str + day_str + '_2-01.htm'
    response = requests.get(url)
    # 防止乱码
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text)
    p_list = soup.select('div>p')
    article = ''
    for i in range(len(p_list) - 1):
        paragraph = str(p_list[i].getText())
        article += paragraph
    article = article.replace('\r', '').replace('\n', '').replace(' ', '').replace('\u3000', '').replace('\xa0', '')
    article_list.append([article])  # 构造成2维矩阵，与爬取的title数据对应
    print(article)
    day += 1
    time.sleep(10)
    df_article = pd.DataFrame(article_list, index=date_list)
    # df_article['date'] = date_list
    df_article = df_article.fillna('空')
    Util.save_data(df_article, 'RenMIn_top2', filename='../data/', index=date_list)
