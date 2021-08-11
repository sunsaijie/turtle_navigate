"""
对象管理器
"""

class Objects:
    container = {}
    switch_role = {}
    
    @classmethod
    def get_object_by_id(cls, *ids):
        rets = []
        for id_ in ids:
            if id_ in cls.container:
                rets.append(cls.container[id_])
        if len(rets) == 1:
            return rets[0]
        else:
            return rets
    
    @classmethod 
    def create_object(cls, role, id_, round_id):
        object_class = cls.switch_role.get(role, cls)
        return object_class(id_, round_id)
    
    @classmethod
    def regisiter_object(cls, role, object_class):
        cls.switch_role[role] = object_class
    
    @classmethod
    def clear_objects(cls, round_id):
        del_ids = []
        for id_, o in cls.container.items():
            if o.round_id != round_id:
                del_ids.append(id_)
        for del_id in del_ids:
            print("删除了", del_id)
            del cls.container[del_id]
        
    
    def __init__(self, id_, round_id):
        # 注册对象到对象管理器中
        self.__class__.container[id_] = self
        self.round_id = round_id
        self.id_ = id_
    
    def update(self, infos, round_id):
        """更新对象状态"""
        raise NotImplementedError
        

class GoldMine(Objects):
    gold = 0
    type_id = 7
    def update(self, infos, round_id):
        self.round_id = round_id
        self.gold = infos.get("gold")


class Soldier(Objects):
    life = 0
    type_id = 3
    def update(self, infos, round_id):
        self.round_id = round_id
        self.life = infos.get("life")
        

Objects.regisiter_object("GoldMine",GoldMine)
Objects.regisiter_object("Soldier", Soldier)
