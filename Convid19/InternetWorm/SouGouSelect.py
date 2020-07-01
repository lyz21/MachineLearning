# encoding=utf-8
"""
@Time : 2020/4/2 13:04 
@Author : LiuYanZhe
@File : SouGouSelect.py 
@Software: PyCharm
@Description: 爬取搜狗平台搜索量
"""
import requests
# 使用正则分析页面
import re
import pandas as pd
import time


def getHotWords(word, filename):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}  # 请求头
    url = 'http://index.sogou.com/index/searchHeat?kwdNamesStr=' + word + '&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT'
    response = requests.get(url, headers=headers)
    # 防止乱码
    response.encoding = response.apparent_encoding
    # 设定正则表达式匹配模式,找到位置 text1和text2找出列表，但由于没法将str转为list类型，因此放弃
    # comp1 = re.compile(r'root.SG.wholedata =.*')  # 设定查找模式
    # text1 = comp1.search(response.text).group()  # 取出所有匹配到的字符串（这里只匹配到一个）,方式1，pattern.search(str)
    # comp2 = re.compile(r'=.*,"topPvDataList')
    # text2 = comp2.search(text1).group()
    # text3 = re.search('\[\[.*\]\]', text2).group()  # 取出所有匹配到的字符串（这里只匹配到一个）,方式2，re.search(pattern,str)
    text = response.text
    avgPv = int(re.search('avgPv":\d*', text).group().replace('avgPv":', ''))  # 平均搜索量
    sumPv = int(re.search('sumPv":\d*', text).group().replace('sumPv":', ''))  # 总搜索量
    pv_list = re.findall('pv":\d*', text)  # 每日搜索量
    date_list = re.findall('date":\d*', text)  # 日期
    # 将搜索量转为int类型，并取出完整的日期
    for i in range(len(pv_list)):
        pv_list[i] = int(pv_list[i].replace('pv":', ''))
        date_list[i] = date_list[i].replace('date":', '')
    print(word, ' avgPv:', avgPv)
    print(word, ' sumPv:', sumPv)
    df = pd.DataFrame([pv_list, date_list]).T
    df.columns = ['Pv', 'date']
    df.to_csv(
        '../data/SouGou-' + str(filename) + '-PV_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv',
        index=None,
        encoding='utf_8_sig')
    print(df)


if __name__ == '__main__':
    words_list = ['不忘初心', '肺炎', '脱贫', '疫情', ]
    name_list = ['BuWangChuXin', 'pneumonia', 'fromPoverty', 'epidemic']
    for i in range(len(words_list)):
        getHotWords(words_list[i], name_list[i])
