# encoding=utf-8
"""
@Time : 2020/4/21 21:19 
@Author : LiuYanZhe
@File : test_line.py 
@Software: PyCharm
@Description: 测试线性回归
"""
from sklearn import linear_model
import numpy as np
from SIR_Model_1.util import picUtil
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

beta = [1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 0.405466101962479, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06,
        1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 0.28768322383769634, 1.0, 1.0, 0.5230408788345577, 0.5237288874129629,
        0.2643879859459332, 0.3667216565481836, 0.5767884960539678, 0.31855832485506974, 0.2511956207124517,
        0.4339584480892643, 0.2518319440851276, 0.19942783956380025, 0.27965099088079354, 0.273235707069078,
        0.20298025158689537, 0.2697112670030862, 0.25549504204587864, 0.21520395676864812, 0.15286340670787293,
        0.23713316516187574, 0.22874280517047618, 0.16966070666661157, 0.2164992444986777, 0.19114639374023548,
        0.14403985070218683, 0.1368428458762072, 0.17189622195762483, 0.16100959266165546, 0.16624943554442356,
        0.1652711558112592, 0.12734466980581008, 0.0943905747601689, 0.1036610491806471, 0.09671252076405894,
        0.10108675754554523, 0.09019560010016445, 0.0929240649515217, 0.06976856106575366, 0.06484774166675701,
        0.05794592469570027, 0.061406722387396105, 0.060902309406993815, 0.05827189584622032, 0.05516220178915313,
        0.04476638530562804, 0.040322737062756166, 0.03888573169622872, 0.047248108914993356, 0.04815140639595543,
        0.04482995959514859, 0.04947317948128873, 0.04031772097763628, 0.03140849299037388, 0.03284572692888336,
        0.02577595895153588, 0.0383569558983079, 0.039001505948782926]
beta = np.array(beta).reshape(-1, 1)[39:]
size = len(beta)
t = np.linspace(1, size, size)
t = np.array(t).reshape(-1, 1)
# 建立线性回归模型
# sklearn一元一次拟合
# regr = linear_model.LinearRegression()
# # 拟合
# regr.fit(t, beta)
# a, b = regr.coef_, regr.intercept_
# print(a, b)
# # y = a * t + b
# y = regr.predict(t)

# numpy拟合
# coef 为系数，poly_fit 拟合函数
x = t.flatten()
y = beta.flatten()
size += 10
x2 = np.linspace(1, size, size)


# coef1 = np.polyfit(x, y, 1)
# poly_fit1 = np.poly1d(coef1)
# plt.plot(x, poly_fit1(x), 'g', label="一阶拟合")
# plt.show()
# print('一阶拟合:', poly_fit1)

# coef2 = np.polyfit(x, y, 2)
# poly_fit2 = np.poly1d(coef2)
# plt.plot(x, poly_fit2(x), 'b', label="二阶拟合")
# plt.show()
# print('二阶拟合:', poly_fit2)

# coef3 = np.polyfit(x, y, 3)
# poly_fit3 = np.poly1d(coef3)
# plt.plot(x, poly_fit3(x), 'y',label="三阶拟合")
# plt.show()
# print(poly_fit3)

# 对数拟合

# picUtil.draw_two(beta, poly_fit2(x2), 'real', 'pre')

def fun_ln(x, a, b, c):
    y = a * np.log(b * x) + c
    return y


popt, pcov = curve_fit(fun_ln, x, y,
                       bounds=([-10, 0.000001, -20], [10, 10., 20]))  # popt为拟合得到的参数,pcov是参数的协方差矩阵,bonds为参数范围
print('popt:', popt, '\npcov:', pcov)
a, b, c = popt
picUtil.draw_two(beta, fun_ln(x2, a, b, c), 'real', 'pre')
