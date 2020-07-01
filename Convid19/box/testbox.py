# encoding=utf-8
"""
@Time : 2020/3/30 23:37 
@Author : LiuYanZhe
@File : testbox.py 
@Software: PyCharm
@Description: 箱线图测试
"""
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
np.random.seed(800)  # 设置随机种子
data = np.random.randint(1, 100, 55)
plt.figure(figsize=(5, 6))  # 设置图形尺寸大小
plt.boxplot(data,
            notch=False,  # 中位线处不设置凹陷
            widths=0.2,  # 设置箱体宽度
            medianprops={'color': 'red'},  # 中位线设置为红色
            boxprops=dict(color="blue"),  # 箱体边框设置为蓝色
            labels="A",  # 设置标签
            whiskerprops={'color': "black"},  # 设置须的颜色，黑色
            capprops={'color': "green"},  # 设置箱线图顶端和末端横线的属性，颜色为绿色
            flierprops={'color': 'purple', 'markeredgecolor': "purple", 'markersize': 3}  # 异常值属性，这里没有异常值，所以没表现出来
            )
plt.title("55个1-100的随机整数的箱线图", fontsize="xx-large", color="#DE0052")
plt.show()
