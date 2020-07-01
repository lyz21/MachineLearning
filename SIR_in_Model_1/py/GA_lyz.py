# encoding=utf-8
"""
@Time : 2020/5/7 16:42
@Author : LiuYanZhe
@File : GA_lyz.py
@Software: PyCharm
@Description: 使用遗传算法优化，寻找最优解
"""
from sko.GA import GA
from SIR_in_Model_1.py.SIR import SIR

Max = float("inf")  # 无穷大浮点数

country = SIR('意大利', 60431283)
length = country.get_data_length()


def loss_func1(start_add, test_num):
    start_add = int(start_add)
    test_num = int(test_num)
    if start_add + test_num >= length - 2:
        return Max
    country.set_start_sub(start_add)  # 设置起始数据
    italy_err = country.sir_main_nopic(forecast_add=test_num,
                                       test_num=test_num)  # 25656122.19997323
    print('italy_err:', italy_err)
    return italy_err


if __name__ == '__main__':
    ga = GA(func=loss_func1, n_dim=2, size_pop=50, max_iter=3, lb=[0, 0], ub=[length, length])  # 遗传算法求解
    best_x, best_y = ga.run()
    start_add = best_x[0]
    test_num = best_x[1]
    start_add = int(start_add)
    test_num = int(test_num)
    print('start_add:', start_add)
    print('test_num:', int(test_num))
    country.set_start_sub(start_add)
    err = country.sir_main(forecast_add=test_num + 10, test_num=test_num)
    print(err)
