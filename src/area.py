import numpy as np
from itertools import combinations_with_replacement, permutations, combinations, product

directions = [ x for x in product([-1, 1, 0], [-1, 1, 0]) if x != (0,0)]
# {(1, 2), (2, 1), (0, 0), (2, 0), (2, 2), (1, 3)}

a = [
    [0,1,1,8,0,0],
    [8,1,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
]

a = np.array(a)


def find_enters(a, *points):
    width = len(a) 
    height = len(a[0])
    
    def unbound(p):
        return (0 <= p[0] < width 
                and 0 <= p[1] < height)


    def around(p):
        a_points = []
        for vector in directions:
            print(vector)
            next_point = p[0] + vector[0], p[1] + vector[1]
            if unbound(next_point) and a[next_point[0]][next_point[1]] == 0:
                a_points.append(next_point)
            
        return a_points
    
    enter_points = set()
    for point in points:
        enter_points = enter_points | set(around(point))
    return enter_points

print(find_enters(a, (0,1), (0,2),(1,1)))

# {(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 3)}
            





