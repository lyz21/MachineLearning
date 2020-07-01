# encoding=utf-8
"""
@Time : 2019/10/18 16:35
@Author : LiuYanZhe
@File : BP_lyz.py
@Software: PyCharm
@Description:  BP神经网络的Python代码实现
sigmoid函数会将输出值固定在-1到1间，因此需要对原始数据归一化处理（将值固定在0-1间）
一层隐含层的三层神经网络
"""
import numpy
import random
import logging
import time

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# 禁用日志
# logging.disable()
'''全局变量'''
# 记录y的最大最小值，反归一化时用
Y_MAX = 0  # 一层时
Y_MIN = 0
Y_MAX_LIST = []  # 两层时
Y_MIN_LIST = []
# 定义各层节点数
INPUT_NUM = 18
HIDDEN_NUM = 37
OUTPUT_NUM = 3
# INPUT_NUM = 2
# HIDDEN_NUM = 10
# OUTPUT_NUM = 1
FLAG = 0
# 存储全局误差(存储加权后的，为了和未改进的作比较)
list_E = []
# 存储LearnRate
list_LearnRate = []
# 各个朝代训练数量
qing = 29
ming = 50
yuan = 83
# 各个朝代训练数量
qing_test = 11
ming_test = 18
yuan_test = 31
# 正确输出项扩大倍数
RIGHTRATE = 2.5


# 生成a-b间的随机数方法
def randNum(a, b):
    return random.random() * (b - a) + a


# 归一化X，两层，按列归一化
def normalX(x_list, a, b):
    x_arr = numpy.array(x_list)  # 列表转化为矩阵方便找最小值
    max_list = x_arr.max(0)
    min_list = x_arr.min(0)
    # logging.debug('归一化X:'+str(max_list))
    for i in range(len(x_list)):
        for j in range(len(x_list[i])):
            x_list[i][j] = a * (x_list[i][j] - min_list[j]) / (max_list[j] - min_list[j]) + b
    return x_list


# 归一化y，两层，按列归一化
def normalDY(y_list, a, b):
    y_arr = numpy.array(y_list)  # 列表转矩阵
    max_list = y_arr.max(0)
    min_list = y_arr.min(0)
    global Y_MAX_LIST, Y_MIN_LIST
    Y_MAX_LIST = max_list  # 存储最大最小值
    Y_MIN_LIST = min_list
    for i in range(len(y_list)):
        for j in range(len(y_list[i])):
            y_list[i][j] = a * (y_list[i][j] - min_list[j]) / (max_list[j] - min_list[j]) + b
    return y_list


# 反归一化y，两层
def normalDY_F(y_out_list, a, b):
    for i in range(len(y_out_list)):
        for j in range(len(y_out_list[i])):
            y_out_list[i][j] = (y_out_list[i][j] - b) * (Y_MAX_LIST[j] - Y_MIN_LIST[j]) / a + Y_MIN_LIST[j]
    return y_out_list


# 归一化Y，一层
def normalY(y_list, a, b):
    max_y = max(y_list)
    min_y = min(y_list)
    global Y_MIN, Y_MAX
    Y_MIN = min_y
    Y_MAX = max_y
    for i in range(len(y_list)):
        y_list[i] = a * (y_list[i] - min_y) / (max_y - min_y) + b
    return y_list


# 反归一化Y
def normalY_F(y_out_list, a, b):
    y_true_list = []
    for i in range(len(y_out_list)):
        temp = (y_out_list[i] - b) * (Y_MAX - Y_MIN) / a + Y_MIN
        y_true_list.append(temp)
    return y_true_list


# 加载数据方法
def loadData():
    # input_list = [[1, 2], [2, 3], [3, 6], [4, 1], [6, 2]]
    # output_list = [3, 5, 9, 5, 8]
    # input_list = [[0.1, 0.2], [0.2, 0.3], [0.3, 0.6], [0.4, 0.1], [0.6, 0.2]]
    # output_list = [0.3, 0.5, 0.9, 0.5, 0.8]
    input_list = numpy.loadtxt('data_input.txt').tolist()
    output_list = numpy.loadtxt('data_output.txt').tolist()
    # 归一化
    input_list = normalX(input_list, 1, 0)
    # output_list = normalY(output_list, 1, 0)
    return input_list, output_list


# 激励函数
def incentiveFun(a, x):
    if a == 1:
        return 1 / (1 + numpy.exp(-x))


# 激励函数的导数
def incentiveFunD(a, y):
    if a == 1:
        return y * (1 - y)


class BpNet:
    def __init__(self, iNum, hNum, oNum, flag=0):  # flag为随机赋值或外部赋值
        # logging.debug('---init---')
        # 设定激励函数类型
        self.methodType = 1
        # 初始化，iNum,hNum,oNum分别为输入层、隐含层、输出层个数
        self.inputNum = iNum
        self.hiddenNum = hNum
        self.outputNum = oNum
        # 定义各层节点，列表存储节点值（激活）
        self.input_list = [0.0] * iNum
        self.hidden_list = [0.0] * hNum
        self.output_list = [0.0] * oNum
        # 定义阈值
        self.hidden_threshold_list = [0.0] * hNum
        self.output_threshold_list = [0.0] * oNum
        if flag == 0:  # 若flag=0,随机赋值，否则单独调用set方法赋值
            # 为阈值随机赋值
            # print('阈值随机赋值')
            for i in range(self.hiddenNum):
                self.hidden_threshold_list[i] = randNum(-1.0, 1.0)
            for i in range(self.outputNum):
                self.output_threshold_list[i] = randNum(-1.0, 1.0)
        # 建立权值矩阵（使用NUmpy生成矩阵，转换为二维列表存储）
        # 从输入层到隐藏层的权值矩阵
        self.inHid_weight = numpy.ones((self.inputNum, self.hiddenNum)).tolist()
        # 从隐藏层到输出层的权值矩阵
        self.outhid_weight = numpy.ones((self.hiddenNum, self.outputNum)).tolist()
        if flag == 0:
            # print('权值随机赋值')
            # 为权值矩阵赋随机值
            for i in range(self.inputNum):
                for j in range(self.hiddenNum):
                    self.inHid_weight[i][j] = randNum(-1.0, 1.0)
            for i in range(self.hiddenNum):
                for j in range(self.outputNum):
                    self.outhid_weight[i][j] = randNum(-1.0, 1.0)
        # logging.debug('input_list:' + str(self.input_list))
        # logging.debug('hidden_list:' + str(self.hidden_list))
        # logging.debug('output_list:' + str(self.output_list))
        # logging.debug('inHid_weight:' + str(self.inHid_weight))
        # logging.debug('outhid_weight:' + str(self.outhid_weight))

    # 设置阈值与权值
    def setweightANDthreshold(self, output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight):
        # print('设定阈值与权值')
        self.hidden_threshold_list = hidden_threshold_list
        self.output_threshold_list = output_threshold_list
        self.inHid_weight = inHid_weight
        self.outhid_weight = outhid_weight

    '''正向传播'''

    # 通过公式计算神经网络的输出
    def update(self, data_list):
        # logging.debug('---update---')
        # 为输入层赋值(激活输入层)
        for i in range(self.inputNum):
            self.input_list[i] = data_list[i]
        # logging.debug('input_list:' + str(self.input_list))
        # 计算隐藏层的输出（激活隐藏层）
        for i in range(self.hiddenNum):
            hi = 0.0
            for j in range(self.inputNum):
                hi = hi + self.inHid_weight[j][i] * self.input_list[j]
            self.hidden_list[i] = incentiveFun(self.methodType,
                                               hi - self.hidden_threshold_list[i])  # 隐含层节点保存的是隐含层处理后的输出ho,计算输出层时要用
        # 计算输出层的输出（即网络的输出）（激活输出层）
        for i in range(self.outputNum):
            yi = 0.0
            for j in range(self.hiddenNum):
                yi = yi + self.outhid_weight[j][i] * self.hidden_list[j]
            self.output_list[i] = incentiveFun(self.methodType, yi - self.output_threshold_list[i])  # 输出层节点保存的是输出层的输出yo
        # logging.debug('hidden_list:' + str(self.hidden_list))
        # logging.debug('output_list:' + str(self.output_list))
        return self.output_list

    '''反向传播（修正权值）'''

    def backPropagate(self, rightOut_list, learnRate, flag=-1):  # 参数rightOut_list指 期望输出,learnRate指学习率
        # logging.debug('---backPropagate---')
        '''计算误差'''
        # 输出层误差
        outErr_list = [0.0] * self.outputNum
        for i in range(self.outputNum):
            # logging.debug('rightOut_list:'+str(rightOut_list))
            # logging.debug('self.output_list:'+str(self.output_list))
            temp = rightOut_list[i] - self.output_list[i]
            # print('第', i, '个:', rightOut_list[i])
            if i == flag:
                # print(temp)
                temp = temp * RIGHTRATE
                # print(temp)
                # print('加倍')
            outErr_list[i] = temp * incentiveFunD(self.methodType, self.output_list[i])

        # 隐藏层误差
        hidErr_list = [0.0] * self.hiddenNum
        for i in range(self.hiddenNum):
            hid_err = 0.0
            for j in range(self.outputNum):
                hid_err = hid_err + outErr_list[j] * self.outhid_weight[i][j]
            hidErr_list[i] = hid_err * incentiveFunD(self.methodType, self.hidden_list[i])
        '''更新权重'''
        # 更新隐含层到输出层权重
        for i in range(self.hiddenNum):
            for j in range(self.outputNum):
                self.outhid_weight[i][j] = self.outhid_weight[i][j] + learnRate * outErr_list[j] * self.hidden_list[i]
        # 更新输入层到隐含层权重
        for i in range(self.inputNum):
            for j in range(self.hiddenNum):
                self.inHid_weight[i][j] = self.inHid_weight[i][j] + learnRate * hidErr_list[j] * self.input_list[i]
        '''更新阈值'''
        # 更新隐藏层阈值
        for i in range(self.hiddenNum):
            self.hidden_threshold_list[i] = self.hidden_threshold_list[i] - learnRate * hidErr_list[i]
        # 更新输出层阈值
        for i in range(self.outputNum):
            self.output_threshold_list[i] = self.output_threshold_list[i] - learnRate * outErr_list[i]
        # 用误差函数计算误差e
        err = 0.0
        err_true = 0.0
        for i in range(self.outputNum):
            err_true = err_true + (rightOut_list[i] - self.output_list[i]) ** 2
            e = rightOut_list[i] - self.output_list[i]
            if i == flag:
                e = e * RIGHTRATE
            err = err + e ** 2
        e = err / 2
        e_true = err_true / 2
        # logging.debug('outhid_weight:' + str(self.outhid_weight))
        # logging.debug('inHid_weight:' + str(self.inHid_weight))
        # logging.debug('误差:' + str(self.inHid_weight))
        # print('输入', self.input_list, '期望输出：', str(rightOut_list), '实际输出：', self.output_list)
        # print('期望输出：', str(rightOut_list), '实际输出：', self.output_list)
        return e, e_true

    # 训练函数
    def train(self, x_list, y_list, max_iter=1000, min_E=0.00028, learnRate=0.1):
        # 存储原始学习率
        # learnRate_old=learnRate
        for i in range(max_iter):
            e = 0.0
            e_true = 0.0
            # 指数法动态更改学习率
            # learnRate=learnRate*numpy.exp(-0.01*i)
            # if i%10==0:
            # # 多项式法动态更改学习率
            #     learnRate=learnRate*(1+0.01*i)**(-0.05)
            #     list_LearnRate.append(learnRate)
            if i % 400 == 0:
                learnRate = learnRate * 0.5  # 训练次数每隔1000次，学习率减半(翻倍）
            for j in range(len(x_list)):
                # 正向传播
                self.update(x_list[j])
                if j < qing:
                    flag = 0
                elif j >= qing and j < qing + ming:
                    flag = 1
                elif j >= qing + ming and j < qing + ming + yuan:
                    flag = 2
                else:
                    flag = -1
                # 反向更新,统计误差
                if OUTPUT_NUM == 1:  # 若输出节点为1，是一维列表，需变成2维
                    y_temp = []
                    y_temp.append(y_list[j])
                    temp_e, temp_e_true = self.backPropagate(y_temp, learnRate, flag=flag)
                    e = e + temp_e
                    e_true = e_true + temp_e_true
                else:
                    temp_e, temp_e_true = self.backPropagate(y_list[j], learnRate, flag=flag)
                    e = e + temp_e
                    e_true = e_true + temp_e_true
            # 计算全局误差
            E = e / len(y_list)
            E_true = e_true / len(y_list)
            # list_E.append(E_true)
            list_E.append(E)
            # logging.debug('全局误差：' + str(E))
            # print('隐藏层阈值：', self.hidden_threshold_list, '\n输出层阈值：', self.output_threshold_list)
            if i % 100 == 0:  # 每100次存储并输出一次E
                if FLAG == 0:
                    # print('第 ', i, ' 次训练，全局误差：', str(E))
                    logging.debug('第 ' + str(i) + ' 次训练，全局误差：', str(E))
            # print('全局误差：', str(E))
            # 全局误差达到预设精度，结束算法
            if E <= min_E:
                break
        return E

    # 预测函数
    def pre(self, x_list, y_list):
        list_pre = []  # 存储预测值
        list_judge = []  # 存储比对结果
        list_rate = []  # 存储比例，依次为[正确比例，清朝正确比例，明朝正确比例，元朝正确比例]
        right_count = 0  # 存储正确数量
        right_qing_count = 0  # 存储清朝正确的数量
        right_ming_count = 0  # 存储明朝正确的数量
        right_yuan_count = 0  # 存储元朝正确的数量
        for i in range(len(x_list)):
            y_net = self.update(x_list[i])
            # y_net = normalY_F(y_net, 1, 0)  # 反归一化
            y_right = y_list[i]
            # print('预测值：', str(y_net), '真实值：', str(y_right))
            logging.debug('预测值：' + str(y_net) + '真实值：' + str(y_right))
            list_pre.append(y_net.copy())
            # 如果预测正确
            if y_net.index(max(y_net)) == y_right.index(max(y_right)):
                list_judge.append(1)
                right_count += 1
                if i < qing_test:  # 清朝的数据
                    right_qing_count += 1
                elif i >= qing_test and i < ming_test + qing_test:
                    right_ming_count += 1
                elif i >= ming_test + qing_test and i < yuan_test + ming_test + qing_test:
                    right_yuan_count += 1
            else:
                list_judge.append(0)
        # 计算比例
        allrate = right_count / (qing_test + ming_test + yuan_test)
        qingrate = right_qing_count / qing_test
        mingrate = right_ming_count / ming_test
        yuanrate = right_yuan_count / yuan_test
        list_rate.append(allrate)
        list_rate.append(qingrate)
        list_rate.append(mingrate)
        list_rate.append(yuanrate)
        list_count = [right_qing_count + right_ming_count + right_yuan_count, right_qing_count, right_ming_count,
                      right_yuan_count]
        # print('right_qing_count',right_qing_count)
        # print('right_ming_count',right_ming_count)
        # print('right_yuan_count',right_yuan_count)
        # print('judge:',list_judge)
        return list_pre, y_list, list_judge, list_rate, list_count


def main(name='_main', max_iter=2000, learnRate=0.05):
    startTime = time.time()
    # 实例Bp对象
    bp = BpNet(INPUT_NUM, HIDDEN_NUM, OUTPUT_NUM)
    # 加载数据
    x_list, y_list = loadData()
    # logging.debug('y_list:'+str(y_list))
    # 训练网络
    bp.train(x_list, y_list, max_iter=max_iter, learnRate=learnRate)
    numpy.savetxt('神经网络每百次训练全局误差' + name, list_E)
    # 预测
    # a = [[0.2, 0.1], [0.5, 0.4], [0.7, 0.1], [0.1, 0.1]]
    # b = [0.3, 0.9, 0.8, 0.2]
    # a = [[2, 1], [5, 4], [7, 1]]
    # b = [3, 9, 8]
    a = numpy.loadtxt('test_input.txt').tolist()
    b = numpy.loadtxt('test_output.txt').tolist()
    a = normalX(a, 1, 0)  # 归一化x
    list_pre, y_list, list_judge, list_rate, list_count = bp.pre(a, b)
    numpy.savetxt('BP_output_threshold_list.txt', bp.output_threshold_list)
    numpy.savetxt('BP_hidden_threshold_list.txt', bp.hidden_threshold_list)
    numpy.savetxt('BP_outhid_weight.txt', bp.outhid_weight)
    numpy.savetxt('BP_inHid_weight.txt', bp.inHid_weight)
    numpy.savetxt('预测结果' + name, list_pre)
    numpy.savetxt('正确结果' + name, y_list)
    numpy.savetxt('结果对比' + name, list_judge)
    numpy.savetxt('正确比例' + name, list_rate)
    print('预测正确数量（全部，清，明，元）：', list_count)
    print('预测正确比例（全部，清，明，元）：', list_rate)
    endTime = time.time()
    print('运行时间：', endTime - startTime)
    return list_rate[0]


def main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight, max_iter=1000, min_E=0.00028,
             learnRate=0.1, name='_蚁群'):
    # startTime = time.time()
    # 标志位，蚁群算法不要在控制框输出信息
    global FLAG
    FLAG = 0
    # 实例Bp对象
    bp = BpNet(INPUT_NUM, HIDDEN_NUM, OUTPUT_NUM, flag=1)
    bp.setweightANDthreshold(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight)
    # 加载数据
    x_list, y_list = loadData()
    # logging.debug('y_list:'+str(y_list))
    # 训练网络
    # print('bp.output_threshold_list:', bp.output_threshold_list)
    bp.train(x_list, y_list, max_iter=max_iter, min_E=min_E, learnRate=learnRate)
    numpy.savetxt('神经网络训练每百次全局误差E' + name, list_E)
    # 预测
    a = numpy.loadtxt('test_input.txt').tolist()
    b = numpy.loadtxt('test_output.txt').tolist()
    a = normalX(a, 1, 0)  # 归一化x
    list_pre, y_list, list_judge, list_rate, list_count = bp.pre(a, b)
    numpy.savetxt('BP_output_threshold_list.txt', bp.output_threshold_list)
    numpy.savetxt('BP_hidden_threshold_list.txt', bp.hidden_threshold_list)
    numpy.savetxt('BP_outhid_weight.txt', bp.outhid_weight)
    numpy.savetxt('BP_inHid_weight.txt', bp.inHid_weight)
    numpy.savetxt('预测结果' + name, list_pre)
    numpy.savetxt('正确结果' + name, y_list)
    numpy.savetxt('结果对比' + name, list_judge)
    numpy.savetxt('正确比例' + name, list_rate)
    print('预测正确数量（全部，清，明，元）：', list_count)
    print('预测正确比例（全部，清，明，元）：', list_rate)
    # endTime = time.time()
    # print('BP神经网络运行时间：', endTime - startTime)
    # 返回全部数量以计算画图
    list_all_count = [yuan + ming + qing, qing, ming, yuan]
    return list_rate, list_count, list_all_count, list_pre, y_list, list_E, list_LearnRate


# 通过预设权值与阈值，获得BP神经网络的误差（通过预设权值和阈值改进BP神经网络时,用误差作为衡量标准）
# 参数列表：（隐藏层阈值列表，输出层阈值列表,输入层到隐藏层权值列表,隐藏层到输出层权值列表）
def measure(hidden_threshold_list, output_threshold_list, inHid_weight, outhid_weight):
    # 标志位，蚁群算法不要在控制框输出信息
    global FLAG
    FLAG = 1
    # 实例Bp对象
    bp = BpNet(INPUT_NUM, HIDDEN_NUM, OUTPUT_NUM, flag=1)
    # 设置权值、阈值
    bp.setweightANDthreshold(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight)
    # bp.hidden_threshold_list = hidden_threshold_list
    # bp.output_threshold_list = output_threshold_list
    # bp.inHid_weight = inHid_weight
    # bp.outhid_weight = outhid_weight
    # 加载数据
    x_list, y_list = loadData()
    # 获得全局误差
    e = 0.0
    for j in range(len(x_list)):
        # 正向传播,获得输出结果
        output_list = bp.update(x_list[j])
        # 统计误
        err = 0.0
        if j < qing:
            flag = 0
        elif j >= qing and j < qing + ming:
            flag = 1
        elif j >= qing + ming and j < qing + ming + yuan:
            flag = 2
        for k in range(bp.outputNum):
            temp = y_list[j][k] - output_list[k]
            if temp == flag:
                temp = temp * RIGHTRATE
            err = err + temp ** 2
            # print(y_list[j][k],':',output_list[k])
        e = e + err / 2
    # 计算全局误差
    E = e / len(y_list)

    return E

# main()
