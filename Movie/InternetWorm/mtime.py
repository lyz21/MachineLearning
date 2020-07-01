# encoding=utf-8
"""
Name:         mtime
Description:  
Author:       LiuYanZhe
Date:         2019/10/29
"""
# 下载页面
import requests
# 清洗数据
import bs4
# 日志模块
import logging
# 时间控制
import time
# 目录控制
import os
# 处理表格
import openpyxl

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志模块
logging.disable()
'''全局变量'''
# URL = 'http://movie.mtime.com/240425/reviews/short/'  # 时光  可爬 红海行动
# URL = 'http://movie.mtime.com/263505/reviews/short/'  # 时光  可爬 我和我的祖国
# URL = 'http://movie.mtime.com/229733/reviews/short/'  # 时光  可爬 战狼2
# URL = 'http://movie.mtime.com/218707/reviews/short/'  # 时光  可爬 流浪地球
# URL = 'http://movie.mtime.com/251525/reviews/short/'  # 时光  可爬 哪吒
# URL = 'http://movie.mtime.com/238037/reviews/short/'  # 时光  可爬 蜘蛛侠
# URL = 'http://movie.mtime.com/258541/reviews/short/'  # 时光  可爬 绿皮书
# URL = 'http://movie.mtime.com/218090/reviews/short/'  # 时光  可爬 复仇者联盟4
URL = 'http://movie.mtime.com/228404/reviews/short/'  # 时光  可爬 三块广告牌
# URL = 'http://movie.mtime.com/232987/reviews/short/'  # 时光  可爬 至暗时刻

# 时光网只能看10页，且页面命名不太有规律，因此直接用列表存储
PAGE = ['hot.html', 'hot-2.html', 'hot-3.html', 'hot-4.html', 'hot-5.html', 'hot-6.html', 'hot-7.html', 'hot-8.html',
        'hot-9.html', 'hot-10.html']
# 每次爬取间隔时间，控制爬取次数
T = 3
# 工作目录
# WORKSPACE = 'H:/DATA'
WORKSPACE = 'E:/data_lyz'
# 保存文件名
# WORKBOOKNAME = '红海行动时光网影评.xlsx'
# WORKBOOKNAME = '我和我的祖国时光网影评.xlsx'
# WORKBOOKNAME = '战狼2时光网影评.xlsx'
# WORKBOOKNAME = '流浪地球时光网影评.xlsx'
# WORKBOOKNAME = '哪吒之魔童降世时光网影评.xlsx'
# WORKBOOKNAME = '蜘蛛侠时光网影评.xlsx'
# WORKBOOKNAME = '复仇者联盟4影评.xlsx'
WORKBOOKNAME = '三块广告牌时光网影评.xlsx'
# WORKBOOKNAME = '至暗时刻时光网影评.xlsx'
# 设置工作目录
os.chdir(WORKSPACE)


# 通过url获取response处理后返回soup方法
def getSoup(url):
    # 获取网页response对象
    response = requests.get(url)
    # 乱码处理
    response.encoding = 'utf-8'
    # response.encoding = response.apparent_encoding
    # 监控网页状态
    response.raise_for_status()
    # 获取soup对象，BeautuifulSoup清洗数据
    soup = bs4.BeautifulSoup(response.text)
    # 为避免ip被封，限制每分钟爬取次数,每次调用后暂停2s
    time.sleep(T)
    return soup


# 获取用户信息 反爬取，爬不到
# def getUserInfo(url):
#     soup = getSoup(url)
#     logging.debug('soup:' + str(soup))
#     info_list = soup.select('.normal')
#     logging.debug('info_list:' + str(info_list))
#     # 为避免ip被封，限制每分钟爬取次数,每次调用后暂停2s
#     time.sleep(T)

# getUserInfo('http://my.mtime.com/5905659/')
# 创建workbook对象
workbook = openpyxl.Workbook()
# 获取当前sheet对象（表格）
sheet = workbook.get_active_sheet()
sheet['A1'] = '用户名'
sheet['A2'] = '评分'
sheet['A3'] = '评论'
sheet['A4'] = '评论时间'
for i in range(5,len(PAGE)):
    print('第', str(i), '页')
    url = URL + PAGE[i]
    soup = getSoup(url)
    '''评分'''
    score_list = soup.select('span.db_point.ml6')
    '''评论'''
    comment_list = soup.select('h3')
    '''用户链接'''
    user_html_list = soup.select('.pic_58>.px14>a')
    '''时间'''
    date_list = soup.select('.mt10>a')
    '''点赞数'''
    # up_list=soup.select('.com_good')
    # logging.debug('点赞数：'+str(up_list))
    for j in range(len(score_list)):
        print('第', str(j), '个评论')
        name = user_html_list[j].getText()
        score = score_list[j].getText()
        comment = comment_list[j].getText()
        data = date_list[j].get('entertime')
        # link = user_html_list[j].get('href')
        '''存储'''
        # 设置列号
        c = i*20+j + 2
        column = openpyxl.utils.get_column_letter(c)
        print('用户名：', name)
        sheet[column + '1'] = name
        print('评分：', score)
        sheet[column + '2'] = score
        print('评论：', comment)
        sheet[column + '3'] = comment
        print('评论时间：', data)
        sheet[column + '4'] = data
        # 设置表名
        sheet.title = '评论'
        # 保存文件
        workbook.save(WORKBOOKNAME)
        print('第', str(i), '页已存储')
        # print('用户链接：', link)
print('完成！')
