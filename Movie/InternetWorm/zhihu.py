# encoding=utf-8
"""
Name:         zhihu
Description:  爬取知乎电影评论
Author:       LiuYanZhe
Date:         2019/10/29
"""
# 下载页面
import requests
# 清洗数据
import bs4
# 日志模块
import logging

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志模块
# logging.disable()
'''全局变量'''
URL = 'https://www.zhihu.com/question/275224277'      # 知乎 有反爬取
# URL='https://maoyan.com/films/1182552'  # 猫眼  有反爬取
# URL='https://www.tiexue.net/'   # 铁血    可爬
# 获取网页response对象
response = requests.get(URL)
# 乱码处理
response.encoding = 'utf-8'
# response.encoding = response.apparent_encoding
# 监控网页状态
response.raise_for_status()
# 获取soup对象，BeautuifulSoup清洗数据
soup = bs4.BeautifulSoup(response.text)
logging.debug('soup: '+str(soup))