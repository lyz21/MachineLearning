# encoding=utf-8
"""
Name:         douban250
Description:  
Author:       Administrator
Date:         2019/10/28
"""
# 下载页面模块
import requests
# 分析页面
import bs4
# 处理表格
import openpyxl
# 目录控制
import os
# 日志模块
import logging
# 随机数生成，用来模拟ip
import random
# 控制运行时间
import time

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

'''
全局变量
'''
# 工作目录
WORKPATH = "H:/python/bookTask"
# 下载链接
URL = 'https://movie.douban.com/top250?start='
# 页数
PAGENUM = 0
# 表名
SHEETNAME = '豆瓣电影250'
# 文件名
WORKBOOKNAME = '豆瓣电影250_2.xlsx'
# 记录当前写入行数
ROWNUM = 2
# 爬取间隔时间,2s
T = 2

'''
数据结构
'''
# 存储电影名
list_name = []
# 存储电影信息,dic_name={'电影名':dic_detail},dic_detail={'列名','信息'}
dic_name = {}
dic_detail = {}
# 存储评分,存储结构与上面一样
dic_star_name = {}
dic_star_detail = {}

'''
工作目录设置
'''
os.chdir(WORKPATH)

'''
方法
'''


# 去除字符串空格、换行方法
def delspace(string):
    # 去除换行
    string = string.replace('\n', '')
    # 去除空格
    string = string.replace(' ', '')
    string = string.replace('\xa0', '')
    # 去除两边空格
    string = string.strip()
    return string


# 去除字符串空格,不去换行方法
def delspace0(string):
    # 去除空格
    string = string.replace(' ', '')
    string = string.replace('\xa0', '')
    # 去除两边空格
    string = string.strip()
    return string


# j标记list下标
j = 0  # 存储信息用
k = 0  # 存储评分用
while True:
    '''
    获取页面数据
    '''
    # 更改页号，拼接URL
    openurl = URL + str(PAGENUM)
    logging.debug('openurl:' + openurl)
    # 为避免ip被封，限制每分钟爬取次数
    time.sleep(T)
    # 获取网页,得到response对象
    response = requests.get(openurl)
    # logging.debug('页面：'+response.text)
    # 防止乱码
    response.encoding = response.apparent_encoding
    # 监控获取网页状态
    response.raise_for_status()
    # 获取soup对象，用于分析网页
    soup = bs4.BeautifulSoup(response.text)
    # 直接在div下的a元素，找到电影名
    elems_name = soup.select('div>a')
    # 找div下的直接p元素，找到电影信息（导演、演员、时间、地区、类型）
    elems_detail = soup.select('div>p')
    # 找CSS class属性为star的
    elems_score = soup.select('.star')
    '''数据结构中存储数据'''
    # 存储电影名
    for i in range(7, len(elems_name) - 11):
        # 获取电影名
        movieName = str(elems_name[i].getText())
        # 去除空格、换行
        movieName = delspace(movieName)
        # 如果全是空格，跳过
        if movieName.isspace() or len(movieName) == 0:
            logging.debug('跳过')
            continue
        # 将电影名添加到list中
        logging.debug('movieName:' + movieName)
        list_name.append(movieName)
    logging.debug('++++++++++++++++++++++++长度=' + str(len(elems_detail)))
    '''存储电影信息'''
    # 循环读取页面中获得的信息
    for i in range(2, len(elems_detail), 2):
        logging.debug('---------i=' + str(i) + '')
        # 读取到信息结束前一个跳出，最后一个不是信息，不读取，同时防止越界
        if i == len(elems_detail) - 1:
            break
        # 获取电影信息
        movieDetail = str(elems_detail[i].getText())
        # 获取电影简介
        movieShort = str(elems_detail[i + 1].getText())
        # 去除空格，不去换行
        # movieDetail=delspace0(movieDetail)
        # 详细信息去两边空格
        movieDetail = movieDetail.strip()
        # 简介去除空格
        movieShort = delspace(movieShort)
        logging.debug('信息：' + movieDetail)
        logging.debug('简介：' + movieShort)
        # 全是空格，跳过
        if movieDetail.isspace() or len(movieDetail) == 0 or movieDetail == 'xa0':
            logging.debug('跳过')
            continue
        if movieShort.isspace() or len(movieShort) == 0:
            logging.debug('跳过')
            continue
        '''处理电影信息字符串'''
        # 通过换行先分成两部分，导演主演、时间/地区/类型，返回数据类型为列表
        temp_list = movieDetail.split('\n')
        # 导演和主演
        temp_temp_list = temp_list[0].split('主演')
        logging.debug('temp_temp_list:' + str(temp_temp_list) + 'temp_temp_list长度：' + str(len(temp_temp_list)))
        # 导演
        movieDirector = temp_temp_list[0]
        movieDirector = movieDirector.replace('导演:', '')
        if len(temp_temp_list) >= 2:
            # 主演
            movieActor = temp_temp_list[1]
            movieActor = movieActor.replace(':', '')
        else:
            # 主演
            movieActor = '...'
        # 时间/地区/类型
        temp_list = temp_list[1].split('/')
        # 时间
        movieTime = temp_list[0]
        # 地区
        moviePlace = temp_list[1]
        # 给地区加上/
        moviePlace = moviePlace.replace(' ', '/')
        # 类型
        movieType = temp_list[2]
        # 给类型加上/
        movieType = movieType.replace(' ', '/')
        # 去空格（因为要在地区中将空格变为/，所以只能最后去空格）
        movieDirector = delspace0(movieDirector)
        movieActor = delspace0(movieActor)
        movieTime = delspace0(movieTime)
        moviePlace = delspace0(moviePlace)
        movieType = delspace0(movieType)
        logging.debug(
            '\n导演：' + movieDirector + '\n主演：' + movieActor + '\n时间：' + movieTime + '\n地区：' + moviePlace + '\n类型：' + movieType)
        '''将处理过的信息存入字典'''
        # 详细信息存入字典
        dic_detail = {'导演': movieDirector, '主演': movieActor, '时间': movieTime, '地区': moviePlace, '类型': movieType,
                      '简介': movieShort}
        # 将字典存入外层字典1，key从list中取出
        dic_name.setdefault(list_name[j], dic_detail)
        # 下标后移一位
        j += 1
    # 评分和评论人数
    for i in range(len(elems_score)):
        # 获取评分和人数
        movieStar = str(elems_score[i].getText())
        # 去除空格
        movieStar = delspace0(movieStar)
        # 使用换行符分割
        temp_list = movieStar.split('\n')
        # 评分
        movie_Star = temp_list[0]
        # 人数
        movie_Peonum = temp_list[2]
        movie_Peonum = movie_Peonum.replace('人评价', '')
        logging.debug(str(temp_list))
        logging.debug('\n评分：' + movie_Star + '\n人数：' + movie_Peonum)
        # 将数据存储在数据结构中
        dic_star_detail = {'评分': movie_Star, '评论人数': movie_Peonum}
        dic_star_name.setdefault(list_name[k], dic_star_detail)
        # 列表下标后移一位
        k += 1
    # 跳转下一页
    PAGENUM = 25 + int(PAGENUM)
    # 最后一页结束
    if PAGENUM > 225:
        break
'''
数据存入excel
'''
'''
打开excel
'''
# 创建workbook对象
workbook = openpyxl.Workbook()
# 获取sheet对象
sheet = workbook.get_active_sheet()
# 设置表头
sheet['A1'] = '电影名'
sheet['B1'] = '导演'
sheet['C1'] = '主演'
sheet['D1'] = '评分'
sheet['E1'] = '评论人数'
sheet['F1'] = '时间'
sheet['G1'] = '地区'
sheet['H1'] = '类型'
sheet['I1'] = '简介'
'''
写入excel
'''
# 写入数据
for i in range(len(list_name)):
    # 详情字典
    dic_w_detail = dic_name[list_name[i]]
    # 评分字典
    dic_w_star = dic_star_name[list_name[i]]
    # 第一列	电影名
    sheet['A' + str(ROWNUM)] = list_name[i]
    # 第二列	导演
    sheet['B' + str(ROWNUM)] = dic_w_detail['导演']
    # 第三列	主演
    sheet['C' + str(ROWNUM)] = dic_w_detail['主演']
    # 第四列	评分
    sheet['D' + str(ROWNUM)] = dic_w_star['评分']
    # 第五列	评论人数
    sheet['E' + str(ROWNUM)] = dic_w_star['评论人数']
    # 第六列	时间
    sheet['F' + str(ROWNUM)] = dic_w_detail['时间']
    # 第七列	地区
    sheet['G' + str(ROWNUM)] = dic_w_detail['地区']
    # 第八列	类型
    sheet['H' + str(ROWNUM)] = dic_w_detail['类型']
    # 第九列	简介
    sheet['I' + str(ROWNUM)] = dic_w_detail['简介']
    # 下移一行
    ROWNUM += 1
# 设置表名
sheet.title = SHEETNAME
# 保存文件
workbook.save(WORKBOOKNAME)

"""
# 显示评分字典
logging.debug('============================')
logging.debug(str(dic_star_name))
"""
"""
# 显示资料字典
logging.debug('============================')
logging.debug(str(dic_name))
"""
'''
# 遍历list
for i in range(len(list_name)):
	logging.debug('电影名：'+list_name[i])
logging.debug('list_name长度：'+str(len(list_name)))
'''
print('完成！')
