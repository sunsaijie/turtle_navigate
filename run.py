from matrix import load_map, point
from draw import GoldMine, Mine, Mountain, River, Canvas

from typing import List, Dict, Tuple

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
    resolve = Resolve(load_map, point)
    data = resolve.resolve()
    for moves in data:
        c.accept_move_dict(moves)
    
    c.done()

class Resolve:
    def __init__(self, load_map, point):
        self.load_map = load_map
        self.point = point

    def resolve(self) -> List[Dict[int, Tuple[int, int]]]:
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
        for i in range(20):
            ret = {}
            for key in self.point:
                ret[key] = (1,0)
            rets.append(ret)
        return rets


if __name__ == "__main__":
    render()

