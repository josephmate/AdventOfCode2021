import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque
from typing import OrderedDict

# on x=10..12,y=10..12,z=10..12
# off x=9..11,y=9..11,z=9..11
pattern = r'(\w+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)'
def parse_file(filename):
    lines = []
    with open(filename) as r:
        for line in r:
            line = line.rstrip()
            match = re.search(pattern, line)
            is_on = match.group(1) == "on"
            lines.append((is_on,
                int(match.group(2)), int(match.group(3)),
                int(match.group(4)), int(match.group(5)),
                int(match.group(6)), int(match.group(7))
                ))
    return lines

sample_small = parse_file('sample_small.txt')
sample_large = parse_file('sample_large.txt')
sample_even_larger = parse_file('sample_even_larger.txt')
input = parse_file('input.txt')

def solve_small(steps):
    on_cubes = set()

    for is_on, x1, x2, y1, y2, z1, z2 in steps:
        if (
            x1 >= -50 and x1 <= 50 and
            x2 >= -50 and x2 <= 50 and
            y1 >= -50 and y1 <= 50 and
            y2 >= -50 and y2 <= 50 and
            z1 >= -50 and z1 <= 50 and
            z2 >= -50 and z2 <= 50
        ):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    for z in range(z1, z2+1):
                        if is_on:
                            on_cubes.add((x,y,z))
                        elif (x,y,z) in on_cubes:
                            on_cubes.remove((x,y,z))

    return len(on_cubes)

print("39")
print(solve_small(sample_small))
print("590784")
print(solve_small(sample_large))
print("input soln")
print(solve_small(input))

# 2,758,514,936,282,235 entries won't fit into a set
# so we need a way to count the cubes iteratively instead
# of putting each coord into a set
# Let stick to 2D to make visualizing easier
# Suppose o is on
# Suppose . is of
# . . .
# . . .
# . . .
# 1 to 3 , 1 to 3
# o o o
# o o o
# o o o
# count is 9 so far
# 2 to 2 , 2 to 2
# o o o
# o . o
# o o o
# we need to recognize 1 coord intersects with 3 by 3
# so need to reduce the count by 1
# count is 8 so far
# 1 to 3, 1 to 3
# o o o
# o o o
# o o o
# need to recongize that
# a) 2,2 is off and we can turn that on
# b) 1,3 to 1,3 is already on minus the of
# so some how need to come up with incrementing by 1...?
# what if when processing the third cube, we look at each previous cube 1 by 1
# third cube is 3 by 3 so increment by 9
# so second cube, intersects on off , so increment by 1
# first cube incersects by 9 so decrement by 9
# overall we incremented by 1 as expected.
# lets try with another example to check
#
# on 2 to 4, 2 to 4
# . . . . .
# . o o o .
# . o o o .
# . o o o .
# . . . . .
# off 3 to 3, 3 to 3
# . . . . .
# . o o o .
# . o . o .
# . o o o .
# . . . . .
# on 3 to 5, 3 to 5
# . . . . .
# . o o o .
# . o o o o
# . o o o o
# . . o o o
# step 1 (0):
#   cube is 3by3 so add 9
#   no cubes before it so no interesections
# step 2(9):
#   cube is 1 by 1 
#   intersects with 3 by 3 so decrement by 1
# step 3(8):
#  cube is 3 by 3 so add 9
#  intersects with off 1 by 1 so increment by 1
#  insersects with on 2by2 so decrement by 4
# 14
# what about double offs?
# o o
# o o
# then
# o o
# o . 
# then again
# o o
# o . 
# after step 2 we have 3
# intersect off 1by1 so increment by 1
# intersect on  1by1 so decrement by 1
# total delta is 0
# final result 3
#
# double off, no on
# .
#
# .
# intersect off 1by1 decrement by 1
# final result -1 ????
# it seems like I need to recurse on the intersections somehow

# let look at the cube insection graph to see the depth
# maybe im making the problem more complex than it needs
# to be

# a  a  a
# a ab ab  b
# a ab ab  b
#    b  b  b
# 1 to 3 and 1 to 3
# 2 to 4 and 2 to 4
#                 
#   ____________ x2,y2,z2
#  /          /|
#  ----------/ |
#  |         | /
#  |         |/
#  ----------
# x1,y1,z1
# 
def is_intersecting(step_a, step_b):
    _, a_x1, a_x2, a_y1, a_y2, a_z1, a_z2 = step_a
    _, b_x1, b_x2, b_y1, b_y2, b_z1, b_z2 = step_b
    
    # check if one of the corners of one are within the other
    b_xs = [b_x1, b_x2]
    b_ys = [b_y1, b_y2]
    b_zs = [b_z1, b_z2]
    print(f"{a_x1}..{a_x2}   {a_y1}..{a_y2}    {a_z1}..{a_z2}")
    for b_x in b_xs:
        for b_y in b_ys:
            for b_z in b_zs:
                print(f"{b_x},{b_y},{b_z}")
                if (
                        b_x >= a_x1 and b_x <= a_x2
                    and b_y >= a_y1 and b_y <= a_y2
                    and b_z >= a_z1 and b_z <= a_z2
                ):
                    return True
    return False

def intersection_graph(steps):
    graph = OrderedDict()
    for i in range(0, len(steps)):
        for j in range(0, len(steps)):
            if not i == j and is_intersecting(steps[i], steps[j]):
                if i in graph:
                    graph[i].append(j)
                else:
                    graph[i] = [j]
                if j in graph:
                    graph[j].append(i)
                else:
                    graph[j] = [i]
    return graph

print()
print(is_intersecting(sample_even_larger[0], sample_even_larger[1]))
print(is_intersecting(sample_even_larger[1], sample_even_larger[0]))

exit()

print()
print("\n".join(map( lambda t: str(t), intersection_graph(sample_even_larger).items())))
print()


# from the sample, there is ALOT of intersection