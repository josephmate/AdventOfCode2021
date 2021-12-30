import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque
from typing import OrderedDict
import math
from time import time as current_time

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
# check corners is not enough
# could be a line of one of the cubes that intersects:
#        b  b
#   a  a ba ba  a
#   a  a ba ba  a
#        b  b
def is_intersecting(step_a, step_b):
    _, a_x1, a_x2, a_y1, a_y2, a_z1, a_z2 = step_a
    _, b_x1, b_x2, b_y1, b_y2, b_z1, b_z2 = step_b
    
    return not (
           # x is into the screen
           # y is to the right
           # z is up
           b_x1 > a_x2 # completely infront of a
        or b_x2 < a_x1 # completely behind
        or b_y1 > a_y2 # completely to the right
        or b_y2 < a_y1 # completely to the left
        or b_z1 > a_z2 # completely above
        or b_z2 < a_z1 # completely below 
    )

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


print()
print("\n".join(map( lambda t: str(t), intersection_graph(sample_even_larger).items())))
print()


# from the sample, there is ALOT of intersection

# what if I sub divide the universe into smaller squares until it's iterable in one minute?
# lets see how many input cubes (ignoring the first in the -50 to 50 set)
# if there are only 1-2 cubes in each, it should be much easier to solve

def get_boundary(steps):
    return (
        min(map(lambda step: step[1], steps)),
        max(map(lambda step: step[2], steps)),
        min(map(lambda step: step[3], steps)),
        max(map(lambda step: step[4], steps)),
        min(map(lambda step: step[5], steps)),
        max(map(lambda step: step[6], steps)),
    )    

print(get_boundary(sample_even_larger))
print(get_boundary(input))
print()

# 2,758,514,936,282,235 need to be reduced to 2^32
# 140246 needs to be reduced to about 1625
print(pow(2_758_514_936_282_235, 1/3))
print(pow(pow(2,32), 1/3))
print(140246/1625)
print( math.log(pow(1625,3))/math.log(2) )
# so we're dealing with cubes of about 86 unit

def count_steps_in_cubes(steps, divider):
    min_x, max_x, min_y, max_y, min_z, max_z = get_boundary(steps)

    # counts the number of cubes that have x cubes passing through it
    counts = {}
    x_increment = (max_x - min_x) // divider
    y_increment = (max_y - min_y) // divider
    z_increment = (max_z - min_z) // divider

    i = 0
    for x1 in range(min_x, max_x+1, x_increment):
        print(i)
        i += 1
        for y1 in range(min_y, max_y+1, y_increment):
            for z1 in range(min_z, max_z+1, z_increment):
                x2 = x1 + x_increment
                y2 = y1 + y_increment
                z2 = z1 + z_increment
                count = 0
                for step in steps:
                    if is_intersecting(
                        (False, x1,x2,y1,y2,z1,z2),
                        step
                    ):
                        count += 1
                counts[count] = counts.get(count, 0) + 1
    return counts


print()
# divider=100
# (0, 498535)
# (1, 153723)
# (2, 124807)
# (3, 105378)
# (4, 71922)
# (5, 42809)
# (6, 17709)
# (7, 8106)
# (8, 5026)
# (9, 2010)
# (10, 268)
# (11, 8)
# divider=200
# (0, 3975791)
# (1, 1228022)
# (2, 1004724)
# (3, 830487)
# (4, 540722)
# (5, 308315)
# (6, 120934)
# (7, 61477)
# (8, 37725)
# (9, 11472)
# (10, 910)
# (11, 22)
# divider=500
# (0, 61629679)
# (1, 19352038)
# (2, 15800534)
# (3, 12816593)
# (4, 8167703)
# (5, 4586200)
# (6, 1773080)
# (7, 908790)
# (8, 555530)
# (9, 155444)
# (10, 5857)
# (11, 53)
#print("\n".join(map( lambda t: str(t), count_steps_in_cubes(sample_even_larger,500).items())))

# Lets see if I can partition the space until there are 3 intersecting cubes


def partition_count_impl(steps, x1, x2, y1, y2, z1, z2, intersects_by_volume, min_vol=1):
    intersect_steps = []
    for step in steps:
        if is_intersecting(step, (0, x1, x2, y1, y2, z1, z2)):
            intersect_steps.append(step)
    
    intersect_count = len(intersect_steps)
    volume = (x2-x1+1) * (y2-y1+1) * (z2-z1+1)
    if intersect_count <= 3 or volume <= min_vol:
        intersects_by_volume[intersect_count] = intersects_by_volume.get(intersect_count, 0) + volume
    else:
        # x1=10, x2=13, y1=10,y2=13
        # 10 11 12 13
        # 11  a  a  a
        # 12  a  a  a
        # 13  a  a  a
        # expected:
        #    x1 x2  y1 y2
        # 1. 10,11  10,11  
        # 2. 10,11  12,13 
        # 3. 12,13  10,11
        # 4. 12,13  12,13
        # x_delta = (13-10)/2 = 3/2 = 1
        # x_mid = x_delta + 10 = 11
        # y_mid = y_delta + 10 = 11
        # (x1, x_mid)     (y1, y_mid)
        # (x1, x_mid)     (y_mid + 1, y2)
        # (x_mid +1, x2)  (y1, y_mid)
        # (x_mid +1, x2)  (y_mid + 1, y2)
        # check with odd case:
        # x1=10, x2=12, y1=10, y2=12
        # 10 11 12
        # 11  a  a
        # 12  a  a
        # Expected:
        # 1. 10,11 10,11
        # 2. 10,11 12,12
        # 3. 12,12 10,11
        # 4. 12,12 12,12
        # Actual:
        # x_delta = (12-10)/2 = 2/2 = 1
        # x_mid = x_delta + 10 = 11
        # y_mix = 11
        # 10, 11   10,11
        # 10, 11   12,12
        # 12, 12   10,11
        # 12, 12   12,12
        x_delta = (x2-x1)//2
        y_delta = (y2-y1)//2
        z_delta = (z2-z1)//2
        x_mid = x_delta + x1
        y_mid = y_delta + y1
        z_mid = z_delta + z1
        # since we're in 3 dimensions, instead of 4 squares, we have 8 cubes
        partition_count_impl(intersect_steps,      x1, x_mid,      y1, y_mid,      z1, z_mid, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps,      x1, x_mid,      y1, y_mid, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps,      x1, x_mid, y_mid+1,    y2,      z1, z_mid, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps,      x1, x_mid, y_mid+1,    y2, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps, x_mid+1,    x2,      y1, y_mid,      z1, z_mid, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps, x_mid+1,    x2,      y1, y_mid, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps, x_mid+1,    x2, y_mid+1,    y2,      z1, z_mid, intersects_by_volume, min_vol)
        partition_count_impl(intersect_steps, x_mid+1,    x2, y_mid+1,    y2, z_mid+1,    z2, intersects_by_volume, min_vol)



def partition_count(steps, min_vol=1):
    min_x, max_x, min_y, max_y, min_z, max_z = get_boundary(steps)
    intersects_by_volume = {}
    partition_count_impl(steps, min_x, max_x, min_y, max_y, min_z, max_z, intersects_by_volume, min_vol)
    return intersects_by_volume

input_boundaries = get_boundary(input)
input_volume = (
    (input_boundaries[1]-input_boundaries[0]+1)
    *(input_boundaries[3]-input_boundaries[2]+1)
    *(input_boundaries[5]-input_boundaries[4]+1)
)
print(f"expected volume: {input_volume}")
for i in [1_000_000_000, 100_000_000, 10_000_000, 1_000_000, 100_000, 10_000, 1_000, 100]:
    start = current_time()
    input_intersects_by_volume = partition_count(input,i)
    end = current_time()
    print(f"min_vol={i} {end-start} secs")

    print("\n".join(map( lambda t: str(t), input_intersects_by_volume.items())))

    print(f"expected volume: {input_volume}")
    print(f"actual   volume: {sum(input_intersects_by_volume.values())}")
