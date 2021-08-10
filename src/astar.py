import numpy as np
from dataclasses import dataclass

@dataclass
class Node:
    """
    G值是从起始节点到此节点的距离价值
    H值是从的当前节点到目标节点的距离价值
    """
    x: int
    y: int
    G: int = 0
    H: int = 0
    Parent = None
   
    @property
    def F(self):
        return self.G + self.H
    
    def __eq__(self, opt):
        return self.x == opt.x and self.y == opt.y
    
    def __sub__(self, opt):
        """计算H值
        x坐标的差值 + y坐标的差值
        """
        return (abs(self.x - opt.x) + abs(self.y - opt.y)) * 10
    
    def __or__(self, opt):
        """计算G值
        \ 斜线距离算14
        -- 或者 | 距离一格子算10
        """
        dis_x = abs(self.x - opt.x)
        dis_y = abs(self.y - opt.y)
        if dis_y > dis_x:
            dis_x, dis_y = dis_y, dis_x
        delta = abs(dis_x - dis_y)
        return abs(dis_x - delta) * 14 + delta * 10


matrix = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
]


def calc(matrix, start_node: Node, end_node: Node):
    open_list = [start_node]
    closed_list = []
    while open_list:
        handle_node = open_list[0]
        for node in open_list:
            if node.F < handle_node.F:
                handle_node = node
        open_list.remove(handle_node)
        closed_list.append(handle_node)
        
        # 如果正在处理节点是终点节点，则返回当前节点
        if handle_node == end_node:
            return handle_node
        
        # 找到邻居节点
        for i in range(-1, 2):
            for j in range(-1, 2):
                # 如果是当前节点，则跳过
                if i == j == 0:
                    continue
                try:
                    v = matrix[handle_node.x + i][handle_node.y + j]
                except IndexError:
                    # 如果数组越界则跳过
                    continue
                if v != 0:
                    # 如果是障碍则跳过
                    continue
                nebor_node = Node(handle_node.x + i, handle_node.y + j)
                if nebor_node in closed_list:
                    # 如果在关闭列表里面则直接跳过
                    continue
                elif nebor_node in open_list:
                    nebor_node = open_list[open_list.index(nebor_node)]
                    # 计算经过当前处理节点到此节点的G值得大小，如果比原来的小，则
                    # 更新父节点为当前节点,否则不需要做任何操作
                    thourgh_cur_G = handle_node.G + (nebor_node - handle_node)
                    if thourgh_cur_G < nebor_node.G:
                        nebor_node.G = thourgh_cur_G
                        nebor_node.Parent = handle_node
                else:
                    # 计算G值，从起点到当前点的值
                    nebor_node.G = nebor_node | start_node
                    # 计算H值，从当前点到终点的距离
                    nebor_node.H = nebor_node - end_node
                    # 把处理节点作为当前节点的父亲
                    nebor_node.Parent = handle_node
                    open_list.append(nebor_node)

        
    
end_node = calc(matrix, Node(0, 0), Node(5, 5))
while end_node.Parent:
    print(end_node.Parent)
    end_node = end_node.Parent
