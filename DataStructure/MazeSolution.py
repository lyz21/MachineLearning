# encoding=utf-8
"""
@Time : 2020/5/21 10:10
@Author : LiuYanZhe
@File : MazeSolution.py
@Software: PyCharm
@Description: 迷宫求解
"""
import numpy as np
import matplotlib.pyplot as plt


class Maze:
    def __init__(self, start, end, maze_map=0):
        r, c = start
        out_r, out_c = end
        if maze_map == 0:
            self.maze_map = np.array([[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
                                      [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                                      [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
                                      [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                                      [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]])
        else:
            self.maze_map = maze_map
        self.list_passed = []
        self.draw()
        # 设置入口作为当前节点
        self.now = [r, c]
        self.maze_map[self.now[0], self.now[1]] = 2
        self.list_passed.append(self.now)  # 将该节点加入已走
        # 设置迷宫宽高
        self.h = len(self.maze_map)
        self.w = len(self.maze_map[0])
        # 设置出口
        self.out = [out_r, out_c]
        print(self.maze_map)
        self.draw()

    # 标记已走过位置,(a,b)为刚走过的位置
    def mark_passed(self):
        self.maze_map[self.now[0], self.now[1]] = 2
        self.list_passed.append(self.now)

    # 按照四个方向寻找下一个节点
    def find_next(self):
        r, c = self.now
        flag = 0  # 如果寻找下一步成功，返回1，否则返回0
        for i in range(4):
            if i == 0 and (r - 1) >= 0:  # 上
                if self.maze_map[r - 1, c] == 0:
                    self.now = [r - 1, c]
                    self.mark_passed()
                    flag = 1
                    break
            elif i == 1 and (r + 1) < self.h:  # 下
                if self.maze_map[r + 1, c] == 0:
                    self.now = [r + 1, c]
                    self.mark_passed()
                    flag = 1
                    break
            elif i == 2 and (c - 1) >= 0:  # 左
                if self.maze_map[r, c - 1] == 0:
                    self.now = [r, c - 1]
                    self.mark_passed()
                    flag = 1
                    break
            elif i == 3 and (c + 1) < self.w:  # 右
                if self.maze_map[r, c + 1] == 0:
                    self.now = [r, c + 1]
                    self.mark_passed()
                    flag = 1
                    break
        print('-' * 15)
        print(self.maze_map)
        return flag

    # 寻找路径
    def find_path(self):
        while True:
            if self.out == self.now:  # 到达出口,结束
                print(self.list_passed)
                break
            # 寻找下一步
            f = self.find_next()
            if f == 0:  # 寻找下一步失败，退回一步
                self.list_passed.pop()
                r, c = self.list_passed[len(self.list_passed) - 1]
                self.now = [r, c]
            self.draw()

    # 绘制图像方法
    def draw(self):
        plt.xticks([])
        plt.yticks([])
        plt.imshow(self.maze_map, cmap='Blues')
        # plt.savefig('../pic/kmeans_time.png', dpi=400, bbox_inches='tight')
        # plt.show()
        plt.pause(0.03)


if __name__ == '__main__':
    maze = Maze([0, 2], [14, 15])  # 不设置迷宫就是用默认的迷宫
    maze.find_path()
