# encoding=utf-8
"""
@Time : 2020/3/27 22:37 
@Author : LiuYanZhe
@File : AllCountry_history_data.py 
@Software: PyCharm
@Description: 各国家历史数据
"""

import requests
import json
from Convid19.InternetWorm import Util
import pandas as pd
import time

province_data = pd.read_csv('../data/AllCountry_2020_03_27.csv')
province_dict = {num: name for num, name in zip(province_data['id'], province_data['name'])}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}  # 请求头

i = 0
start = time.time()
for province_id in province_dict:
    try:
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + str(province_id)  # 访问链接
        data_requests = requests.get(url, headers=headers)  # 发起请求，获得响应数据
        data_json = json.loads(data_requests.text)  # 格式转为json
        # 解析数据
        data = data_json['data']['list']  # list类型
        history_data = Util.get_data(data, ['date', 'lastUpdateTime'])
        history_data['name'] = province_dict[province_id]

        # 合并数据
        if i == 0:
            history_all_data = history_data
            i += 1
        else:
            history_all_data = pd.concat([history_all_data, history_data], axis=0)
            i += 1
        print('*' * 10, '第', str(i), '个', province_dict[province_id], '成功。该数据大小：', history_data.shape, '，总数据大小：',
              history_all_data.shape, '累计耗时：', round(time.time() - start), '*' * 10)
        Util.save_data(history_all_data, 'History_country')
        time.sleep(10)
    except:
        print('*' * 10, province_dict[province_id], 'wrong!', '*' * 10)
print('结束！')
