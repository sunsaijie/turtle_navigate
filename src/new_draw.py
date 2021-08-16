from turtle import Turtle, done, setup, screensize, register_shape, delay, update, tracer, speed
import numpy as np
import time
from matrix import load_map
from jsp import Jsp, make_path
from collections import defaultdict, OrderedDict

UPDATE_SPEED = 0.1

a = [
    [0,0,8,9],
    [0,0,8,7],
    [0,0,8,6],
]

class Block:
    color = "white"
    def __init__(self, id_):
        self.ct = Turtle()
        self.pos = None
        self.id_ = id_

    def move(self, pos):
        self.ct.clear()
        if self.pos is None:
            self.pos = pos
        elif abs(pos[1] - self.pos[1]) > 1:
            pass
        elif abs(pos[0] - self.pos[0]) > 1:
            pass
        else:
            self.pos = pos
        return self.pos

class Mine(Block):
    color = 'red'

class GoldMine(Block):
    color = "yellow"

class River(Block):
    color = "blue"

class Mountain(Block):
    color = "gray"

class Fatmain(Block):
    color = "green"

class TaijiPao(Block):
    color = "orange"

block_mapping = {
        6: Mine,
        9: River,
        7: GoldMine,
        8: Mountain,
        4: Fatmain,
        5: TaijiPao
}
        

class Canvas:
    unit_size = 20
    
    def __init__(self, matrix):
        self.width = len(matrix)
        self.height = len(matrix)
        self.matrix = matrix
    
    def _init_canvas(self):
        setup(width=self.width * self.unit_size * 1.2 , 
                height=(self.height -1) * self.unit_size * 1.2)
        screensize(self.width * self.unit_size,
                (self.height -1 )* self.unit_size)
        self.start_point = (-self.width * self.unit_size / 2, 
                - (self.height) * self.unit_size / 2)
        ct = Turtle()
        tracer(0)
        ct.speed(0)
        ct.ht()
        ct.up()
        startx, starty = self.start_point
        ct.setposition(startx, starty)
        for i in range(self.height + 1):
            # 遍历高度上的格子个数
            ct.setposition(startx, starty +  i * self.unit_size)
            ct.down()
            ct.forward(self.width * self.unit_size)
            ct.up()
        
        ct.setposition(startx, starty)
        ct.left(90)
        for j in range(self.width + 1):
            # 遍历宽度上的格子个数
            ct.setposition(startx + j * self.unit_size, starty)
            ct.down()
            ct.forward((self.height)* self.unit_size)
            ct.up()
    
    def fix_block(self, position, color, ct=None):
        if ct is None:
            ct = Turtle()
        tracer(0)
        ct.speed(0)
        ct.ht()
        x, y = position
        start_x, start_y = self.start_point
        lx = start_x + x * self.unit_size
        ly = start_y + y * self.unit_size
        ct.up()
        ct.setposition(lx, ly)
        ct.setheading(0)
        ct.down()
        ct.ht()
        ct.begin_fill()
        ct.fillcolor(color)
        for _ in range(3):
            ct.forward(self.unit_size)
            ct.left(90)
        ct.forward(self.unit_size)
        ct.end_fill()
        ct.ht()
    
    def _init_block(self):
        for x, row in enumerate(self.matrix):
            for y, v in enumerate(row):
                if v != 0:
                    self.fix_block((x,y), block_mapping.get(v).color)
        update()
    
    def move(self, block, pos):
        privous_pos = block.pos
        pos = block.move(pos)
        if self.matrix[pos[0]][pos[1]] == 0:
            self.matrix[pos[0]][pos[1]] = 1
            if privous_pos:
                self.matrix[privous_pos[0]][privous_pos[1]] = 0
            self.fix_block(pos, block.color, block.ct)
        else:
            if privous_pos:
                self.fix_block(privous_pos, block.color, block.ct)
            block.pos = privous_pos
    
    def accept(self, motions):
        for block, pos in motions:
            self.move(block, pos)
        time.sleep(UPDATE_SPEED)
        update()
            
# 群体移动解决方案
def group_move():
    can = Canvas(np.flip(np.array(load_map), axis=0).T)
    can._init_canvas()
    can._init_block()
    aa_paths = {}
    jsp = Jsp(np.flip(np.array(load_map), axis=0).T) 
    for i, pos in enumerate([(0,38), (0,37), (1,38),(1,37), (2,36), (2,37), (2,38), (2,39)]):
        aa = Fatmain(i)
        a = jsp.find_path(pos, (36,10))
        paths = make_path(a)
        aa_paths[aa] = paths
    
    while True:
        motions = []
        if all(len(x) == 0 for x in aa_paths.values()):
            break
        for aa, paths in aa_paths.items():
            if not paths:
                continue
            path = paths[0]
            if path not in [x[1] for x in motions] and can.matrix[path[0]][path[1]] == 0:
                path = paths.pop(0)
                motions.append((aa, path))
        can.accept(motions)
    done()
    
        
def is_neibor(cur, opt):
    if cur is None:
        return False
    return abs(cur[1] - opt[1]) <= 1 and abs(cur[0] - opt[0]) <=1

def dis(cur, opt):
    return abs(cur[1] - opt[1]) + abs(cur[0] - opt[0])
        
if __name__ == "__main__":
    import random
    can = Canvas(np.flip(np.array(load_map), axis=0).T)
    can._init_canvas()
    can._init_block()
    aa_paths = {}
    aa_can_attack = defaultdict(list)
    target = (20,9)
    target_attack = (21,8)
    jsp = Jsp(np.flip(np.array(load_map), axis=0).T) 
    for i, pos in enumerate([(0,38), (0,37), (1,38),(1,37), (2,36), (2,37), (2,38), (2,39)]):
        aa = Fatmain(i)
        a = jsp.find_path(pos, (20,9))
        paths = make_path(a)
        aa_paths[aa] = paths
    
    while True:
        motions = []
        if all(len(x) == 0 for x in aa_paths.values()):
            break
        if any(is_neibor(x.pos, target_attack) for x in aa_paths):
            break
        for aa, paths in aa_paths.items():
            if not paths:
                continue
            path = paths[0]
            if path not in [x[1] for x in motions] and can.matrix[path[0]][path[1]] == 0:
                path = paths.pop(0)
                motions.append((aa, path))
        can.accept(motions)
    print("进入这个..")
    

    # 找到第一个靠近的人
    for aa in aa_paths:
        if is_neibor(aa.pos, target_attack):
            break
    print(aa)
    
    # 找到目标周围所有可以站位的地方
    neiborOftarget = []
    for x, y in [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]:
        if can.matrix[x + target_attack[0]][y + target_attack[1]] == 0:
            neiborOftarget.append((x + target_attack[0], y + target_attack[1]))
    neiborOftarget = sorted(neiborOftarget, key=lambda x: dis(x, aa.pos)) 
    # 跟第一个靠近的人按照顺序排列
    neiborOftarget = [x for x in neiborOftarget if x!= aa.pos]
   
    # 取出最近的一个
    first = neiborOftarget[0]
    
    del aa_paths[aa]
    order_aa_paths = OrderedDict()
    # 更新占位符地图
    jsp.map_points['holder'] = 0
    jsp.map_points[aa.pos[0]][aa.pos[1]]['holder'] = 1
    # 一次计算到目标点周围各个空地的路径
    for index, aa in enumerate(sorted(aa_paths, key=lambda x: dis(x.pos, first))):
        if index == len(neiborOftarget):
            break
        a = jsp.find_path(aa.pos, neiborOftarget[index])
        path = make_path(a)
        order_aa_paths[aa] = path[1:]
        jsp.map_points[neiborOftarget[index][0]][neiborOftarget[index][1]]['holder'] = 1
    jsp.map_points['holder'] = 0
    
        
    for aa, oa in order_aa_paths.items():
        print(aa.id_, oa)
    for i in can.matrix:
        print(i)
    while True:
        motions = []
        for aa in order_aa_paths:
            if is_neibor(aa.pos, target_attack):
                print(aa.id_, "攻击")
        for aa, paths in order_aa_paths.items():
            if not paths:
                continue
            path = paths[0]
            if path not in [x[1] for x in motions] and can.matrix[path[0]][path[1]] == 0:
                path = paths.pop(0)
                motions.append((aa, path))
        can.accept(motions)
    done()
