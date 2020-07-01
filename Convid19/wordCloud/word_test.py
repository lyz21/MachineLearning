# encoding=utf-8
"""
@Time : 2020/3/31 10:53 
@Author : LiuYanZhe
@File : word_test.py 
@Software: PyCharm
@Description: 词云图测试版
"""

import os

from matplotlib.image import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

data_pd = pd.read_csv('../data/RenMin_keyWords_data_2020_03_29.csv')
data_np = data_pd.values
print(data_np)

# font_path = 'C://Windows//Fonts//simhei.ttf'
font_path = 'C://Windows//Fonts//STXINGKA.TTF'
# kw_str = '今天 的 天气 真不错 啊，我们 一起 去 吃饭吧！'  # 你需要进行可视化的字符串
# color_mask = imread(os.getcwd() + "\\python.png")  # 读取背景图片
# color_mask = imread('python.png')
# color_mask = imread('panzi.jpg')
cloud = WordCloud(
    # 设置字体，不指定就会出现乱码
    font_path=font_path,  # 这个路径是pc中的字体路径
    # 设置背景色
    background_color='white',
    # 词云形状
    # mask=color_mask,
    # 允许最大词汇
    max_words=2000,
    # 最大号字体
    max_font_size=40, width=600, height=600
)
# word_cloud = cloud.generate(kw_str)  # 产生词云,输入的格式是以空格分隔的词语组成的字符串
word_cloud = cloud.generate_from_frequencies({'a': 20, 'b': 4})
word_cloud.to_file("pjl_cloud4.png")  # 保存图片
#  显示词云图片
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
