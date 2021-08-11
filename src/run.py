from matrix import load_map, point
from draw import GoldMine, Mine, Mountain, River, Canvas
from itertools import permutations
from astar import AstartClass

from typing import List, Dict, Tuple
import random

def render():
    block_dict = {}
    for m in [GoldMine, Mine, Mountain, River]:
        block_dict[m.id_] = m
    
    width = len(load_map)
    height = len(load_map[0])
    c = Canvas(width, height)
    
    # 把地图上的固定标记点画出
    for y, row in enumerate(load_map):
        for x, v in enumerate(row):
            if v != 0:
                c.append(x, y, block_dict.get(v))
    c._init_canvas()
    
    # 把起始点画出来
    for id_, start_point in point.items():
        c.set_moveblock(*start_point, id_)
    
    # 计算每个点的移动轨迹
    resolve = AstartClass(load_map)
    data = []
    for i in resolve.resolve((0,0), (38, 38)):
        data.append({1: i})
    for moves in data:
        c.accept_move_dict(moves)
    
    c.done()


class Resolve:
    def __init__(self, load_map, point):
        self.load_map = load_map
        self.point = point
        self.directions = [(x, y) for x, y in permutations([-1, 0, 1], 2) if x != 0 or y != 0]
        self.directions.append((1, 1))
        self.directions.append((-1, -1))
        print(self.directions)

    def resolve(self, target_x, target_y) -> List[Dict[int, Tuple[int, int]]]:
        """
        [
            {id: (1, 1)}
            ...
        ]
        列表中每一个字典为每次的行动
        字典中的每一个键是id_, 值是一个方向,一个有8个方向
        (1,1), (1,-1), (1,0)....
        """
        rets = []
        for _ in range(100):
            ret = {}
            for key in self.point:
                ret[key] = random.choice(self.directions)
            rets.append(ret)
        return rets
    
    def resolve_1(self, target_x, target_y):
        rets = []
        index = 0
        while index < 100:
            index += 1
            ret = {}
            for id_, point in self.point.items():
                if point[0] < target_x:
                    d_x = 1
                elif point[0] > target_x:
                    d_x = -1
                else:
                    d_x = 0
            
                if point[1] < target_y:
                    d_y = 1
                elif point[1] > target_y:
                    d_y = -1
                else:
                    d_y = 0
                t_x , t_y  = point[0] + d_x, point[1] + d_y
                
                turn = 0
                while self.load_map[t_y][t_x] != 0:
                    # 换一个方向, 在原来的基础上右转
                    print(id_, "碰撞了", t_x, t_y, self.load_map[t_y][t_x])
                        
                    print(id_, "turn_right before", d_x, d_y)
                    d_x, d_y = self.turn_right(d_x, d_y)
                    print(id_, "turn_right after", d_x, d_y)
                    t_x , t_y  = point[0] + d_x, point[1] + d_y
                    if not (0 <= t_y < len(self.load_map) and 0 <= t_x < len(self.load_map[0])):
                        d_x = d_y = 0
                        t_x, t_y = point[0], point[1]
                        

                if (t_x, t_y) in self.point.values():
                    d_x = d_y = 0
                    t_x, t_y = point[0], point[1]
                    
                    
                ret[id_] = (d_x, d_y)
                self.point[id_] = (t_x, t_y)
            rets.append(ret)
        return rets
    
    def turn_right(self, d_x, d_y):
        directions = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]
        if d_x == 0 and d_y == 0:
            return d_x, d_y
        
        index = directions.index((d_x, d_y)) + 1
        d_x, d_y = directions[index % 8]
        return d_x, d_y
                
    


if __name__ == "__main__":
    render()

