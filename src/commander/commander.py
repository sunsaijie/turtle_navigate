from utils import Singleton
from resource.resource import Resource
import abc

class Task(metaclass=abc.Meta):
    members = []
    
    def add_members(self, *iid):
        self.members.extend(iid)
    
    def release_members(self):
        return self.members

    @abc.abstractmethod
    def is_finish(self) -> bool:
        pass
    
    @abc.abstractmethod
    def action(self):
        pass
    
    

class MiningTask(Task):
    def __init__(self, *gold_points):
        self.gold_points = gold_points
        self.resource = Resource()
    
    def is_finish(self) -> bool:
        for gold_point in self.gold_points:
            pass
        return True
    
    def action(self):
        for members in self.members:
            print("这里是")
        return {}


class AttackTask(Task):
    def __init__(self, *enemy_points):
        self.enemy_points = enemy_points
        self.resource = Resource()
    
    def is_finish(self) -> bool:
        return True
    
    def action(self):
        for members in self.members:
            print("这里是寻路和dsds")
        return {}
            

class GuardTask(Task):
    def __init__(self, *target_point):
        self.target_point = target_point
        self.resource = Resource()
    
    def is_finish(self) -> bool:
        return True
    
    def action(self):
        for members in self.members:
            print("这里是血路和dsds")
        return {}
    


class Commander(metaclass=Singleton):
    tasks = []
    idle_soliders = []
    working_soliders = []

    def accept(self, tasks):
        for task in tasks:
            print("接受到任务指令:", task)


    def make_mine(self):
        pass



