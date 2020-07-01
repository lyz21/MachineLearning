# encoding=utf-8
"""
@Time : 2020/2/4 14:19 
@Author : LiuYanZhe
@File : CV.py 
@Software: PyCharm
@Description: 产生交叉验证法使用的数据
"""
import numpy as np
import logging

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable()

# 统计数据中各朝代比例，以分层抽样
def count_rate(data):
    # 记录元、明、清朝数据的下标
    y_list = []
    m_list = []
    q_list = []
    data_output = data[:, -3:].tolist()
    for i in range(len(data_output)):
        sub = data_output[i].index(max(data_output[i]))
        if sub == 0:
            q_list.append(i)
        elif sub == 1:
            m_list.append(i)
        else:
            y_list.append(i)
    return y_list, m_list, q_list


class dataOperate_CV:
    def __init__(self, path='data/data.txt', k=10):
        # 加载数据
        self.data = np.loadtxt(path)
        self.k = k
        logging.debug('k:'+str(k))
        # 将数据划分为k个相似的互斥子集
        # 下标列表，用来选择
        # list_sub = list(range(len(self.data)))
        data_length = len(self.data)
        # 记录划分过后的各个子集
        list_all = []
        # 计算每个子集元素个数n
        n = int(np.ceil(len(self.data) / self.k))
        # 统计各朝代比例
        yuan_list, ming_list, qing_list = count_rate(self.data)
        # 计算各朝代选取样本数
        yuan_num = int(n * len(yuan_list) / len(self.data))
        # 四舍五入
        if n * len(yuan_list) / len(self.data) - yuan_num > 0.4:
            yuan_num += 1
        ming_num = int(n * len(ming_list) / len(self.data))
        # 四舍五入
        if n * len(ming_list) / len(self.data) - yuan_num > 0.4:
            yuan_num += 1
        for i in range(self.k):
            logging.debug('i:'+str(i))
            # 临时保存当前形成的子集
            temp_list = []
            if n > data_length:
                n = data_length
                yuan_num = len(yuan_list)
                ming_num = len(ming_list)
            # 每次选择n行存入
            for j in range(n):
                # 挑选元朝
                if j < yuan_num:
                    # 随机选择一个data的下标
                    sub = yuan_list[np.random.randint(len(yuan_list))]
                    # 将该下标的这一行保存到临时子集中
                    temp_list.append(self.data[sub].tolist())
                    # 将该行从待选集中删除
                    yuan_list.remove(sub)
                    data_length -= 1
                # 挑选明朝
                elif j >= yuan_num and j < yuan_num + ming_num:
                    # 随机选择一个data的下标
                    sub = ming_list[np.random.randint(len(ming_list))]
                    # 将该下标的这一行保存到临时子集中
                    temp_list.append(self.data[sub].tolist())
                    # 将该行从待选集中删除
                    ming_list.remove(sub)
                    data_length -= 1
                # 挑选清朝
                elif len(qing_list) > 0:
                    # 随机选择一个data的下标
                    sub = qing_list[np.random.randint(len(qing_list))]
                    # 将该下标的这一行保存到临时子集中
                    temp_list.append(self.data[sub].tolist())
                    # 将该行从待选集中删除
                    qing_list.remove(sub)
                    data_length -= 1
            list_all.append(temp_list)
        self.list_all = list_all

    # 分割数据（分割出输入数据和输出数据）
    def divide_outAndIn(self, data):
        data_input = data[:, :-3]
        data_output = data[:, -3:]
        return data_input, data_output

    # 将数据分为测试集和训练集,第i个为测试集,分成k个子集
    def divide_testAndTrain(self, i):
        # 获取划分后的k个子集
        list_div = self.list_all
        # 分离测试集
        list_test = list_div[i]
        # 分离训练集
        list_train = []
        for m in range(len(list_div)):
            if i == m:
                continue
            for n in range(len(list_div[m])):
                list_train.append(list_div[m][n])
        return list_test, list_train

    # 获取划分后的训练集和测试集的输入和输出
    def divide_testAndtrain_inAndOut(self, i):
        list_test, list_train = self.divide_testAndTrain(i)
        list_test_in, list_test_out = self.divide_outAndIn(np.array(list_test))
        list_train_in, list_train_out = self.divide_outAndIn(np.array(list_train))
        return list_test_in, list_test_out, list_train_in, list_train_out
