import random

roles = ["GoldMine", "Soldier"]

def gen_inquire_data():
    items = []
    for i in range(20):
        items.append({
            "id": random.randint(1000,2000),
            "role": random.choice(roles),
            "life": 90,
            "gold": 50,
            "position": (random.randint(1,35), random.randint(1,35))
        })
        
    for i in range(1, 30):
        # for _ in range(0, random.randint(1,3)):
        #     item = random.choice(items)
        #     items.remove(item)
        # for _ in range(0, random.randint(1,3)):
        #     items.append({
        #         "id": random.randint(1000,2000),
        #         "role": random.choice(roles),
        #         "life": 90,
        #         "gold": 50,
        #         "position": (random.randint(1,35), random.randint(1,35))
        #     })
            
        yield {
            "round_id": i,
            "objects": items
        }

