from dataclasses import dataclass
from typing import List, Type, Tuple, Optional
from matrix import load_map
import logging
import numpy as np
import time


matrix =  [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,1,0,0,0,1,1,1],
    [0,0,1,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
]

logging.basicConfig(level=logging.INFO, format="%(message)s", filename="action.log", filemode='w')

Vector = Tuple[int]

DIRECTIONS: List[Vector] = [
        (1,  1),
        (1,  0),
        (1, -1),
        (-1, 1),
        (-1,-1),
        (-1, 0),
        (0,  1),
        (0, -1)]

def cost_time(fun):
    def inner_func(*args, **kwargs):
        st = time.time()
        ret = fun(*args, **kwargs)
        print(fun.__name__, "cost", time.time() - st)
        return ret
    return inner_func


@dataclass
class Node:
    """地图上的节点类

    Attributjs:
        x: x轴坐标
        y: y轴坐标
        G: 从起点位置到当前节点的距离成本
        H: 从当前位置到终点的距离成本
        F: G + H
        Parent: 当前节点的父节点
    
    Methods:
        get_direction(self):
            获取当前节点的方向，根据父节点和当前节点的位置决定
            如果是起始节点则返回None
    """
    x: int
    y: int
    G: int = 0
    H: int = 0
    Parent = None
    
    @property
    def F(self):
        return self.G + self.H
        
    def __and__(self, opt):
        """计算当前节点和目标Node的成本H"""
        return (abs(opt.x - self.x) + abs(opt.y - self.y)) * 10
    
    def __or__(self, opt):
        """计算当前节点与目标的G值"""
        y_dis = abs(opt.y - self.y)
        x_dis = abs(opt.x - self.x)
        min_dis = min(y_dis, x_dis)
        return  min_dis * 14 + (y_dis + x_dis - 2 * min_dis) * 10
    
    def __eq__(self, opt):
        return self.x == opt.x and self.y == opt.y
    
    def __add__(self, director: Optional[Vector]):
        if isinstance(director, Node):
            return Node(self.x + Node.x, self.y + Node.y)
        else:
            return Node(self.x + director[0], self.y + director[1])
    
    def __sub__(self, opt) -> Vector:
        """根据父节点和当前节点的位置关系，获取当前的方向
        
        坐标系
        y|      c
         |   p 
         |__ __ __ x
         
        如上图所示: c 应该为/ 方向
        
        
        计算方式:
            (c.x - p.x , c.y - p.y)
        
        

        """
        if self.x == opt.x:
            x = 0
        else:
            x = int((self.x - opt.x) / abs(self.x - opt.x))
        if self.y == opt.y:
            y = 0
        else:
            y = int((self.y - opt.y) / abs(self.y - opt.y))
        return (x, y)
        
    def __hash__(self):
        return hash((self.x, self.y))
    


class Jsp:
    def __init__(self, map_points):
        self.width = len(map_points)
        self.height =len(map_points[0])
        self.map_points = np.zeros((self.width, self.height), dtype=np.dtype([('t', 'i4'), ('holder', 'i4')]))
        self.map_points['t'] = map_points
    
    @cost_time
    def find_path(self, start:Vector, end:Vector) -> Optional[List[Vector]]:
        start_node = Node(*start)
        end_node = Node(*end)
        # logging.debug("执行寻路任务开始，起始节点为%s, 终点节点为%s", start_node, end_node)

        start_node.H = end_node & start_node
        open_list = [start_node]
        closed_list = set()
        # logging.debug("初始化open_list... %s", open_list)
        
        while True:
            # 如果已经没有open节点了，说明无路可走
            if not open_list:
                # logging.debug("open_list已经探索完了, 没有找到相应的路径..")
                return None
            min_F_node = self.find_min_F(open_list)
            # logging.debug("open_list中找到一个最小F值的节点:%s,\n 在open_list中: %s", min_F_node, open_list)

            # 如果已经到目标点了，则可以跳出了
            if min_F_node == end_node:
                # logging.debug("最小F值得节点就是目标节点，找到目标了 %s ", min_F_node)
                return min_F_node
            
            # 找到自然邻居
            # logging.debug("开始探索节点 %s.=================== ", min_F_node)
            nnbs = self.nature_neighbour(min_F_node)
            # logging.debug("%s节点的nnbs:\n%s", min_F_node, nnbs)
            # logging.debug("开始遍历nnbs...")
            for nnb in nnbs:
                # logging.info("扫描%s的nnb:%s", min_F_node, nnb)
                jps = self.is_jps(nnb, min_F_node, end_node)

                # if jps:
                #     # logging.debug("%s nnb 有跳点", nnb)
                # else:
                #     logging.debug("%s nnb 没有跳点", nnb)

                if jps and jps not in closed_list:
                    jps.G = min_F_node.G + (jps | min_F_node)
                    jps.H = end_node & jps
                    jps.Parent = min_F_node
                    if jps in open_list:
                        # logging.debug("%s 在openlist中,  需要比较G值", jps)
                        list_nnb = open_list[open_list.index(jps)]
                        if list_nnb.G > jps.G:
                            list_nnb.Parent = min_F_node
                            # list_nnb.Parent.Parent = min_F_node
                            list_nnb.G = jps.G
                        continue
                    else:
                        # open_list.append(jps)
                        # logging.debug("将%s加入下一个需要探索的节点", jps)
                        # logging.debug("%s的父节点为%s", jps, jps.Parent)
                        open_list.append(jps)
            
            # 删除open列表, 加入close列表
            open_list.remove(min_F_node)
            closed_list.add(min_F_node)
            # logging.debug("结束探索节点 %s.=================== ", min_F_node)
            # logging.debug('---------------')
            # logging.debug("经过本轮探索, open_list中的节点为%s", open_list)
            # logging.debug('---------------')
            
    
    def find_min_F(self, open_list: List[Node]) -> Node:
        """在列表中找到最小的F值得Node"""
        min_F_node = open_list[0]
        for node in open_list[1:]:
            if node.F < min_F_node.F:
                min_F_node = node
        return min_F_node
    
    def nature_neighbour(self, point: Node):
        nnbs = []
        if point.Parent is None:
            for director in DIRECTIONS:
                next_point = point + director
                if self.can_passover(next_point):
                    nnbs.append(next_point)
        else:
            director = point - point.Parent
            # TODO沿着这个方向走
            if self.can_passover(point + director):
                nnbs.append(point + director)
            
            if not all(director):
                # 0  1  0
                # px x  0 
                # 0  0  0
                # 至少有一个0，说明是垂直或者水平的方向
                if director[0] == 0:
                    for v in [-1, 1]:
                        if not self.can_passover(point + (v, 0)):
                            nnbs.append(point + (v, director[1]))
                else:
                    for v in [-1, 1]:
                        if not self.can_passover(point + (0, v)):
                            nnbs.append(point + (director[0], v))
            
            else:
                # 斜着的情况
                # 
                # 0  0  0
                # 0  x  0 
                # px 0  0
                # 
                # px -> x == (1, 1)
                # 上和右都需要加进去
                if self.can_passover(point + (0, director[1])):
                    nnbs.append( point + (0, director[1]))
                if self.can_passover(point + (director[0], 0)):
                    nnbs.append( point + (director[0], 0))
                # (1, 1)
                # a  0  0
                # 1  x  0 
                # px 0  0
                #
                if (not self.can_passover(point + (-director[0], 0)) 
                        and self.can_passover(point + (0, director[1]))):
                    nnbs.append( point + (-director[0], director[1]))
                if (not self.can_passover(point + (0, -director[1])) 
                        and self.can_passover(point + (director[0], 0))):
                    nnbs.append( point + (director[0], -director[1]))
        return nnbs

    def can_passover(self, point: Node) -> bool:
        """判断坐标是否能够通过"""
        x = point.x
        y = point.y
        if not (0 <= x < self.width):
            return False
        elif not (0 <= y < self.height):
            return False
        elif self.map_points[x][y]['t'] != 0:
            return False
        elif self.map_points[x][y]['holder'] != 0:
            return False
        else:
            return True
        
    
    def forced_neighbour(self, point: Vector):
        """找到一个点的强迫邻居
        """
        pass
    
    def is_jps(self, target: Node, base: Node, end_node:Node) -> Optional[Node]:
        """判断target点是不是base点的跳点
        
        是跳点的定义有三个
        1. 是整个寻路的起始点或终止点
        2. 节点y在当前的搜索方向的前提下，有强迫邻居
        3. 如果当前搜索方向是斜向的, 且在y节点处，在水平分量或垂直分量上搜索可以找到跳点
           那么当前节点为跳点
        

        x为当前节点, p(x)为x的父节点
        
        自然邻居:
        搜索方向为垂直或水平, 
        px -> x 搜索方向为水平向右
        继续这个方向 -> a 则a是自然邻居

          1  2  3
        p(x) x  a
          4  5  6

        搜索方向为斜向
        px -> x 搜索方向为右上
        则当前搜索方向、x轴上的分量方向，y轴上的分量方向 a, b ,c 则 x 的自然邻居

           1  a  b
           4  x  c
         p(x) 5  6

        强迫邻居(定义):
        1. x的周围有障碍
        2. n不是x的自然邻居
        3. p(x)经过x到达n点的距离代价是p(x)到达n点的距离中最小的
        则n是x的强迫邻居
        
          0    1  a
          p(x) x  0
          0    0  0 
        
        1. a不是x的自然邻居
        2. x的周围有障碍
        3. p(x) -> x -> a 是 p(x) -> a 的最短距离
        
        -> a是x的强迫邻居

        """
        # 根据定义，如果需要判断的店是起点或者终点则为跳点, TODO中外面传进来
        # logging.debug("检查%s是否是%s的跳点....", target, base)
        if target == end_node:
            # logging.debug("%s 就是终点节点，是跳点", target)
            return target
        
        # 如果不可到达当然也不是跳点
        if not self.can_passover(target):
            # logging.debug("%s不是%s的跳点, 因为target点不可到达", target, base)
            return None
        
        # 节点y在当前的搜索方向的前提下，有强迫邻居
        director = target - base
        # logging.debug("当前搜索方向是%s", director)

        # d当前在水平和垂直上移动
        if not all(director):
            """ 
            b -> base, t -> target
             水平方向
             
             满足这种形态
             0   1   a
             b   t   0
             0   0   0 

             0   0   0
             b   t   0
             0   1   a 
             
             垂直方向
             0  b  0 
             1  t  0
             a  0  0

             0  b  0 
             0  t  1
             0  0  a
            """
            # 水平方向
            if director[1] == 0:
                if (not self.can_passover(target + (0, 1))) and self.can_passover(target + (director[0] ,1)):
                    return target
                if (not self.can_passover(target + (0, -1))) and self.can_passover(target + (director[0] ,-1)):
                    return target
            elif director[0] == 0:
                if (not self.can_passover(target + (-1, 0))) and self.can_passover(target + (-1 ,director[1])):
                    return target
                if (not self.can_passover(target + (1, 0))) and self.can_passover(target + (1 ,director[1])):
                    return target
        else:
            """
            斜线移动方向
            
            b -> t 只有这两种形态

            b  1  a
            0  t  x
            0  x  x

            b  0  0
            1  t  x
            a  x  x

            a  x  x
            1  t  x
            b  0  0

            0  x  x
            0  t  x
            b  1  a
            """
            if self.can_passover(
                    target + (-director[0], director[1])) and not self.can_passover(
                            target + (-director[0], 0)):
                return target
            if self.can_passover(
                    target + (director[0], -director[1])) and not self.can_passover(
                            target + (0, -director[1])):
                return target
        # 3. 如果当前搜索方向是斜向的, 且在y节点处，在水平分量或垂直分量上搜索可以找到跳点
        # 那么当前节点为跳点
        if all(director):
            x_next = self.is_jps(target + (director[0], 0), target, end_node)
            y_next = self.is_jps(target + (0, director[1]), target, end_node)
            if x_next or y_next:
                # return x_next or y_next
                return target
        if self.can_passover(target + (director[0], 0)) or self.can_passover(target + (0, director[1])):
            # 0  0  0  0  0  1  a 
            # px x  0  0  0  0  0
            # 0  0  0  0  0  0  0
            # 
            # 还是考虑的第二种继续往前搜索
            next_j = self.is_jps(target + director, target, end_node)
            if next_j:
                return next_j
        return None
    
def make_path(node):
    paths = []
    if not node:
        return paths
    while node.Parent:
        p = node.Parent
        new_p = Node(p.x, p.y)
        director = node - p
        item = []
        while new_p != node:
            # print(node, new_p)
            new_p = new_p + director
            item.append((new_p.x, new_p.y))
        paths.extend(reversed(item))
        node = p
    paths.append((node.x, node.y))
    paths.reverse()
    return paths
    # for i, _ in enumerate(paths[:-1]):
    #     yield (paths[i + 1][0] - paths[i][0], paths[i + 1][1] - paths[i][1])
    #     
        
    
from astar import AstartClass
            


if __name__ == "__main__":
    # jsp = Jsp(np.flip(np.array(matrix), axis=0).T)
    jsp = Jsp(np.flip(np.array(load_map), axis=0).T)
    a = jsp.find_path((0,38), (38,0)) 
    while a.Parent:
        print(a)
        a = a.Parent
    # for i in make_path(a):
    #     print(i)
    # make_path(a)
    s = AstartClass(np.flip(np.array(load_map), axis=0).T)
    s.resolve = cost_time(s.resolve)
    a = s.resolve((0,38), (38,0))
    # print(a)
    while a.Parent:
        print(a)
        a = a.Parent
    # print(a)

