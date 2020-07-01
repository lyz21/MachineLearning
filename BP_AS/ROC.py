# encoding=utf-8
"""
@Time : 2020/2/8 18:27 
@Author : LiuYanZhe
@File : ROC.py 
@Software: PyCharm
@Description: 
"""
from sklearn import metrics
import matplotlib.pyplot as plt


# 将2维数组转化为1维
def divide_list(list0):
    list1 = []
    list2 = []
    list3 = []
    for items in list0:
        list1.append(items[0])
        list2.append(items[1])
        list3.append(items[2])
    return list1, list2, list3


# 计算ROC和AUC
def ROC_AUC(true_list, pre_list):
    # roc_curve的输入为
    # true_list: 样本标签
    # pre_list: 模型对样本属于正例的概率输出
    # pos_label: 标记为正例的标签，本例中标记为2的即为正例   假阳性率 fp, 真阳性率 tpr, 阈值 thresholds
    fpr, tpr, thresholds = metrics.roc_curve(true_list, pre_list, pos_label=1)
    # print('fpr:', fpr, 'tpr:', tpr, 'thresholds:', thresholds)
    # auc的输入为很简单，就是fpr, tpr值
    auc = metrics.auc(fpr, tpr)
    # print('auc:', auc)
    return fpr, tpr, auc


# 绘制图像,三条线
def Draw_ROC(list_fpr, list_tpr, list_auc, name):
    lw = 1
    # ax1 = plt.subplot(1, 1, 1)  # 创建一个画板，同时创建一个子图
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    # ax1.plot([0, 1], [0, 1], color='navy', alpha=0.5, lw=lw, linestyle='--')
    # 画n条线
    for i in range(len(list_fpr)):
        fpr = list_fpr[i]
        tpr = list_tpr[i]
        auc = list_auc[i]
        # ax1.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % auc)
        if i == 0:
            # ax1.plot(fpr, tpr, color='darkorange', lw=lw, label='Qing - ROC curve (area = %0.2f)' % auc)
            ax1.plot(fpr, tpr, color='k', lw=lw, linestyle='--', label='Qing - ROC curve (area = %0.2f)' % auc)
        elif i == 1:
            ax1.plot(fpr, tpr, color='k', lw=lw, linestyle='-.', label='Ming - ROC curve (area = %0.2f)' % auc)
        else:
            ax1.plot(fpr, tpr, color='k', lw=lw, linestyle='-', label='Yuan - ROC curve (area = %0.2f)' % auc)
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title(name)
    plt.legend(loc="lower right")
    plt.savefig('pic/' + name + '.png', dpi=400, bbox_inches='tight')
    # plt.show()


# 主方法
def main_lyz(list_pre, list_y, name='ROC'):
    list_pre1, list_pre2, list_pre3 = divide_list(list_pre)
    list_y1, list_y2, list_y3 = divide_list(list_y)
    fpr1, tpr1, auc1 = ROC_AUC(list_y1, list_pre1)
    fpr2, tpr2, auc2 = ROC_AUC(list_y2, list_pre2)
    fpr3, tpr3, auc3 = ROC_AUC(list_y3, list_pre3)
    list_fpr = [fpr1, fpr2, fpr3]
    list_tpr = [tpr1, tpr2, tpr3]
    list_auc = [auc1, auc2, auc3]
    Draw_ROC(list_fpr, list_tpr, list_auc, name)
