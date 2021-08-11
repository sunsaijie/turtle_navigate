"""
提供全局的策略
"""
from resource.resource import Resource
from utils import Singleton


class Policy(metaclass=Singleton):
    def publish(self):
        r = Resource()
        print("金矿数为",  r.gold_count())
        print("剩余金矿数为", r.goldmine_count())
        print("我方士兵数量", r.soldier_count())
        tasks = []
        tasks.append("攻击有生力量")
        tasks.append("生产士兵")
        tasks.append("采一个狂")
        return tasks
