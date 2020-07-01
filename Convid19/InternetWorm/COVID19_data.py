# encoding=utf-8
"""
@Time : 2020/3/27 14:38 
@Author : LiuYanZhe
@File : COVID19_data.py 
@Software: PyCharm
@Description: 新冠肺炎病例数据爬取（网易疫情）学习版
"""
import requests  # 网络请求
import pandas as pd  # 使用pandas保存数据
import json
import time  # 计时

pd.set_option('max_rows', 500)
# 设置请求头，伪装成浏览器（检查-->Network-->XHR-->选择name-->Headers-->user-agent）
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'  # ?t= 后面是一个时间戳，可以不需要
r = requests.get(url, headers=headers)  # 发起请求
# print(r.status_code)  # 查看请求状态
# print(r.text)  # 获取的文本
# print(type(r.text))  # 查看类型 （str类型）
# print(len(r.text))  # 查看长度
data_json = json.loads(r.text)  # 转化为json格式
# print(type(data_json))
# print(data_json)
# print(data_json['data'].keys)
data = data_json['data']
# print(data)
# print(type(data))  # 查看类型 （dic类型）
areaTree = data['areaTree']
# print('type:',type(areaTree), '；', areaTree)    # list类型
china_data = areaTree[2]
# print('type:', type(china_data), '；', china_data)  # dict类型
china_province_data = china_data['children']
# print('type:', type(china_province_data), '；', china_province_data)  # list类型
# list里面每个元素是一个字典，字典key值包括'today', 'total', 'extData', 'name', 'id', 'lastUpdateTime', 'children'
# print(china_province_data[0].keys())
# 查看每个省的数据
# for i in range(len(china_province_data)):
#     print(china_province_data[i]['name'], china_province_data[i]['total'], china_province_data[i]['lastUpdateTime'])
#     if i > 5:
#         break
# 获取可以直接取出的信息
info = pd.DataFrame(china_province_data)[['id', 'name', 'lastUpdateTime']]
# print(info.head())
# 获取当天信息
province_today_data = pd.DataFrame([province['today'] for province in china_province_data])
province_today_data.columns = ['today_' + column for column in province_today_data.columns]  # 重新设置列名
# print(province_today_data.head())
# 获取总信息
province_total_data = pd.DataFrame([province['total'] for province in china_province_data])
province_total_data.columns = ['total_' + column for column in province_total_data.columns]  # 重新设置列名
# print(province_total_data)
# 合并上面三个表
china_province_data = pd.concat([info, province_today_data, province_total_data], axis=1)
print(china_province_data.head())
# 保存数据
file_name = 'china_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
china_province_data.to_csv(file_name, index=None, encoding='utf_8_sig')
