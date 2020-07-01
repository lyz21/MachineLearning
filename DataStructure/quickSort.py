# encoding=utf-8
"""
@Time : 2020/4/24 15:43 
@Author : LiuYanZhe
@File : quickSort.py 
@Software: PyCharm
@Description: 
"""


# 快速排序
def partition(arr, begin, end):
    flag = 0  # 标识符，记录从前往后还是从后向前
    sub = begin  # 记录待填补的下标
    key = arr[begin]  # 选择第一个作为比较对象
    begin += 1
    while begin <= end:
        if flag == 0:  # 从后向前找比标准值小的，放前面
            if key >= arr[end]:
                arr[sub] = arr[end]
                sub = end
                flag = 1
            end -= 1
        else:  # 从前向后找比标准值大的，放后面
            if key <= arr[begin]:
                arr[sub], sub = arr[begin], begin
                flag = 0
            begin += 1
    arr[sub] = key
    return sub


def sort_quick(arr, begin, end):
    if begin < end:
        mid = partition(arr, begin, end)
        sort_quick(arr, begin, mid - 1)
        sort_quick(arr, mid + 1, end)
        print(arr)


if __name__ == '__main__':
    # data1 = [1, 6, 3, 2, 7, 10, 13, 24, 5, 43, 23, 10, 26, 28, 67, 1]
    data1 = [23, 12, 16, 28, 9, 7, 36, 5, 2, 45, 8, 13, 11, 35]
    print('输入数组：', data1)
    print('-------------------')
    # sort_bubble(data1)
    # data1 = [1, 6, 3, 2, 7, 10, 13, 24, 5, 43, 23, 10, 26, 28, 67]
    # sort_selection(data1)
    # data1 = [1, 6, 3, 2, 7, 10, 13, 24, 5, 43, 23, 10, 26, 28, 67]
    # sort_insertion(data1)
    # quickSort(data1, 0, len(data1) - 1)
    # print('快速排序     比较次数：', num_comp, '     交换次数：', num_exchange)
    sort_quick(data1, 0, len(data1) - 1)
    print('-------------------')
    print('输出数组：', data1)
