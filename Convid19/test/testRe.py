# encoding=utf-8
"""
@Time : 2020/4/2 13:34 
@Author : LiuYanZhe
@File : testRe.py 
@Software: PyCharm
@Description: 正则测试
"""
import re
import numpy as np

# data = r'root.SG || (root.SG = {});root.SG.query = "肺炎";root.SG.timePeriodType = "MONTH";root.SG.dataType = "SEARCH_ALL";root.SG.path = "\u002Findex\u002FsearchHeat";root.SG.data = {"pvList": [[{"kwdId": 12170, "pv": 2049732, "isPeak": 0, "date": 20200303, "id": 12114936098},{"kwdId": 12170, "pv": 1907327, "isPeak": 0, "date": 20200304, "id": 12114936078},{"kwdId": 12170, "pv": 1842964, "isPeak": 0, "date": 20200305, "id": 12114936079},                    {"avgWapPv": 1351676, "ratioWapChain": "-66.3%", "ratioWapMonth": "1604.3%", "ratioChain": "-64.6%","topPvDataList": [{"topPvDataVoList": null, "kwdName": "肺炎"}]};root.SG.wholedata = {"pvList": [[{"kwdId": 12170, "pv": 22251, "isPeak": 0, "date": 20160101, "id": 4275551093},dId": 12170, "pv": 40754, "isPeak": 0, "date": 20161128, "id": 4275551102},{"kwdId": 12170, "pv": 1353685, "isPeak": 0, "date": 20200329, "id": 12338439004},{"kwdId": 12170, "pv": 1195903, "isPeak": 0, "date": 20200330, "id": 12338439005},"infoList": [{"avgWapPv": 222273, "ratioWapChain": "-", "ratioWapMonth": "-", "ratioChain": "-","ratioMonth": "-", "avgPv": 235604, "kwdName": "肺炎","kwdSumPv": {"sumPv": 365893461}}],"topPvDataList": [{"topPvDataVoList": null, "kwdName": "肺炎"}]};}(this));'
# comp = re.compile(r'root.SG.wholedata =')
# text = comp.search(response.text).string

# string = '1234r356789'
# # pattern = '1.\d*'
# comp = re.compile('1.\d*')
# text = comp.search(string).group()
# # text = re.search(pattern, string).group()
# print(text)

# pattern1 = "cat"
# pattern2 = "bird"
# string = "dog runs to cat"
# print(re.search(pattern1, string))
# print(re.search(pattern2, string))

# str = '[[asdafafafgag]]123456'
# str2 = re.search('\[\[.*\]\]', str).group()
# print(str2)

data = '[[{"pv":22251,"isPeak":0,"date":20160101},"pv":2,"isPeak":0,"date":20160102}]]'
pv_list = re.findall('pv":\d*', data)
date_list = re.findall('date":\d*', data)
for i in range(len(pv_list)):
    pv_list[i] = int(pv_list[i].replace('pv":', ''))
    date_list[i] = date_list[i].replace('date":', '')
print(pv_list)
print(date_list)
