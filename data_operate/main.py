
# encoding=utf-8
"""
@Time : 2020/2/4 14:44
@Author : LiuYanZhe
@File : main.py
@Software: PyCharm
@Description:
"""
from data_operate import CV
from data_operate import BP

k = 10
dataCV = CV.dataOperate_CV(k=k)
rightRate_list = []
rightRateCount = 0
for i in range(k):
    list1, list2, list3, list4 = dataCV.divide_testAndtrain_inAndOut(i)
    print('--------------', i, '次------------------')
    print('测试输入：', len(list1))
    print('测试输出：', len(list2))
    print('训练输入：', len(list3))
    print('训练输出：', len(list4))
    rightRate = BP.main(x_list=list3, y_list=list4, test_x_list=list1, test_y_list=list2)
    rightRateCount += rightRate
    rightRate_list.append(rightRate)
    # print('测试输入：', list1)
    # print('测试输出：', list2)
    # print('训练输入：', list3)
    # print('训练输出：', list4)
print('------------------结果-------------------------')
print(rightRate_list)
print('平均正确率：')
print(rightRateCount / len(rightRate_list))

