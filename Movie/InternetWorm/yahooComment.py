# encoding=utf-8
"""
Name:         yahooComment
Description:  爬取雅虎日本电影评论
Author:       LiuYanZhe
Date:         2019/10/31
"""
# 下载页面
import requests
# 清洗数据(分析页面)
import bs4
# 控制运行时间
import time
# 日志
import logging
# 处理表格
import openpyxl
# 目录控制
import os

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志
# logging.disable()

'''全局变量'''
# 工作目录
WORKSPACE = 'E:/data_lyz'
# 起始页面号
PAGENUM = 1
# 每页条数
ENTRYNUM = 10
# 爬取总页数
PAGENUM_COUNT = 90
# 网页链接
# URL = 'https://movies.yahoo.co.jp/movie/355058/review/?sort=mrf&page='  # 你的名字
# URL = 'https://movies.yahoo.co.jp/movie/362605/review/?sort=mrf&page='  # 至暗时刻
# URL = 'https://movies.yahoo.co.jp/movie/362181/review/?sort=mrf&page='  # 三块广告牌
# URL = 'https://movies.yahoo.co.jp/movie/365598/review/?sort=mrf&page='  # 绿皮书
URL = 'https://movies.yahoo.co.jp/movie/361843/review/?sort=mrf&page='  # 战狼2
# 每次爬取间隔时间
T = 2
# 保存的文件名
# WORKBOOKNAME = '你的名字日本雅虎影评.xlsx'
# WORKBOOKNAME = '至暗时刻日本雅虎影评.xlsx'
# WORKBOOKNAME = '三块广告牌日本雅虎影评.xlsx'
# WORKBOOKNAME = '绿皮书日本雅虎影评.xlsx'
WORKBOOKNAME = '战狼2日本雅虎影评.xlsx'
# 存储列号
COLUMN_NUM=2
# 设置工作目录
os.chdir(WORKSPACE)


# 获取网页方法,返回soup对象进行数据清洗
def getrequest(url):
    # 为避免ip被封，限制每分钟爬取次数
    time.sleep(T)
    # 获取网页response对象
    response = requests.get(url)
    # 乱码处理
    response.encoding = 'utf-8'
    # response.encoding = response.apparent_encoding
    # 监控网页状态
    try:
        response.raise_for_status()
        # 获取soup对象，BeautuifulSoup清洗数据
        soup = bs4.BeautifulSoup(response.text)
    except requests.exceptions.HTTPError:
        soup = '无'
        print('获取网页出错！')
    return soup


'''每页存储为一个表格，防止中间爬取出错一个数据也存不上'''
# 创建workbook对象
workbook = openpyxl.Workbook()
# 获取当前sheet对象（表格）
sheet = workbook.get_active_sheet()
sheet['A1'] = '评分'
sheet['A2'] = '点赞数'
for i in range(PAGENUM_COUNT):
    print('第', str(i + 1), '页')
    # 拼接链接
    Turl = URL + str(PAGENUM)
    # 获得soup
    soup = getrequest(Turl)
    # 找到评分标签
    star_list = soup.select('.rating-star.text-large>i')
    # 找到点赞标签
    good_list = soup.select('.opacity-60>strong')
    for j in range(ENTRYNUM):
        print('第', str(j + 1), '个评论')
        # 列号转字母
        column = openpyxl.utils.get_column_letter(COLUMN_NUM)
        # 获取评分内容
        star_temp = star_list[j].get('class')
        # 剪切出评分
        star = str(star_temp[1]).replace('rate-', '')
        print('评分:', star)
        sheet[column+'1']=star
        good = good_list[2 * j + 1].getText()
        print('认同人数：', good)
        sheet[column+'2']=good
        COLUMN_NUM+=1
        # 设置表名
        sheet.title = str('评论')
        # 保存文件
        workbook.save(WORKBOOKNAME)
        print('已保存')
    # 当前更新页面号
    PAGENUM = PAGENUM + 1
