# encoding=utf-8
"""
@Time : 2020/4/26 19:03 
@Author : LiuYanZhe
@File : LSTM_test.py 
@Software: PyCharm
@Description: 尝试使用LSTM长短时记忆网络预测参数
"""
from numpy import array
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from SIR_Model_1.util import picUtil

'''
下面的split_sequence（）函数实现了这种行为，并将给定的单变量序列分成多个样本，其中每个样本具有指定的时间步长，输出是单个时间步。
'''


# split a univariate sequence into samples
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


if __name__ == '__main__':
    # define input sequence
    # raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    # print('raw_seq:', raw_seq)

    raw_seq = [0.28768322383769634, 1.0, 1.0, 0.5230408788345577, 0.5237288874129629,
               0.2643879859459332, 0.3667216565481836, 0.5767884960539678, 0.31855832485506974, 0.2511956207124517,
               0.4339584480892643, 0.2518319440851276, 0.19942783956380025, 0.27965099088079354, 0.273235707069078,
               0.20298025158689537, 0.2697112670030862, 0.25549504204587864, 0.21520395676864812, 0.15286340670787293,
               0.23713316516187574, 0.22874280517047618, 0.16966070666661157, 0.2164992444986777, 0.19114639374023548,
               0.14403985070218683, 0.1368428458762072, 0.17189622195762483, 0.16100959266165546, 0.16624943554442356,
               0.1652711558112592, 0.12734466980581008, 0.0943905747601689, 0.1036610491806471, 0.09671252076405894,
               0.10108675754554523, 0.09019560010016445, 0.0929240649515217, 0.06976856106575366, 0.06484774166675701,
               0.05794592469570027, 0.061406722387396105, 0.060902309406993815, 0.05827189584622032,
               0.05516220178915313,
               0.04476638530562804, 0.040322737062756166, 0.03888573169622872, 0.047248108914993356,
               0.04815140639595543,
               0.04482995959514859, 0.04947317948128873, 0.04031772097763628, 0.03140849299037388, 0.03284572692888336,
               0.02577595895153588, 0.0383569558983079, 0.039001505948782926]
    print('len(raw_seq):', len(raw_seq))
    # 设置时间步
    n_steps = 3
    # 按时间步划分为输入和输出
    X, y = split_sequence(raw_seq, n_steps)
    print('训练X:', X)
    print('训练Y:', y)

    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    # 定义模型
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))  # 隐藏层，输入，特征维
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # 训练模型
    model.fit(X, y, epochs=300, batch_size=1, verbose=2)  # 迭代次数，批次数，verbose决定是否显示每次迭代
    # demonstrate prediction
    # x_input = array([[0.03284572692888336, 0.02577595895153588, 0.0383569558983079],[0.02577595895153588, 0.0383569558983079, 0.039001505948782926]])

    x_input = X
    x_input = x_input.reshape((x_input.shape[0], x_input.shape[1], n_features))
    yhat_list = model.predict(x_input, verbose=0)
    # print('预测X_len:', len(x_input))
    # print('预测Y_len:', len(yhat_list))
    # print('预测X:', x_input)
    # print('预测Y:', yhat_list)

    pre_t = 50
    pre_x_input = raw_seq[len(raw_seq) - n_steps:]
    print('len(pre_x_input):', len(pre_x_input))
    # 保存预测的Y
    pre_Y = list(raw_seq[:n_steps]) + list(yhat_list)
    print('len(pre_Y):', len(pre_Y))
    print('pre_Y:', pre_Y)
    for i in range(n_steps, pre_t + n_steps, 1):
        print('第', str(i), '次循环')
        temp_x_input = array(pre_x_input[i - n_steps:])
        print('temp_x_input:', temp_x_input)
        print('预测X_', i, temp_x_input)
        temp_x_input = temp_x_input.reshape((1, n_steps, n_features))
        temp_yhat = model.predict(temp_x_input, verbose=0)
        print('预测Y_', i, temp_yhat)
        pre_x_input.append(temp_yhat[0])
        pre_Y.append(temp_yhat[0])
    pre_Y = np.array(pre_Y).flatten()
    print('raw_seq:', raw_seq)
    print('pre_Y:', pre_Y)
    print('len(raw_seq):', len(raw_seq))
    print('len(pre_Y):', len(pre_Y))
    picUtil.draw_two(raw_seq, pre_Y, xticks=np.linspace(1, len(pre_Y), len(pre_Y)), name1='real', name2='pre')
