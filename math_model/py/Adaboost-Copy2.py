#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
import sklearn.model_selection as ms
import sklearn.svm as svm  # 导入svm函数
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

# In[2]:


# #加载数据
train = pd.read_csv('../data/data_dis.csv', index_col=0)
# print(train)
attr = ['cql', 'vitalCapacity',  'a', 'zxqdcs', 'age', 'BMI']
x = train[attr]
y = train['label']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=666)


print(x)



from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier


def ada_classifier(train_data, train_label, test_data):
    '''
    input:train_data(ndarray):训练数据
          train_label(ndarray):训练标签
          test_data(ndarray):测试标签
    output:predict(ndarray):预测结果
    '''
    # ********* Begin *********#
    ada = AdaBoostClassifier(base_estimator=DecisionTreeClassifier
    (max_depth=6, min_samples_split=10, min_samples_leaf=5),
                             n_estimators=50, learning_rate=0.2)
    ada.fit(train_data, train_label)
    predict = ada.predict(test_data)
    # ********* End *********#
    return predict

a = ada_classifier(x_train, y_train, x_test)


print(y_test)


accuracy_score(y_test, a)

from sklearn.model_selection import cross_val_score

ada = AdaBoostClassifier(base_estimator=DecisionTreeClassifier
(max_depth=5, min_samples_split=30, min_samples_leaf=5),
                         n_estimators=10, learning_rate=0.2)
scores = cross_val_score(ada, x, y)
print(scores)
