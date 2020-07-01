# encoding=utf-8
"""
@Time : 2020/3/29 14:35
@Author : LiuYanZhe
@File : RenMinTitle_data.py
@Software: PyCharm
@Description: 人民日报每日排名前30新闻标题爬取
"""
# 下载页面模块
import requests
# 分析页面
import bs4
# 控制运行时间
import time
from Convid19.InternetWorm import Util
import pandas as pd

#
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}  # 请求头
#
# month, day = 1, 1
# date_list = []
# title_list = []
# for i in range(88):
#     if (month == 1 or month == 3) and day > 31:  # 1月结束，到第2月,1.31没有
#         month += 1
#         day = 1
#     if month == 2 and day > 29:
#         month += 1
#         day = 1
#     if month == 4 and day > 30:
#         month += 1
#         day = 1
#     if day < 10:
#         day_str = '0' + str(day)
#     else:
#         day_str = str(day)
#     if month < 10:
#         month_str = '0' + str(month)
#     else:
#         month_str = str(month)
#     date = month_str + '-' + day_str
#     date_list.append(date)
#     url = 'http://paperpost.people.com.cn/all-rmrb-2020-' + date + '.html'  # 访问链接
#     response = requests.get(url)
#     # 防止乱码
#     response.encoding = response.apparent_encoding
#     soup = bs4.BeautifulSoup(response.text)
#     a_list = soup.select('a')
#     title_day_list = []
#     for a in a_list:
#         title = str(a.get('title')).replace('\r', '').replace('\n', '').replace(' ', '')
#         title_day_list.append(title)
#     title_list.append(title_day_list)  # title为2维矩阵
#     day += 1
#     time.sleep(10)
#     df_title = pd.DataFrame(title_list, index=date_list)
#     df_title = df_title.fillna('空')
#     Util.save_data(df_title, 'RenMIn_Title', filename='../data/', index=date_list)


# df1 = pd.read_csv('../data/RenMInTitle_2020_03_29.csv')
# month, day = 1, 1
# date_list = []
# for i in range(50):
#     if day >= 31:  # 1月结束，到第2月,1.31没有
#         month += 1
#         day = 1
#     if day < 10:
#         day_str = '0' + str(day)
#     else:
#         day_str = str(day)
#     if month < 10:
#         month_str = '0' + str(month)
#     else:
#         month_str = str(month)
#     date = month_str + '-' + day_str
#     date_list.append(date)
#     day += 1
# df1.index = date_list
# print(df1)
# df1.to_csv('RenMIn_Title_2020_03_29.csv', encoding='utf_8_sig')


# 1.27-1.30
# title_list = [['把疫情防控作为当前最重要的工作来抓', '绿水青山带来了金山银山（总书记来过我们家)', '贯彻习近平总书记重要讲话和中央政治局常委会会议精神进一步部署疫情防控工作',
#                '武汉力保患者“应收尽收”“应治尽治”(来自疫情防控一线的报道)', '驰援', '城乡融合撬动“美丽经济”(今日谈)'],
#               ['全国各级财政已投入112.1亿元用于疫情防控', '把人民群众生命安全和身体健康放在第一位', '团结带领广大人民群众坚决贯彻落实党中央决策部署紧紧依靠人民群众坚决打赢疫情防控阻击战',
#                '李克强到湖北武汉考察指导新型冠状病毒感染肺炎疫情防控工作', '国务院办公厅关于延长2020年春节假期的通知', '湖北充实基层救治力量（来自疫情防控一线的报道）', '别让谣言跑在科学前面(今日谈)',
#                '海拔5000米的坚守（新春走基层）', '小岛上的又一个春节（新春走基层）'],
#               ['习近平会见世界卫生组织总干事谭德塞', '关于加强党的领导、为打赢疫情防控阻击战提供坚强政治保证的通知', '让党旗在防控疫情斗争第一线高高飘扬党旗高高飘扬汇聚磅礴力量',
#                '冰刀升级新技术（新春走基层）', '搬迁开启新生活（新春走基层）', '不忘来路才能更好前行（今日谈）'],
#               ['构筑群防群治的严密防线', '牢记宗旨 勇挑重担 为打赢疫情防控阻击战作出贡献', '进一步研究疫情防控形势 部署有针对性加强防控工作', '坚定信心战疫情同舟共济筑防线', '生活必需品供应有保障',
#                '52支医疗队6097人增援湖北防控疫情（来自疫情防控一线的报道）', '隔绝疫情，凝聚真情（今日谈）']
#               ]

##########################################################################################

'''爬取的数据缺失部分，补充上'''


#
#
# # 生成日期方法
def getDateList(day_num, start_month=1, start_day=1):
    month, day = start_month, start_day
    date_list = []
    for i in range(day_num):
        if (month == 1 or month == 3) and day > 31:  # 1月结束，到第2月,1.31没有
            month += 1
            day = 1
        if month == 2 and day > 29:  # 1月结束，到第2月,1.31没有
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
        date = month_str + '_' + day_str
        date_list.append(date)
        day += 1
    return date_list


#
#
text = [['把疫情防控作为当前最重要的工作来抓', '绿水青山带来了金山银山（总书记来过我们家)', '贯彻习近平总书记重要讲话和中央政治局常委会会议精神进一步部署疫情防控工作',
         '武汉力保患者“应收尽收”“应治尽治”(来自疫情防控一线的报道)', '驰援', '城乡融合撬动“美丽经济”(今日谈)', '空', '空', '空',
         '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['全国各级财政已投入112.1亿元用于疫情防控', '把人民群众生命安全和身体健康放在第一位', '团结带领广大人民群众坚决贯彻落实党中央决策部署紧紧依靠人民群众坚决打赢疫情防控阻击战',
         '李克强到湖北武汉考察指导新型冠状病毒感染肺炎疫情防控工作', '国务院办公厅关于延长2020年春节假期的通知', '湖北充实基层救治力量（来自疫情防控一线的报道）',
         '别让谣言跑在科学前面(今日谈)',
         '海拔5000米的坚守（新春走基层）', '小岛上的又一个春节（新春走基层）',
         '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['习近平会见世界卫生组织总干事谭德塞', '关于加强党的领导、为打赢疫情防控阻击战提供坚强政治保证的通知', '让党旗在防控疫情斗争第一线高高飘扬党旗高高飘扬汇聚磅礴力量',
         '冰刀升级新技术（新春走基层）', '搬迁开启新生活（新春走基层）', '不忘来路才能更好前行（今日谈）', '空', '空', '空',
         '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['构筑群防群治的严密防线', '牢记宗旨 勇挑重担 为打赢疫情防控阻击战作出贡献', '进一步研究疫情防控形势 部署有针对性加强防控工作', '坚定信心战疫情同舟共济筑防线',
         '生活必需品供应有保障',
         '52支医疗队6097人增援湖北防控疫情（来自疫情防控一线的报道）', '隔绝疫情，凝聚真情（今日谈）', '空', '空',
         '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['为打赢疫情防控阻击战作出贡献', '村子变美了 机会增多了（总书记来过我们家）', '在严峻斗争实践中考察识别干部', '更大发挥医疗卫生和科技的利器作用 群策群力打赢疫情防控阻击战',
         '改革要常讲常新（今日谈）', '武汉雷神山医院建设进度完成40%', '湖北多方筹集医疗物资应对疫情（来自疫情防控一线的报道）', '空', '空',
         '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空', '空']
        ]
df1 = pd.read_csv('../data/RenMIn_Title_2020_04_06.csv')  # 加载爬的标题
# print(df1.iloc[:, 1:])
i = 26
for item in text:
    df1.iloc[i, 1:] = item
    i += 1
date_list = getDateList(len(df1))
print(date_list)
df1 = df1.iloc[:, 1:]
df1['date'] = date_list
df1.to_csv('../data/RenMinTitle_all_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv', index=None)
print(df1)
