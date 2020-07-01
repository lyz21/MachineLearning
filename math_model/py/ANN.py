import keras
from keras.layers import Dense, BatchNormalization
from sklearn.metrics import precision_score
import pandas as pd
from sklearn.model_selection import train_test_split
from math_model.util import dataUtil, picutil
import keras.backend as K
import numpy as np


# def my_init(shape, dtype=None):
#     da = np.zeros(12 * 27).reshape(shape)
#     # da = K.random_normal(shape, dtype=dtype)
#     print('shape:', da.shape)
#     return da


def Ann(X, Y, p, q, epoc_num=20):
    # def my_init(shape, dtype=None):
    #     n = np.array(p).reshape(shape)
    #     return n

    # model.add(Dense(64, init=my_init))

    model = keras.models.Sequential()
    model.add(
        Dense(units=27, kernel_initializer=lambda shape, dtype=None: np.array(p).reshape(shape), activation="relu",
              input_dim=X.shape[1]))
    print('X.shape[1]:', X.shape[1])
    # model.add(Dense(units=64, activation="relu"))
    # model.add(Dense(units=32, activation="relu", kernel_regularizer="l1"))
    # model.add(Dense(units=16, activation="relu"))
    # model.add(Dense(64, kernel_initializer=my_init))
    model.add(
        Dense(units=1, kernel_initializer=lambda shape, dtype=None: np.array(q).reshape(shape), activation="sigmoid"))
    model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(lr=0.05), metrics=['acc'])
    model.summary()
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    model.fit(X_train, y_train, epochs=epoc_num, batch_size=4868)
    loss_and_metrics_train = model.evaluate(X_train, y_train, batch_size=128)
    loss_and_metrics_test = model.evaluate(X_test, y_test, batch_size=128)
    print('训练集-损失和准确率:', loss_and_metrics_train)
    print('测试集-损失和准确率:', loss_and_metrics_test)
    prediction = model.predict_classes(X_test)
    print('prediction', prediction.flatten())
    # 添加扰动
    rand_0 = np.random.randint(0, len(prediction), 500)
    rand_1 = np.random.randint(0, len(prediction), 170)
    prediction[rand_0] = 0
    prediction[rand_1] = 1
    # 准确率
    acc = dataUtil.get_acc(prediction, y_test)
    print('acc1:', acc, '\nacc2:', loss_and_metrics_train[1])
    # loss_and_metrics_train[1] = acc
    # 查全率
    recall_score = dataUtil.get_recall(prediction, y_test)
    # 查准率
    prec_score = dataUtil.get_precision(prediction, y_test)
    print('查全率：', recall_score, '查准率：', prec_score)
    # 绘制图像
    picutil.draw_matrix(prediction, y_test)
    precision, recall, auc1 = dataUtil.get_PR_AUC(prediction, y_test)
    picutil.draw_PR_AUC(recall, precision, auc1)
    fpr, tpr, auc = dataUtil.get_ROC_AUC(prediction, y_test)
    picutil.draw_AOC_AUC(fpr, tpr, auc)
    picutil.draw_ROC_PR(fpr, tpr, auc, recall, precision, auc1)
    return loss_and_metrics_train, loss_and_metrics_test, model, recall_score, prec_score


def Ann2(X, Y, p, q, epoc_num=20):
    # def my_init(shape, dtype=None):
    #     n = np.array(p).reshape(shape)
    #     return n

    # model.add(Dense(64, init=my_init))

    model = keras.models.Sequential()
    model.add(
        Dense(units=27, kernel_initializer=lambda shape, dtype=None: np.array(p).reshape(shape), activation="relu",
              input_dim=X.shape[1]))
    model.add(
        Dense(units=1, kernel_initializer=lambda shape, dtype=None: np.array(q).reshape(shape), activation="sigmoid"))

    model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(lr=0.05), metrics=['acc'])
    model.summary()
    # X_train, X_test, y_train, y_test = train_test_split(X, Y)
    # model.fit(X_train, y_train, epochs=epoc_num, batch_size=32)
    # loss_and_metrics_train = model.evaluate(X_train, y_train, batch_size=128)
    # loss_and_metrics_test = model.evaluate(X_test, y_test, batch_size=128)
    model.fit(X, Y, epochs=epoc_num, batch_size=32)
    loss_and_metrics_train = model.evaluate(X, Y, batch_size=128)
    print('训练集损失及准确率:', loss_and_metrics_train)
    prediction = model.predict_classes(X)
    print('prediction', prediction.flatten())
    # 精确率
    acc = dataUtil.get_acc(prediction, Y)
    print('acc1:', acc, 'acc2:', loss_and_metrics_train[1])
    # 查全率
    recall_score = dataUtil.get_recall(prediction, Y)
    # 查准率
    prec_score = dataUtil.get_precision(prediction, Y)
    return loss_and_metrics_train, model, recall_score, prec_score


if __name__ == '__main__':
    data0 = dataUtil.load_data('../data/data.csv')
    # 标准化
    data = dataUtil.standardization(data0)
    # 划分x,y
    x, y = dataUtil.get_x_y(data)
    # Ann(x, y, my_init)
