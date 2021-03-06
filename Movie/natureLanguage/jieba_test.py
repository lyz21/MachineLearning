# encoding=utf-8
"""
@Time : 2019/10/26 21:17
@Author : LiuYanZhe
@File : jieba_test.py
@Software: PyCharm
jieba 分词器
"""
import jieba
# str='邓超救不起这暑期档，哪吒可以'
str='看到海报和预告片，人们第一反应就是：哪吒太丑了。 觉得丑就对了，因为本片讲的就是打破偏见。 正如很多人一看这是国漫，就不看了；或者去看了，看了觉得还不错也要自动先扣20分。 电影之中，骂哪吒是政治正确，只要你说哪吒是妖怪，就会有人跟着说； 电影之外，骂国产片、国漫也成了政治正确，只要你骂它，就会有人给你点赞。 其实哪吒不是妖怪，他也想降妖除魔洗清骂名； 国漫也不都是烂片，也有人想拍一部佳作证明自己。 比如这部《哪吒》。 山河社稷图一幕真是天马行空，震撼无比，将曾经只存在于想象中的物品具象化，也将中国神话的无穷想象力展现得淋漓尽致。 那些耳熟能详的故事，不再只是故事，而是能看到，能听到，能享受一场视觉盛宴。 今年有《哪吒》，明年有《姜子牙》，封神电影宇宙即将开启。 是时候以电影的形式让中国文化走向世界了'
# cut方法，三个参数，分别是 待切割字符串 是否使用全模式 是否使用HMM模型，默认使用精确模式
list1 = jieba.cut(str, cut_all=False)   # 看到/海报/和/预告片/，/人们/第一/反应/就是/：/哪吒/太丑/了/...
print('精确模式：', '/'.join(list1))
list2 = jieba.cut(str, cut_all=True)    # 看到/海报/和/预告/预告片///人们/第一/反应/就是///哪吒/太丑/了...
print('全模式：', '/'.join(list2))
# cut_for_search 搜索引擎模式 共两个参数 待切割字符串  是否使用HMM模型
list3 = jieba.cut_for_search(str)   # 看到/海报/和/预告/预告片/，/人们/第一/反应/就是/：/哪吒/太丑/了/...
print('搜索引擎模式：', '/'.join(list3))