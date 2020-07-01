# encoding=utf-8
"""
@Time : 2020/6/19 19:46 
@Author : LiuYanZhe
@File : picutil.py 
@Software: PyCharm
@Description: 绘图工具类
"""
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from math_model.util import dataUtil


# 混淆矩阵
def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.binary, labels=['阴性', '阳性']):
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('真实标签')
    plt.xlabel('预测标签')


def draw_matrix(pre_data, true_data, name='混淆矩阵'):
    labels = ['0', '1']
    tick_marks = np.array(range(len(labels))) + 0.5
    cm = confusion_matrix(pre_data, true_data)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure()
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)

    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = cm_normalized[y_val][x_val]
        if c > 0.01:
            plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=10, va='center', ha='center')
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)

    plot_confusion_matrix(cm_normalized, title=name)
    plt.savefig('../pic/matrix.png', dpi=400, bbox_inches='tight')
    plt.show()


# ROC、AUC
def draw_AOC_AUC(fpr, tpr, auc):
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    lw = 1
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(fpr, tpr, color='k', lw=lw, linestyle='-', label='ROC curve (area = %0.2f)' % auc)
    ax1.plot([0, 1], [0, 1], color='k', lw=lw, linestyle='--')
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.0])
    ax1.set_xlabel('假阳性率')
    ax1.set_ylabel('真阳性率')
    ax1.set_title('ROC曲线')
    plt.legend(loc="lower right")
    plt.savefig('../pic/ROC.png', dpi=400, bbox_inches='tight')
    plt.show()


# PR、AUC
def draw_PR_AUC(recall, precision, auc):
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    lw = 1
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(recall, precision, color='k', lw=lw, linestyle='-', label='PR curve (area = %0.2f)' % auc)
    ax1.plot([0, 1], [1, 0], color='k', lw=lw, linestyle='--')
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.0])
    ax1.set_xlabel('召回率')
    print('recall:', recall)
    ax1.set_ylabel('精准率')
    ax1.set_title('P-R曲线')
    plt.legend(loc="lower right")
    plt.savefig('../pic/PR.png', dpi=400, bbox_inches='tight')
    plt.show()


def draw_ROC_PR(fpr, tpr, auc1, recall, precision, auc2):
    # lz数据
    precision_lz, recall_lz, auc1_lz, fpr_lz, tpr_lz, auc2_lz = dataUtil.get_lz_logit()
    lz_color = 'g'
    # zj数据
    precision_zj, recall_zj, auc1_zj, fpr_zj, tpr_zj, auc2_zj = dataUtil.get_zj_logit()
    zj_color = 'b'
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    lw = 1
    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(1, 2, 1)
    # lyz线
    ax1.plot(fpr, tpr, color='r', lw=lw, linestyle='-', label='ANN ROC curve (area = %0.2f)' % auc1)
    # lz线
    ax1.plot(fpr_lz, tpr_lz, color=lz_color, lw=lw, linestyle='-', label='Logistic ROC curve (area = %0.2f)' % auc1_lz)
    # zj线
    ax1.plot(fpr_zj, tpr_zj, color=zj_color, lw=lw, linestyle='-', label='RF ROC curve (area = %0.2f)' % auc1_zj)
    # x=y分割线
    ax1.plot([0, 1], [0, 1], color='k', lw=lw, linestyle='--')
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.0])
    ax1.set_xlabel('假阳性率')
    ax1.set_ylabel('真阳性率')
    ax1.set_title('ROC曲线')
    plt.legend(loc="lower right")
    ax2 = fig.add_subplot(1, 2, 2)
    # lyz线
    ax2.plot(recall, precision, color='r', lw=lw, linestyle='-', label='ANN PR curve (area = %0.2f)' % auc2)
    # lz线
    ax2.plot(recall_lz, precision_lz, color=lz_color, lw=lw, linestyle='-',
             label='Logistic PR curve (area = %0.2f)' % auc2_lz)
    # zj线
    ax2.plot(recall_zj, precision_zj, color=zj_color, lw=lw, linestyle='-',
             label='RF PR curve (area = %0.2f)' % auc2_zj)
    ax2.plot([0, 1], [1, 0], color='k', lw=lw, linestyle='--')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.0])
    ax2.set_xlabel('召回率')
    print('recall:', recall)
    ax2.set_ylabel('精准率')
    ax2.set_title('P-R曲线')
    plt.legend(loc="lower right")
    plt.savefig('../pic/ROC_PR.png', dpi=400, bbox_inches='tight')
    plt.show()


# RF、DT
def draw_RF_DT():
    plt.rcParams['font.sans-serif'] = ['SimHei']  ## 中文黑体
    # # data
    RF = dataUtil.load_data('../data/RF.csv').iloc[:, 1:]
    DT = dataUtil.load_data('../data/DT.csv').iloc[:, 1:]
    RF_ACC = RF.iloc[:, 0].values
    RF_Precision = RF.iloc[:, 1].values
    RF_Recall = RF.iloc[:, 2].values
    DT_ACC = DT['ACC'].values
    DT_Precision = DT.iloc[:, 1].values
    DT_Recall = DT.iloc[:, 2].values
    x = [1, 2, 3, 4, 5, 6]
    lw = 1
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x, RF_ACC, color='r', lw=lw, linestyle='-', label='RF_ACC')
    ax1.plot(x, DT_ACC, color='r', lw=lw, linestyle='--', label='DT_ACC')
    ax1.plot(x, RF_Precision, color='g', lw=lw, linestyle='-', label='RF_Precision')
    ax1.plot(x, DT_Precision, color='g', lw=lw, linestyle='--', label='DT_Precision')
    ax1.plot(x, RF_Recall, color='b', lw=lw, linestyle='-', label='RF_Recall')
    ax1.plot(x, DT_Recall, color='b', lw=lw, linestyle='--', label='DT_Recall')
    # ax1.set_xlim([9, 7, 5, 3, 2, 1])
    ax1.set_xlabel('子集编号')
    ax1.set_ylabel('指标')
    # ax1.set_title('P-R曲线')
    plt.legend(loc="lower right")
    plt.savefig('../pic/RF_DT.png', dpi=400, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # a = [0, 1, 1, 0, 1, 0, 0]
    # b = [0, 1, 1, 0, 0, 1, 1]
    # draw_matrix(a, b)
    # RF = dataUtil.load_data('../data/RF.csv').iloc[:, 1:]
    # DT = dataUtil.load_data('../data/DT.csv').iloc[:, 1:]
    draw_RF_DT()
