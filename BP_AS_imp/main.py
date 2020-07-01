# encoding=utf-8
"""
@Time : 2020/2/4 14:44
@Author : LiuYanZhe
@File : main.py
@Software: PyCharm
@Description:
"""
from BP_AS_imp import CV
from BP_AS_imp import BP
from BP_AS_imp import AS_lyz

k = 5
dataCV = CV.dataOperate_CV(k=k)
# 记录无改进BP
rightRate_list1 = []
rightRateCount1 = 0
# 蚁群改进BP
rightRate_list2 = []
rightRateCount2 = 0
# for i in range(k):
for i in range(2):
    list1, list2, list3, list4 = dataCV.divide_testAndtrain_inAndOut(i)
    print('--------------', i, '次------------------')
    # print('测试输入：', len(list1))
    # print('测试输出：', len(list2))
    # print('训练输入：', len(list3))
    # print('训练输出：', len(list4))
    # 无改进BP
    rightRate1 = BP.main(x_list=list3, y_list=list4, test_x_list=list1, test_y_list=list2, max_iter=2,learnRate=0.1)
    rightRateCount1 += rightRate1
    rightRate_list1.append(rightRate1)
    # 蚁群改进BP
    # 蚁群生成阈值 30次
    output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight = AS_lyz.main_AS(MAXITEM=1, x_list=list3,
                                                                                               y_list=list4)
    rightRate2 = BP.main_par(output_threshold_list, hidden_threshold_list, outhid_weight, inHid_weight, x_list=list3,
                             y_list=list4, test_x_list=list1, test_y_list=list2, learnRate=0.1,
                             max_iter=2)
    rightRateCount2 += rightRate2
    rightRate_list2.append(rightRate2)

print('------------------结果-------------------------')
print('无改进BP正确率')
print(rightRate_list1)
print('蚁群改进BP正确率')
print(rightRate_list2)
print('无改进BP平均正确率/蚁群改进BP平均正确率')
print(rightRateCount1 / len(rightRate_list1))
print(rightRateCount2 / len(rightRate_list2))
