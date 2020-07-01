# encoding=utf-8
"""
@Time : 2020/6/22 10:19 
@Author : LiuYanZhe
@File : Tree.py 
@Software: PyCharm
@Description: 决策树可视化
"""
import numpy as np

import pandas as pd
from graphviz import render
from sklearn import tree
import pydotplus
from sklearn import metrics
from math_model.util import dataUtil
import graphviz
import os

os.environ["PATH"] += os.pathsep + 'E:/Program Files (x86)/Graphviz 2.28/bin/'  # 注意修改你的路径


def lrisTrain():
    data0 = dataUtil.load_data('../data/data.csv')
    data = data0.iloc[:, 1:]
    str = ['number', 'cql', 'vitalCapacity', 'a', 'zxqdcs', 'age', 'BMI', 'label']
    data = data[str]
    # 标准化
    # data = dataUtil.standardization(data)
    print('*' * 10, 'data(标准化之后)')
    print(data.head(10))
    # 把数据分为测试数据和验证数据
    # 划分x,y
    x, y = dataUtil.get_x_y(data)
    print('*' * 10, 'x')
    print(x)
    print('*' * 10, 'y')
    print(y)
    # 划分训练集测试集
    train_data, test_data, train_target, test_target = dataUtil.k_fold(x, y)
    print('*' * 10, 'train_data')
    print(train_data)
    print('*' * 10, 'test_data')
    print(test_data)
    print('*' * 10, 'train_target')
    print(train_target)
    print('*' * 10, 'test_target')
    print(test_target)
    # Model(建模)-引入决策树
    # 决策树
    # clf = tree.DecisionTreeClassifier(criterion="entropy")
    # AdaBoost
    clf = tree.DecisionTreeRegressor()
    # clf = tree.AdaBoostClassifier(
    #     base_estimator=tree.DecisionTreeClassifier(max_depth=5, min_samples_split=30, min_samples_leaf=5),
    #     n_estimators=10, learning_rate=0.2)
    # 训练集进行训练
    clf.fit(train_data, train_target)
    # # 进行预测
    y_pred = clf.predict(test_data)
    # # 法一：通过准确率进行验证
    print(metrics.accuracy_score(y_true=test_target, y_pred=y_pred))
    # 画图方法1-生成dot文件
    # with open('treeone.dot', 'w') as f:
    #     dot_data = tree.export_graphviz(clf, out_file=None)
    #     f.write(dot_data)
    # 画图方法2-生成pdf文件
    # dot_data = tree.export_graphviz(clf, out_file=None, feature_names=clf.feature_importances_,
    #                                 filled=True, rounded=True, special_characters=True)
    dot_data = tree.export_graphviz(clf, out_file=None, filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    # # 保存图像到pdf文件
    graph.write_pdf("treetwo.pdf")

    # # Verify(验证)

    # # 法二：通过混淆矩阵验证（横轴：实际值，纵轴：预测值）（理想情况下是个对角阵）
    # print(metrics.confusion_matrix(y_true=test_target, y_pred=y_pred))
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data)
    # graph.render("iris")


lrisTrain()
