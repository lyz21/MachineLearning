# encoding=utf-8
"""
@Time : 2020/3/27 20:00 
@Author : LiuYanZhe
@File : china_province_data.py 
@Software: PyCharm
@Description:  新冠肺炎病例 各国家 中国各省份今日新增和总数,中国历史数据
"""
import requests
import json
from Convid19.InternetWorm import Util  # 导入自己写的工具包

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}  # 请求头
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'  # 访问链接
data_requests = requests.get(url, headers=headers)  # 发起请求，获得响应数据
data_json = json.loads(data_requests.text)  # 格式转为json
# # 解析数据
# areaTree = data_json['data']['areaTree']
# # 读取各国家数据
# country_data = Util.get_data(areaTree, ['id', 'name', 'lastUpdateTime'])
# # 保存各国家数据
# Util.save_data(country_data, 'AllCountry')
# # 找到中国各省份数据
# china_data = areaTree[2]
# china_province_data = china_data['children']
# # 取出各省份数据
# province_data = Util.get_data(china_province_data, ['id', 'name', 'lastUpdateTime'])
# # 保存各省份数据
# Util.save_data(province_data, 'China_province')

'''中国历史数据'''
chinaDayList = data_json['data']['chinaDayList']
china_history_data = Util.get_data(chinaDayList, ['date', 'lastUpdateTime'])
Util.save_data(china_history_data, 'China_history')
