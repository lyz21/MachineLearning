# encoding=utf-8
"""
@Time : 2020/4/19 16:17 
@Author : LiuYanZhe
@File : SIR_test1.py 
@Software: PyCharm
@Description: 数据酷客，SIR模型学习1
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint  # 求解微分方程
from scipy.optimize import minimize  # 优化

# 设置人群总人数为N
N = 58000000
# 设置初始时的感染人数I0为239
I0 = 239
# 设置初始时的恢复人数R0为31
R0 = 31
# 所以，初始易感者人群人数 = 总人数 - 初始感染人数 - 初始治愈人数
S0 = N - I0 - R0
# 设置初始值
y0 = [S0, I0, R0]
# 设置估计疫情的时间跨度为60天,# 1-360分成360份
# t = np.linspace(1, 60, 60)
t = np.linspace(1, 360, 360)
# 设置beta值等于0.125
beta = 0.125
# 设置gamma的值等于0.05
gamma = 0.05

# 要求Python的所有输出不用科学计数法表示
np.set_printoptions(suppress=True)


#   我们定义函数的名称为SIR
def SIR(y, t, beta, gamma):
    S, I, R = y
    dSdt = -S * beta / N
    dIdt = S * beta / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def loss(parameters, infectious, recovered, y0):
    # 确定训练模型的天数
    size = len(infectious)
    # 设置时间跨度
    t = np.linspace(1, size, size)
    beta, gamma = parameters
    # 计算预测值
    solution = odeint(SIR, y0, t, args=(beta, gamma))
    # 计算每日的感染者人数的预测值和真实值的均方误差
    l1 = np.mean((solution[:, 1] - infectious) ** 2)  # np.mean 取均值
    # 计算每日的治愈者人数的预测值和真实值之间的均方误差
    l2 = np.mean((solution[:, 2] - recovered) ** 2)
    # 返回SIR模型的损失值
    return l1 + l2


infectious_train = [10, 20, 30, 40, 50]
recovered_train = [5, 6, 7, 8, 9]
# 训练模型
optimal = minimize(loss, [0.0001, 0.0001],
                   args=(infectious_train, recovered_train, y0),
                   method='L-BFGS-B',
                   bounds=[(0.00000001, 1), (0.00000001, 1)])
beta, gamma = optimal.x
# 输出beta、gamma值
print('[beta,gamma]:', [beta, gamma])
# 求解
# odeint()函数是scipy库中一个数值求解微分方程的函数,函数需要至少三个变量，第一个是微分方程函数，第二个是微分方程初值，第三个是微分的自变量
solution = odeint(SIR, y0, t, args=(beta, gamma))
# 输出结果的前四行进行查看
# print(solution[0:4, :])
print(solution)

# 绘图展示

fig, ax = plt.subplots(facecolor='w', dpi=100)

for data, color, label_name in zip([solution[:, 1], solution[:, 2]], ['r', 'g'],
                                   ['infectious(dIdt)', 'recovered(dRdt)']):
    ax.plot(t, data, color, alpha=0.5, lw=2, label=label_name)

ax.set_xlabel('Time/days')
ax.set_ylabel('Number')
ax.legend()
ax.grid(axis='y')
plt.box(False)
plt.show()
