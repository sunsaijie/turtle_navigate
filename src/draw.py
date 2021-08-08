from turtle import Turtle, done, setup, screensize, register_shape, delay, update, tracer, speed
from typing import Tuple
import time


UPDATE_SPEED = 0.5


class BaseBlock:
    """基本block"""
    color = "white"
    id_ = 0

class GoldMine(BaseBlock):
    color = "yellow"
    id_ = 7

class Mine(BaseBlock):
    color = "red"
    id_ = 6

class Mountain(BaseBlock):
    color = "grey"
    id_ = 8


class River(BaseBlock):
    color = "blue"
    id_ = 2


class MoveBlock:
    color = "black"
    
    def __init__(self, id_):
        self.id_ = id_
        self.turtle = Turtle()
        self.turtle.ht()
        self.x = 0
        self.y = 0
    
    def set_start(self, x , y):
        self.x = x
        self.y = y
    
    def move(self, move_to_x, move_to_y, units_size):
        self.turtle.clear()
        self.turtle.up()
        self.turtle.setposition(move_to_x, move_to_y)
        self.turtle.setheading(0)
        self.turtle.fillcolor(self.color)
        self.turtle.begin_fill()
        for _ in range(3):
            self.turtle.forward(units_size)
            self.turtle.right(90)
        self.turtle.forward(units_size)
        self.turtle.end_fill()

class Canvas:
    unit_size = 20
    def __init__(self, width, height):
        self.width_count = width
        self.height_count = height
        self.width = width * self.unit_size
        self.height = height * self.unit_size
        self.width_canvas = self.width * 1.2
        self.height_canvas = self.height * 1.2
        setup(width=self.width_canvas, height=self.height_canvas)
        screensize(self.width, self.height)
        self.start_point = (-self.width / 2, self.height / 2)
        self.blocks = []
        # 已经存在的点
        self.already_exits = []
        self.move_blocks = {}
        print(f"screen的width:{self.width}, height: {self.height}")
    
    def append(self, x, y, block: BaseBlock):
        self.blocks.append((x, y, block))
    
    def _init_canvas(self):
        """初始化画布"""
        ct = Turtle()
        tracer(0)
        ct.speed(0)
        ct.ht()
        # 画网格出来
        self.grid(ct, *self.start_point, width_count=self.width_count, height_count=self.height_count)
        for x, y, block in self.blocks:
            self.draw_block(ct, x, y, block)
        update()
    
    def done(self):
        done()
    
    def accept_move_dict(self, move_dict):
        for id_, move_vertor in move_dict.items():
            if id_ not in self.move_blocks:
                continue
            m = self.move_blocks.get(id_)
            self.move(m, *move_vertor)
        update()
        time.sleep(UPDATE_SPEED)
    
    def set_moveblock(self, location_x, location_y, id_):
        m = MoveBlock(id_)
        x, y = self.start_point
        to_x = x + location_x * self.unit_size
        to_y = y - location_y * self.unit_size
        m.set_start(to_x, to_y)
        if (to_x, to_y) in self.already_exits:
            print("已经存在了一个新的block")
            return
        self.already_exits.append((to_x, to_y))
        self.move_blocks[id_] = m
        self._draw_block(to_x, to_y, m.turtle, m.color)
        update()
    
    
    def move(self, m: MoveBlock, vertor_x, vertor_y):
        x = m.x
        y = m.y
        to_x = x + vertor_x * self.unit_size
        to_y = y - vertor_y * self.unit_size
        start_x, start_y = self.start_point
        end_x = start_x + self.width
        end_y = start_y - self.height
        if to_x < start_x or to_x > end_x:
            print("超出了x轴的范围")
            return 
        
        if to_y > start_y or to_y < end_y:
            print("超出了y轴的范围")
            return
        
        # 如果目标点在已存在的列表，则直接跳过
        if (to_x, to_y) in self.already_exits:
            print("碰撞了!!!!")
            return
        m.move(to_x, to_y, self.unit_size)
        m.set_start(to_x, to_y)
        self.already_exits.append((to_x, to_y))
        if (x, y) in self.already_exits:
            self.already_exits.remove((x, y))
    
    def draw_block(self, ct: Turtle, location_x: int, location_y: int, block: BaseBlock):
        ct.up()
        start_x, start_y = self.start_point
        x = start_x + location_x * self.unit_size
        y = start_y - location_y * self.unit_size
        color = block.color
        self.already_exits.append((x, y))
        self._draw_block(x, y, ct, color)
    
    def _draw_block(self, start_x, start_y, ct: Turtle, color):
        ct.up()
        ct.setposition(start_x, start_y)
        ct.setheading(0)
        ct.down()
        ct.begin_fill()
        ct.fillcolor(color)
        for _ in range(3):
            ct.forward(self.unit_size)
            ct.right(90)
        ct.forward(self.unit_size)
        ct.end_fill()
        ct.up()

    def grid(self, ct: Turtle, startx:int, starty: int, width_count, height_count):
        """画网格出来"""
        ct.up()
        ct.setposition(startx, starty)
        
        for i in range(height_count + 1):
            # 遍历高度上的格子个数
            ct.setposition(startx, starty - i * self.unit_size)
            ct.down()
            ct.forward(width_count * self.unit_size)
            ct.up()
        
        ct.setposition(startx, starty)
        ct.right(90)
        for j in range(width_count + 1):
            # 遍历宽度上的格子个数
            ct.setposition(startx + j * self.unit_size, starty)
            ct.down()
            ct.forward(height_count * self.unit_size)
            ct.up()

