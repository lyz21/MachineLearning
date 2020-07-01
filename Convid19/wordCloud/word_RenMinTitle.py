# encoding=utf-8
"""
@Time : 2020/3/31 11:01 
@Author : LiuYanZhe
@File : word_RenMinTitle.py 
@Software: PyCharm
@Description: 生成人民网50天新闻标题词云图
"""
from random import randint

from textrank4zh import TextRank4Keyword
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import pandas as pd
from Convid19.InternetWorm import Util
from matplotlib.image import imread


# 词云图字体颜色方法(黑色)
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # h = randint(0, 50)
    h = 0  # 色域
    # s = randint(0, 20)
    # l = randint(0, 20)
    flag = randint(0, 1)
    if flag == 0:
        s = int(100.0 * float(randint(0, 200)) / 255.0)  # 饱和度
        l = int(100.0 * float(randint(0, 10)) / 255.0)  # 明亮度
    else:
        s = int(100.0 * float(randint(0, 10)) / 255.0)
        l = int(100.0 * float(randint(0, 230)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)


data_arr = pd.read_csv('../data/RenMinTitle_all_2020_03_30.csv').iloc[:, :30].to_numpy().flatten()  # 转换为1为np类型

dic_keyWord_weight = {}
for sentence in data_arr:
    words = TextRank4Keyword()
    words.analyze(text=sentence, lower=True, window=3)
    keywords_list = words.get_keywords(3, word_min_len=2)
    for keywords in keywords_list:
        dic_keyWord_weight.setdefault(keywords.word, 0)
        dic_keyWord_weight[keywords.word] += keywords.weight * 40  # 按权重统计
        # dic_keyWord_weight[keywords.word] += 1  # 按词频统计
print(len(dic_keyWord_weight))
print(dic_keyWord_weight)

# 排序保存文件
# keywords_pd = pd.DataFrame([dic_keyWord_weight.keys(), dic_keyWord_weight.values()], index=['word', 'weight']).T
# keywords_pd = keywords_pd.sort_values(by='weight', ascending=False)
# dic_keyWord_weight = sorted(dic_keyWord_weight, key=dic_keyWord_weight.get)
# # print(keywords_pd)
# Util.save_data(keywords_pd, name='RenMin_keyWords2_data')

# 绘图
# font_path = 'C://Windows//Fonts//simhei.ttf'
font_path = 'C://Windows//Fonts//STXINGKA.TTF'
# kw_str = '今天 的 天气 真不错 啊，我们 一起 去 吃饭吧！'  # 你需要进行可视化的字符串
# color_mask = imread(os.getcwd() + "\\python.png")  # 读取背景图片
# color_mask = imread('word.jpg')   # 加载背景图（声称形状）
# color_mask = imread('wordCloud/python.png')
# 自带的stopwords关键词不起作用，直接删除字典中的词
stopwords = ['论坛', '全面', '广告', '召开', '攻坚', '习近平', '助力', '图片', '做好', '现场', '发布', '报道', '抓好', '来论', '来自', '乐购', '今日',
             '徐徐', '寻找',
             '金台', '作用', '维护', '彩云', '抓细']
for word in stopwords:
    dic_keyWord_weight.pop(word)
# 手动删除过小值
key_list = []
for key, value in dic_keyWord_weight.items():
    if value < 0.25 * 40:
        key_list.append(key)
for key in key_list:
    dic_keyWord_weight.pop(key)
print(len(dic_keyWord_weight))
cloud = WordCloud(
    # 设置字体，不指定就会出现乱码
    font_path=font_path,  # 这个路径是pc中的字体路径
    # 设置背景色
    # background_color='#383838',
    background_color='white',
    # color_func=random_color_func,
    # mode='RGBA',
    # colormap='Blues',  # 风格  Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r
    # 词云形状
    # mask=color_mask,
    # 允许最大词汇
    max_words=2000,
    # 缩放(可以控制字体的清晰度)
    scale=8,
    # 最大号字体
    max_font_size=170, width=1000, height=600,
    # stopwords=stopwords,
)
# word_cloud = cloud.generate(kw_str)  # 产生词云,输入的格式是以空格分隔的词语组成的字符串
word_cloud = cloud.generate_from_frequencies(dic_keyWord_weight)
word_cloud.to_file("../pic/wordCloud4.2.png")  # 保存图片
#  显示词云图片
# 从背景图片生成颜色值
# back_coloring = ImageColorGenerator(color_mask)
# plt.imshow(word_cloud.recolor(color_func=back_coloring))
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
