from resource.resource import Resource
from policy.global_policy import Policy
from commander.commander import Commander
from data.inquire_data import gen_inquire_data
from matrix import load_map


def run():
    p = Policy()
    commander = Commander()
    r = Resource()
    r.game_start_parse(load_map)
    for i in gen_inquire_data():
        r.game_inquire_parse(i)
        tasks = p.publish()
        commander.accept(tasks)
    r.show_objects()
    # print(r.resource_map)
    r.get_goldmine()

if __name__ == "__main__":
    run()
