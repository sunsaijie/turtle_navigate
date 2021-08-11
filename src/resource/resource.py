from utils import Singleton
import numpy as np
from .objects import Objects


UnitType = np.dtype([
    ("t", "i4",),
    ("id", "i4",),
    ])


class Resource(metaclass=Singleton):
    width = 0
    height = 0
    remind_gold = 0
    
    def __init__(self, play_id=2222):
        self._resource_map = np.array([], dtype=UnitType)
        self.play_id = play_id
        self.objects = Objects
    
    @property
    def resource_map(self):
        return self._resource_map

    def game_start_parse(self, load_map):
        t_map = np.array(load_map)
        self._resource_map = np.zeros((40,40), dtype=UnitType)
        self._resource_map['t'] = t_map
    
    def game_inquire_parse(self, msg_data):
        round_id = msg_data.get("round_id")
        self._resource_map['id'] = 0
        for object_info in msg_data.get("objects", []):
            id_ = object_info.get("id")
            pos = object_info.get("position")
            self._resource_map[pos[1]][pos[0]]['id'] = id_
            if id_ in self.objects.container:
                o = self.objects.container.get(id_)
                o.update(object_info, round_id)
            else:
                role = object_info.get("role")
                o = self.objects.create_object(role, id_, round_id)
            self._resource_map[pos[1]][pos[0]]['t'] = o.type_id
        
        self.objects.clear_objects(round_id)
    
    def show_objects(self):
        for key, value in self.objects.container.items():
            print(key, value)

    def get_goldmine(self):
        all_goldmine_addr = np.where(self._resource_map["t"] == 7)
        ids = self._resource_map[all_goldmine_addr]['id']
        print(ids)
        print("-------")
        print(all_goldmine_addr)
    
    def get_soldier_location(self):
        pass
    
    def soldier_count(self):
        return len(self._resource_map[self._resource_map['t'] == 3])
    
    def gold_count(self):
        return self.remind_gold
    
    def goldmine_count(self):
        return len(self._resource_map[self._resource_map['t'] == 7])
        
    
