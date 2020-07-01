# encoding=utf-8
"""
@Time : 2020/6/19 16:58 
@Author : LiuYanZhe
@File : dataUtil.py
@Software: PyCharm
@Description: 数据处理工具类
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, metrics
import numpy as np

# 加载数据
from sklearn.preprocessing import StandardScaler


def load_data(path):
    df = pd.read_csv(path)
    return df


# 离散化数据
def discretization(data):
    # 离散化年龄
    data.loc[data['age'] <= 40, 'age'] = 1
    data.loc[data['age'] > 60, 'age'] = 3
    data.loc[data['age'] > 3, 'age'] = 2
    # 计算BMI并离散化（离散化体重和身高）
    BMI = data['weight'] / np.power(data['height'] / 100, 2)
    data['BMI'] = BMI
    data.loc[data['BMI'] <= 18.5, 'BMI'] = 1  # 过轻
    data.loc[data['BMI'] >= 24, 'BMI'] = 3  # 过重
    data.loc[data['BMI'] > 3, 'BMI'] = 2  # 正常
    data.to_csv('../data/data_dis.csv')


# BMI
def save_BMI(data):
    BMI = data['weight'] / np.power(data['height'] / 100, 2)
    # data1 = data.iloc[:, :len(data.columns) - 1]
    data1 = data.iloc[:, :5]
    data1['BMI'] = BMI
    # data1['label'] = data['label']
    colums = data.iloc[:, 5:].columns
    data1[colums] = data[colums]
    data1.to_csv('../data/data_dis.csv')


# BMI
def get_BMI():
    data0 = load_data('../data/data.csv')
    BMI = data0['weight'] / np.power(data0['height'] / 100, 2)
    print(BMI)
    data1 = load_data('../data/finalAgeData.csv')
    data = data1.iloc[:, :len(data1.columns) - 2]
    data['BMI'] = BMI
    data['label'] = data1['label']
    data.to_csv('../data/data_dis.csv')
    return BMI


# 将数据划分为输入和输出
def get_x_y(data):
    return data.iloc[:, :len(data.columns) - 1].values, data.loc[:, 'label'].values


# 将数据划分为输入和输出
def get_x_y_pd(data):
    return data.iloc[:, :len(data.columns) - 1], data.loc[:, ['number', 'label']]


# k折交叉验证数据划分
def k_fold(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    return x_train, x_test, y_train, y_test


# 数据标准化
def standardization(data):
    length = len(data.columns)
    print('length:', length)
    colum_name = data.iloc[:, :length - 1].columns.values.tolist()
    print('colum_name:', colum_name)
    teenager_sns_zscore = pd.DataFrame(preprocessing.scale(data[colum_name]),
                                       columns=data[colum_name].columns)
    teenager_sns_zscore['label'] = data['label']
    return teenager_sns_zscore


# 数据标准化2:
def standardization2(data):
    ss = StandardScaler()
    std_data = ss.fit_transform(data)
    return std_data


# 数据正则化
def normalization(data):
    d = preprocessing.normalize(data)
    return d


# 数据归一化
def scale(data):
    d = preprocessing.scale(data)
    return d


# 计算ROC和AUC
def get_ROC_AUC(true_list, pre_list):
    # 假阳性率 fp, 真阳性率 tpr, 阈值 thresholds
    fpr, tpr, thresholds = metrics.roc_curve(true_list, pre_list, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    return fpr, tpr, auc


# 计算PR曲线和AUC
def get_PR_AUC(true_list, pre_list):
    # 假阳性率 fp, 真阳性率 tpr, 阈值 thresholds
    precision, recall, _thresholds = metrics.precision_recall_curve(true_list, pre_list)
    auc = metrics.auc(recall, precision)
    return precision, recall, auc


# 获得准确率acc
def get_acc(y_pre, y_true):
    # y = pd.DataFrame(y_pre - y_true)
    # acc = y[0].value_counts()[0] / len(y)
    acc = metrics.accuracy_score(y_true, y_pre)
    return acc


# 查准率
def get_precision(pre, true):
    score = metrics.precision_score(true, pre)
    return score


# 获得查全率
def get_recall(y_pre, y_true):
    rate = metrics.recall_score(y_true, y_pre)
    # y_pre = pd.DataFrame(y_pre)
    # y_true = pd.DataFrame(y_true)
    # rate = len(y_pre[y_pre['label'] == 1])/len(y_true[y_true['label'] == 1])
    return rate


def del_none_mean():
    data = load_data('../data/data_dis.csv')
    data = data.drop(data.columns[0], axis=1)
    data = data.drop(data.columns[0], axis=1)
    print(len(data.columns))
    data.to_csv('../data/data_dis.csv', index=None)


# 找a值大于92的
def find_92():
    data = load_data('../data/data.csv')
    data = data[(data['a'] > 92) & (data['label'] == 0)]
    num_list = {4609, 1538, 1025, 1540, 2561, 2572, 3598, 2586, 4125, 2082, 1577, 2606, 2095, 4147, 2555, 2617, 2619,
                2110, 1602, 2628, 1605, 3658, 3661, 2129, 1105, 2644, 4694, 2654, 2145, 4709, 2150, 4214, 2678, 1666,
                642, 2181, 2182, 2696, 1682, 1684, 2212, 2219, 2222, 2743, 2232, 4800, 2759, 4297, 2762, 4813, 3790,
                1233, 2257, 2259, 2773, 3801, 2779, 4318, 735, 1247, 2270, 2275, 4840, 2795, 4848, 4336, 2805, 4854,
                2808, 2811, 2820, 2824, 4875, 2316, 2828, 3352, 2841, 2848, 2851, 3876, 2852, 2856, 4905, 1337, 2363,
                2881, 2889, 841, 2385, 1874, 1362, 2905, 2399, 3936, 2405, 2407, 876, 1910, 2934, 1912, 2943, 2949,
                1416,
                1930, 4491, 2460, 1438, 1952, 2468, 1956, 3494, 1447, 2992, 1969, 1974, 2999, 2486, 4538, 1471, 3011,
                2504, 1992, 970, 969, 3020, 4047, 2002, 2004, 1494, 3033, 3034, 3036, 3037, 4574, 2017, 3553, 1507,
                3042,
                4073, 1521, 507, 3069}
    num = data['number'].values
    num_list.update(num)
    # print(num)
    # print(len(num))
    return num


# 合并两个excel
def merge_ex():
    yin_data = pd.read_excel('../data/data.xlsx', sheet_name='阴性')
    yang_data = pd.read_excel('../data/data.xlsx', sheet_name='阳性')
    # label_yang = np.ones((1, yang_data.shape[0])).flatten()
    # label_yin = np.zeros((1, yin_data.shape[0])).flatten()
    yang_data['label'] = 1
    yin_data['label'] = 0
    # 原列名
    # columns = yin_data.columns
    # print(columns)
    # 新列名
    columns = load_data('../data/data.csv').columns
    data = np.vstack((yin_data.values, yang_data.values))
    data = pd.DataFrame(data, columns=columns)
    # 重新编号
    num = np.arange(data.shape[0])
    print('num:', num)
    data['number'] = num
    data.loc[(data['sex'] == '男', 'sex')] = 1
    data.loc[(data['sex'] == '女', 'sex')] = 0
    data.to_csv('../data/data_nan.csv', index=None)
    return data


# 将数据划分为含空的和不含空的，并返回
def get_nan_nonan(data):
    # print(np.isnan(data.loc[2, 'cql']))
    data_nan = data[np.isnan(data['cql'])]
    data_no_nan = data[np.isnan(data['cql']) == False]
    # print('data_nan:', data_nan['cql'])
    # print('data_no_nan:', data_no_nan['cql'])
    return data_nan, data_no_nan, data_no_nan['cql']


# 合并两个pd类型的数组
def mer_t_pd(df1, df2):
    columns = df1.columns
    data = np.vstack((df1.values, df2.values))
    data = pd.DataFrame(data, columns=columns)
    # print(data)
    # print(data.shape)
    print(data)
    data.to_csv('../data/data_22.csv', index=None)


# 获得吕哲逻辑斯蒂回归结果
def get_lz_logit():
    logit_prediction = np.load('../data/logit_prediction.npy').flatten()
    logit_test = np.load('../data/logit_test.npy')
    precision, recall, auc1 = get_PR_AUC(logit_test, logit_prediction)
    fpr, tpr, auc2 = get_ROC_AUC(logit_test, logit_prediction)
    return precision, recall, auc1, fpr, tpr, auc2
# 获得郑捷结果
def get_zj_logit():
    logit_prediction = np.load('../data/rf_test.npy')
    logit_test = np.load('../data/rf_prediction.npy')
    precision, recall, auc1 = get_PR_AUC(logit_test, logit_prediction)
    fpr, tpr, auc2 = get_ROC_AUC(logit_test, logit_prediction)
    return precision, recall, auc1, fpr, tpr, auc2


if __name__ == '__main__':
    # 合并两个excel
    merge_ex()
    # 读取数据
    # data0 = load_data('../data/data_nan.csv')
    # get_nan_nonan(data0)
    # find_92(data0)
    # 标准化
    # data = standardization2(data0)
    # 正则化
    # data = normalization(data0)
    # print(data)
    # print(data0)
    # 获得BMI
    # get_BMI()
    # 离散化数据
    # discretization(data0)
    # 标准化
    # data = standardization(data0)
    # 拆分
    # x, y = get_x_y(data, start_sub=0)
    # print(x)
    # k折交叉拆分
    # x_train, x_test, y_train, y_test = k_fold(x, y)
    # print('x_train:', x_train)
    # print('x_test:', x_test)
    # print('x_train.shape:', x_train.shape)
    # print('x_test.shape:', x_test.shape)
    # del_none_mean()
