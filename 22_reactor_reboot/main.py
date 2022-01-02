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

"""
print("39")
print(solve_small(sample_small))
print("590784")
print(solve_small(sample_large))
print("input soln")
print(solve_small(input))

39
39
590784
590784
input soln
596598
"""
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

assert is_intersecting(sample_even_larger[0], sample_even_larger[1])
assert is_intersecting(sample_even_larger[1], sample_even_larger[0])


#print()
#print("\n".join(map( lambda t: str(t), intersection_graph(sample_even_larger).items())))
#print()
"""
(0, [1, 2, 3, 5, 7, 9, 1, 2, 3, 5, 7, 9])
(1, [0, 0, 2, 3, 5, 7, 9, 2, 3, 5, 7, 9])
(2, [0, 1, 0, 1, 3, 5, 7, 9, 3, 5, 7, 9])
(3, [0, 1, 2, 0, 1, 2, 5, 7, 9, 5, 7, 9])
(5, [0, 1, 2, 3, 0, 1, 2, 3, 6, 7, 9, 6, 7, 9])
(7, [0, 1, 2, 3, 5, 6, 0, 1, 2, 3, 5, 6, 9, 9])
(9, [0, 1, 2, 3, 4, 5, 7, 0, 1, 2, 3, 4, 5, 7])
(4, [9, 9])
(6, [5, 5, 7, 7])
(10, [14, 28, 30, 37, 38, 41, 47, 48, 49, 53, 56, 57, 14, 28, 30, 37, 38, 41, 47, 48, 49, 53, 56, 57])
(14, [10, 10, 26, 28, 30, 37, 38, 41, 47, 48, 49, 53, 56, 57, 26, 28, 30, 37, 38, 41, 47, 48, 49, 53, 56, 57])
(28, [10, 14, 19, 10, 14, 19, 29, 36, 38, 41, 47, 48, 49, 53, 56, 57, 29, 36, 38, 41, 47, 48, 49, 53, 56, 57])
(30, [10, 11, 12, 14, 17, 19, 20, 21, 22, 26, 29, 10, 11, 12, 14, 17, 19, 20, 21, 22, 26, 29, 37, 38, 41, 43, 45, 46, 47, 48, 49, 50, 51, 53, 56, 57, 37, 38, 41, 43, 45, 46, 47, 48, 49, 50, 51, 53, 56, 57])
(37, [10, 14, 17, 21, 23, 26, 30, 34, 10, 14, 17, 21, 23, 26, 30, 34, 38, 41, 47, 48, 49, 51, 53, 56, 57, 38, 41, 47, 48, 49, 51, 53, 56, 57])
(38, [10, 14, 25, 26, 28, 30, 37, 10, 14, 25, 26, 28, 30, 37, 41, 48, 49, 53, 54, 56, 57, 41, 48, 49, 53, 54, 56, 57])
(41, [10, 14, 19, 25, 28, 29, 30, 33, 36, 37, 38, 10, 14, 19, 25, 28, 29, 30, 33, 36, 37, 38, 46, 48, 49, 53, 54, 56, 46, 48, 49, 53, 54, 56])
(47, [10, 14, 17, 19, 21, 22, 23, 26, 28, 29, 30, 34, 37, 43, 10, 14, 17, 19, 21, 22, 23, 26, 28, 29, 30, 34, 37, 43, 48, 49, 53, 56, 57, 48, 49, 53, 56, 57])
(48, [10, 14, 28, 30, 37, 38, 41, 47, 10, 14, 28, 30, 37, 38, 41, 47, 49, 53, 56, 57, 49, 53, 56, 57])
(49, [10, 14, 17, 21, 26, 28, 30, 34, 37, 38, 41, 47, 48, 10, 14, 17, 21, 26, 28, 30, 34, 37, 38, 41, 47, 48, 53, 56, 57, 53, 56, 57])
(53, [10, 14, 19, 26, 28, 30, 37, 38, 41, 47, 48, 49, 10, 14, 19, 26, 28, 30, 37, 38, 41, 47, 48, 49, 56, 57, 56, 57])
(56, [10, 14, 19, 28, 29, 30, 36, 37, 38, 41, 46, 47, 48, 49, 50, 53, 10, 14, 19, 28, 29, 30, 36, 37, 38, 41, 46, 47, 48, 49, 50, 53, 57, 57])
(57, [10, 14, 25, 26, 28, 30, 37, 38, 47, 48, 49, 53, 54, 56, 10, 14, 25, 26, 28, 30, 37, 38, 47, 48, 49, 53, 54, 56])
(11, [12, 20, 22, 29, 30, 36, 43, 44, 45, 46, 50, 12, 20, 22, 29, 30, 36, 43, 44, 45, 46, 50])
(12, [11, 11, 13, 18, 20, 22, 27, 29, 30, 35, 36, 39, 43, 44, 45, 46, 50, 13, 18, 20, 22, 27, 29, 30, 35, 36, 39, 43, 44, 45, 46, 50])
(20, [11, 12, 13, 15, 19, 11, 12, 13, 15, 19, 22, 29, 30, 32, 36, 39, 43, 44, 45, 46, 50, 52, 22, 29, 30, 32, 36, 39, 43, 44, 45, 46, 50, 52])
(22, [11, 12, 13, 17, 18, 20, 11, 12, 13, 17, 18, 20, 27, 29, 30, 35, 36, 43, 44, 45, 46, 47, 50, 51, 58, 27, 29, 30, 35, 36, 43, 44, 45, 46, 47, 50, 51, 58])
(29, [11, 12, 17, 19, 20, 22, 28, 11, 12, 17, 19, 20, 22, 28, 30, 36, 41, 43, 44, 45, 46, 47, 50, 56, 30, 36, 41, 43, 44, 45, 46, 47, 50, 56])
(36, [11, 12, 19, 20, 22, 24, 28, 29, 32, 11, 12, 19, 20, 22, 24, 28, 29, 32, 39, 40, 41, 43, 44, 45, 46, 52, 56, 39, 40, 41, 43, 44, 45, 46, 52, 56])
(43, [11, 12, 13, 17, 18, 20, 22, 27, 29, 30, 35, 36, 39, 11, 12, 13, 17, 18, 20, 22, 27, 29, 30, 35, 36, 39, 44, 45, 46, 47, 50, 51, 58, 44, 45, 46, 47, 50, 51, 58])
(44, [11, 12, 13, 15, 20, 22, 29, 36, 39, 43, 11, 12, 13, 15, 20, 22, 29, 36, 39, 43, 45, 46, 50, 52, 55, 45, 46, 50, 52, 55])
(45, [11, 12, 13, 15, 18, 20, 22, 29, 30, 32, 35, 36, 39, 43, 44, 11, 12, 13, 15, 18, 20, 22, 29, 30, 32, 35, 36, 39, 43, 44, 46, 50, 55, 46, 50, 55])
(46, [11, 12, 13, 18, 19, 20, 22, 29, 30, 32, 36, 39, 41, 43, 44, 45, 11, 12, 13, 18, 19, 20, 22, 29, 30, 32, 36, 39, 41, 43, 44, 45, 50, 55, 56, 50, 55, 56])
(50, [11, 12, 13, 17, 18, 20, 22, 29, 30, 35, 43, 44, 45, 46, 11, 12, 13, 17, 18, 20, 22, 29, 30, 35, 43, 44, 45, 46, 56, 58, 56, 58])
(13, [12, 12, 15, 18, 20, 22, 27, 35, 43, 44, 45, 46, 50, 55, 58, 15, 18, 20, 22, 27, 35, 43, 44, 45, 46, 50, 55, 58])
(18, [12, 13, 15, 12, 13, 15, 21, 22, 27, 35, 42, 43, 45, 46, 50, 51, 55, 58, 21, 22, 27, 35, 42, 43, 45, 46, 50, 51, 55, 58])
(27, [12, 13, 15, 16, 18, 21, 22, 12, 13, 15, 16, 18, 21, 22, 31, 35, 43, 51, 52, 55, 58, 31, 35, 43, 51, 52, 55, 58])
(35, [12, 13, 17, 18, 22, 27, 12, 13, 17, 18, 22, 27, 43, 45, 50, 51, 58, 43, 45, 50, 51, 58])
(39, [12, 19, 20, 32, 36, 12, 19, 20, 32, 36, 40, 43, 44, 45, 46, 52, 55, 40, 43, 44, 45, 46, 52, 55])
(15, [13, 13, 18, 20, 27, 31, 44, 45, 52, 55, 58, 18, 20, 27, 31, 44, 45, 52, 55, 58])
(55, [13, 15, 16, 18, 24, 27, 31, 39, 40, 42, 44, 45, 46, 52, 13, 15, 16, 18, 24, 27, 31, 39, 40, 42, 44, 45, 46, 52, 58, 59, 58, 59])
(58, [13, 15, 16, 18, 21, 22, 23, 26, 27, 31, 34, 35, 42, 43, 50, 51, 52, 55, 13, 15, 16, 18, 21, 22, 23, 26, 27, 31, 34, 35, 42, 43, 50, 51, 52, 55])
(26, [14, 17, 21, 23, 25, 14, 17, 21, 23, 25, 30, 34, 37, 38, 42, 47, 49, 51, 53, 54, 57, 58, 30, 34, 37, 38, 42, 47, 49, 51, 53, 54, 57, 58])
(31, [15, 16, 24, 27, 15, 16, 24, 27, 40, 42, 52, 54, 55, 58, 59, 40, 42, 52, 54, 55, 58, 59])
(52, [15, 20, 24, 27, 31, 36, 39, 40, 44, 15, 20, 24, 27, 31, 36, 39, 40, 44, 54, 55, 58, 54, 55, 58])
(16, [24, 27, 31, 40, 42, 55, 58, 59, 24, 27, 31, 40, 42, 55, 58, 59])
(24, [16, 16, 25, 31, 32, 33, 36, 40, 42, 52, 54, 55, 59, 25, 31, 32, 33, 36, 40, 42, 52, 54, 55, 59])
(40, [16, 24, 25, 31, 32, 33, 36, 39, 16, 24, 25, 31, 32, 33, 36, 39, 52, 54, 55, 59, 52, 54, 55, 59])
(42, [16, 18, 24, 25, 26, 31, 32, 16, 18, 24, 25, 26, 31, 32, 54, 55, 58, 59, 54, 55, 58, 59])
(59, [16, 24, 25, 31, 32, 33, 40, 42, 54, 55, 16, 24, 25, 31, 32, 33, 40, 42, 54, 55])
(17, [21, 22, 23, 26, 29, 30, 35, 37, 43, 47, 49, 50, 51, 21, 22, 23, 26, 29, 30, 35, 37, 43, 47, 49, 50, 51])
(21, [17, 18, 17, 18, 23, 26, 27, 30, 34, 37, 47, 49, 51, 58, 23, 26, 27, 30, 34, 37, 47, 49, 51, 58])
(23, [17, 21, 17, 21, 26, 34, 37, 47, 51, 58, 26, 34, 37, 47, 51, 58])
(51, [17, 18, 21, 22, 23, 26, 27, 30, 34, 35, 37, 43, 17, 18, 21, 22, 23, 26, 27, 30, 34, 35, 37, 43, 58, 58])
(19, [20, 28, 29, 30, 33, 36, 39, 41, 46, 47, 53, 54, 56, 20, 28, 29, 30, 33, 36, 39, 41, 46, 47, 53, 54, 56])
(33, [19, 24, 25, 32, 19, 24, 25, 32, 40, 41, 54, 59, 40, 41, 54, 59])
(54, [19, 24, 25, 26, 31, 32, 33, 38, 40, 41, 42, 52, 19, 24, 25, 26, 31, 32, 33, 38, 40, 41, 42, 52, 57, 59, 57, 59])
(32, [20, 24, 25, 20, 24, 25, 33, 36, 39, 40, 42, 45, 46, 54, 59, 33, 36, 39, 40, 42, 45, 46, 54, 59])
(34, [21, 23, 26, 21, 23, 26, 37, 47, 49, 51, 58, 37, 47, 49, 51, 58])
(25, [24, 24, 26, 32, 33, 38, 40, 41, 42, 54, 57, 59, 26, 32, 33, 38, 40, 41, 42, 54, 57, 59])

"""

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

"""
print(get_boundary(sample_even_larger))
print(get_boundary(input))
print()

(-120100, 120875, -124565, 118853, -121762, 119054)
(-97755, 94973, -98332, 94063, -97168, 95365)

# 2,758,514,936,282,235 need to be reduced to 2^32
# 140246 needs to be reduced to about 1625
print(pow(2_758_514_936_282_235, 1/3))
print(pow(pow(2,32), 1/3))
print(140246/1625)
print( math.log(pow(1625,3))/math.log(2) )
# so we're dealing with cubes of about 86 unit

140246.41867365324
1625.4986772154357
86.30523076923077
31.99867200840954

"""

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


def partition_volume_count_impl(steps, x1, x2, y1, y2, z1, z2, intersects_by_volume, min_vol=1):
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
        partition_volume_count_impl(intersect_steps,      x1, x_mid,      y1, y_mid,      z1, z_mid, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps,      x1, x_mid,      y1, y_mid, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps,      x1, x_mid, y_mid+1,    y2,      z1, z_mid, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps,      x1, x_mid, y_mid+1,    y2, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps, x_mid+1,    x2,      y1, y_mid,      z1, z_mid, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps, x_mid+1,    x2,      y1, y_mid, z_mid+1,    z2, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps, x_mid+1,    x2, y_mid+1,    y2,      z1, z_mid, intersects_by_volume, min_vol)
        partition_volume_count_impl(intersect_steps, x_mid+1,    x2, y_mid+1,    y2, z_mid+1,    z2, intersects_by_volume, min_vol)



def partition_volume_count(steps, min_vol=1):
    min_x, max_x, min_y, max_y, min_z, max_z = get_boundary(steps)
    intersects_by_volume = {}
    partition_volume_count_impl(steps, min_x, max_x, min_y, max_y, min_z, max_z, intersects_by_volume, min_vol)
    return intersects_by_volume

input_boundaries = get_boundary(input)
input_volume = (
    (input_boundaries[1]-input_boundaries[0]+1)
    *(input_boundaries[3]-input_boundaries[2]+1)
    *(input_boundaries[5]-input_boundaries[4]+1)
)
# print(f"expected volume: {input_volume}")
#for i in [1_000_000_000, 100_000_000, 10_000_000, 1_000_000, 100_000, 10_000, 1_000, 100]:
for i in []:
    start = current_time()
    input_intersects_by_volume = partition_volume_count(input,i)
    end = current_time()
    print(f"min_vol={i} {end-start} secs")

    print("\n".join(map( lambda t: str(t), input_intersects_by_volume.items())))

    print(f"expected volume: {input_volume}")
    print(f"actual   volume: {sum(input_intersects_by_volume.values())}")

# (0, 2361821899010547)
# (1, 1319546041432069)
# (2, 1601401737128548)
# (3, 1702756980717707)
# (4, 108689905549876)
# (5, 33791983162659)
# (6, 9255331271108)
# (7, 1691441308210)
# (8, 258161736084)
# (9, 2767011072)
# (20, 53157376)
# expected volume: 7139216301485256
# actual   volume: 7139216301485256
# min_vol=10000000 62.282487630844116 secs
# (0, 2361821958847939)
# (1, 1319550251677969)
# (2, 1601770058878041)
# (3, 1712142841141531)
# (4, 103106152118389)
# (5, 31028401994077)
# (6, 8187063207384)
# (7, 1398353319210)
# (8, 210215894924)
# (9, 997761120)
# (20, 6644672)
# expected volume: 7139216301485256
# actual   volume: 7139216301485256
# based on the above experiment, I don't think I will find a small enough volume
# in time to have 3 or fewer intersections.
# maybe there are more than 3 intersecting at one cube anyways.
# maybe I can partition until the partition is completely inside
# that way I don't need to figure out how to calculate the coords of intersection

def is_a_within_b(step_a, step_b):
    _, a_x1, a_x2, a_y1, a_y2, a_z1, a_z2 = step_a
    _, b_x1, b_x2, b_y1, b_y2, b_z1, b_z2 = step_b

    return (
            a_x1 >= b_x1
        and a_x2 <= b_x2
        and a_y1 >= b_y1
        and a_y2 <= b_y2
        and a_z1 >= b_z1
        and a_z2 <= b_z2
    )

def track_volume_stats(volume_tracker, volume):
    """
    volume_tracker = [
        0,               # 0 volume explored so far
        total_volume,    # 1 total volume to explore
        current_time(),  # 2 time since start
        0,               # 3 last percentage we gave an update
        0.1,             # 4 next percentage where we give an update
        current_time()   # 5 time since last update
    ]
    """
    volume_tracker[0] += volume
    percent = volume_tracker[0] / volume_tracker[1] * 100
    if percent > volume_tracker[4]:
        next_time = current_time()
        estimated_time_left = (current_time()-volume_tracker[2])*(100-percent)/percent
        print(f"from {volume_tracker[3]}% until {percent}% took {next_time-volume_tracker[5]} secs. estimated time left {estimated_time_left} secs")
        volume_tracker[5] = next_time
        volume_tracker[4] = percent + 0.1
        volume_tracker[3] = percent


def on_count_by_partition(steps, x1, x2, y1, y2, z1, z2, volume_tracker):
    intersect_steps = []
    boundary_step = (0, x1, x2, y1, y2, z1, z2)
    for step in steps:
        if is_intersecting(step, boundary_step):
            intersect_steps.append(step)
    
    intersect_count = len(intersect_steps)
    volume = (x2-x1+1) * (y2-y1+1) * (z2-z1+1)
    if intersect_count == 0:
        track_volume_stats(volume_tracker, volume)
        return 0

    all_within = True
    for step in intersect_steps:
        if not is_a_within_b(boundary_step, step):
            all_within = False
    
    if all_within:
        track_volume_stats(volume_tracker, volume)
        if intersect_steps[len(intersect_steps)-1][0] == 'on':
            return volume
        else:
            return 0

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
    return (on_count_by_partition(intersect_steps,      x1, x_mid,      y1, y_mid,      z1, z_mid, volume_tracker)
          + on_count_by_partition(intersect_steps,      x1, x_mid,      y1, y_mid, z_mid+1,    z2, volume_tracker)
          + on_count_by_partition(intersect_steps,      x1, x_mid, y_mid+1,    y2,      z1, z_mid, volume_tracker)
          + on_count_by_partition(intersect_steps,      x1, x_mid, y_mid+1,    y2, z_mid+1,    z2, volume_tracker)
          + on_count_by_partition(intersect_steps, x_mid+1,    x2,      y1, y_mid,      z1, z_mid, volume_tracker)
          + on_count_by_partition(intersect_steps, x_mid+1,    x2,      y1, y_mid, z_mid+1,    z2, volume_tracker)
          + on_count_by_partition(intersect_steps, x_mid+1,    x2, y_mid+1,    y2,      z1, z_mid, volume_tracker)
          + on_count_by_partition(intersect_steps, x_mid+1,    x2, y_mid+1,    y2, z_mid+1,    z2, volume_tracker)
    )

def on_count(steps):
    min_x, max_x, min_y, max_y, min_z, max_z = get_boundary(steps)
    total_volume = (
        (input_boundaries[1]-input_boundaries[0]+1)
        *(input_boundaries[3]-input_boundaries[2]+1)
        *(input_boundaries[5]-input_boundaries[4]+1)
    )
    volume_tracker = [
        0,               # volume explored so far
        total_volume,    # total volume to explore
        current_time(),  # time since start
        0,               # last percentage we gave an update
        0.1,             # next percentage where we give an update
        current_time()   # time since last update
    ]
    on_volume = on_count_by_partition(steps, min_x, max_x, min_y, max_y, min_z, max_z, volume_tracker)
    print(f"total volume explored: {volume_tracker[0]}")
    print(f"expected volume:       {total_volume}")
    return on_volume

"""
print(f"expected: {2758514936282235}")
start = current_time()
on_volume = on_count(sample_even_larger)
end = current_time()
print(f"actual: {on_volume}")
print(f"{end-start} secs")


print("input:")
start = current_time()
on_volume = on_count(input)
end = current_time()
print(on_volume)
print(f"{end-start} secs")

 ------------------
|                  | 
|   Failure        |
|                  |
 ------------------

# The above solution was too slow to run overnight, so I'm moving on.
# Next I want to see if I can take a cube and split it with the
# intersecting cubes after it.
# By the end we should have something like O((9N)^2) cubes, which is okay since
# the input only as about ~400 cubes.
# The only hard part it to figure out how to split the cubes.
# Pseudocode:
# let split_cubes = []
# for each cube in cubes:
#  for each intersecting_cube in split_cubes intersecting with cube:
#    remove intersecting_cube
#    split intersecting_cube based on cube
#    add the split back in
#  add cube into split_cubes
# now split_cubes only contains cubes that 100% overlap????
#   I'm not sure if this is true yet.
#   If the split cube is smaller than the cube, then the split cube won't
#   intersect. Then maybe we need to also split the cube as well?
# now split cubes only contains cube that 100% overlap
# so we can group them by coordinates
# check if the last one is on/off
# if it's on, add that to the volume

 ------------------
|                  |
|   Intersection   |
|                  |
 ------------------

the last piece is calculating the intersection.
Let's try the 2D case first:
  0123456789 -> y
0 ooooo
1 o   o
2 o xxoxx
3 o x o x
4 ooooo x
5   x   X
6   xxxxx
|
v
x
Expected is x=(2,4) y=(2,4)

x1 = max(x1a, x1b) = max(0,2) = 2
x2 = min(x2a, x2b) = min(4,6) = 4
y1 = max(y1a, y1b) = max(0,2) = 2
y2 = min(y2a, y2b) = min(4,6) = 4

let's check what happens if they don't intersect:
  0123456
0 ooo xxx
1 o o x x
2 ooo xxx
Expected: something indicating no intersection

x1 = max(0,0) = 0
x2 = min(2,2) = 2
y1 = max(0,4) = 4
y2 = min(2,6) = 2

y1 > y2, which is not allowed, our rectangles are always
defined by x1 <= x2; y1 <= y2

so if x1 > x2 or y1 > y2 or z1 > z2, then there is no intersection

So for 3D the intersection should be:
x1 = max(x1a, x1b)
x2 = min(x2a, x2b)
y1 = max(y1a, y1b)
y2 = min(y2a, y2b)
z1 = max(z1a, z1b)
z2 = min(z2a, z2b)

x1 <= x2 and y1 <= y2 and z1 <= z2

"""
def get_intersection(step_a, step_b):
    _,         a_x1, a_x2, a_y1, a_y2, a_z1, a_z2 = step_a
    is_on_off, b_x1, b_x2, b_y1, b_y2, b_z1, b_z2 = step_b

    x1 = max(a_x1, b_x1)
    x2 = min(a_x2, b_x2)
    y1 = max(a_y1, b_y1)
    y2 = min(a_y2, b_y2)
    z1 = max(a_z1, b_z1)
    z2 = min(a_z2, b_z2)

    # there is no intersection in these cases
    # we must have x1 <= x2; y1 <= y2; z1 <= z2
    # for there to be an intersection
    if x1 > x2:
        return None
    if y1 > y2:
        return None
    if z1 > z2:
        return None

    return (is_on_off, x1, x2, y1, y2, z1, z2)

"""
 ------------------
|                  |
|  Splitting Cubes |
|                  |
 ------------------


now the hard part is to figure out how to split these cubes based on eachother

ooooo
o   o
o xxoxx
o x o x
ooooo x
  x   X
  xxxxx
When we split, we want only rectangles after we're done.
I think the easiest want to split would end up like this:
11333
11333
2244455
2244455
2244455
  66777
  66777

It looks like the cubes need to be split using the 'lines' x1, x2, y1, y2:
   x x x x
   1 1 2 2
   a b a b
   | | | |
   | | | |
---ooooo-+----y2a
   o   o |
---o xxoxx----y2b
   o x o x
---ooooo x----y1a
     x   x
-----xxxxx----y1b

Lets try a weird case where one corner is not within the other:
        ooooo
        o   o
     xxxoxxxoxxx
     x  o   o  x
     xxxoxxxoxxx
        o   o
        ooooo

        11111
        11111
     33344444555
     33344444555
     33344444555
        22222
        22222
It looks like it could work, but I'm not sure how to translate
this into code yet.
I also don't know how this translates to 3d yet.

Another way I can think of is to start with the intersection,
then consider the the rectangular prism
above, below, forward, back, left right:

ooooo
o   o
o xxoxx
o x o x
ooooo x
  x   X
  xxxxx

but that is not enough because up and left in the above example overlap.
So I think we need to consider the pairs:
2D
left up       up       right up
left     intersection  right
leff down     down     right down

3D
            | /
            |/
       -----+------
           /|
          / |

     --------
    /      / |
   /------/  |
   |      |  |
   |      | /
   |      |/
    ------/

looks like it would be a cross product of
up/down/none, left/right/none, forward/back/none
producing 27 squares
but none,none,none is the intersection so 26

but then I was think we could simplify this by
carefully handling the overlap:

back to 2d

ooooo
o   o
o xxoxx
o x o x
ooooo x
  x   X
  xxxxx

above the top of the intersection
below the bottom of the intersection
to the left of the intersection and below the top and above the bottom of the intersection
to the right of the intersection and below the top and above the bottom of the intersection
that reduces the number of rectangles we produce

in 3D it would be

     --------
    /      / |
   /------/  |
   |      |  |
   |      | /
   |      |/
    ------/

above the intersection
below the intersection
to the left  and below the top of the intersection
             and above the bottom of the instersection
to the right and below the top of the intersection
             and above the bottom of the instersection
forward      and below the top of the intersection
             and above the bottom of the instersection
             and to the right of the left of the intersection
             and to the left of the right of the intersection
backwards    and below the top of the intersection
             and above the bottom of the instersection
             and to the right of the left of the intersection
             and to the left of the right of the intersection

but how do these restrictions translate to code?

x is forward back
y is up down
z is left right

result must have x1 <= x2; y1 <= y2; z1 <= z2
if not, there is no sub shape there.

above the intersection
    y1 = intersection's y2
    y2 = y2 of shape
    x1,x2,z1,z2 stay the same
below the intersection
    y2 = intersection's y1
    y1 = y1 of shape
    x1,x2,z1,z2 stay the same

to the left  and below the top of the intersection and above the bottom of the intersection
z2 = intersection's z1 - 1
z1 remains the same
x1,x2 remain the same
need to collapse the y's since we already have cubes for them
y1 = max(y1, intersection's y1) # we cannot go below the intersection
    no need to add/subtract because the above/below had to remove it
    so we wouldn't double count the intersection
y2 = min(y2, intersection's y2) # we cannot go above the intersection
    no need to add/subtract because the above/below had to remove it
    so we wouldn't double count the intersection
similar for to the right

U = up    D = down    I = intersection
back  forward
<--   -->   ^
UUUUUUUUU   | up
   IIIFFF   
   IIIFFF
   IIIFFF   | down
DDDDDDDDD   v
rotate around the x axis (forward/back axis)

<--   -->   ^
RRRRRRRRR   | right
   IIIFFF   
   IIIFFF
   IIIFFF   | left
LLLLLLLLL   v

so we don't need to add/subtract like we need
to for the edge that touches the intersection
it's also not touching the already split cubes
as we can see from the above two diagrams

forwards
x1 = intersection's x2 + 1
x2 stays the same
y1 = max(y1, intersection's y1)
y2 = min(y2, intersection's y2)
z1 = max(z1, intersection's z1)
z2 = min(z2, intersection's z2)
similar for backwards
"""
def is_valid(step):
    _, x1, x2, y1, y2, z1, z2 = step
    return (
            x1 <= x2
        and y1 <= y2
        and z1 <= z2
    )

def split_by_intersection(intersection, step):
    _,     i_x1, i_x2, i_y1, i_y2, i_z1, i_z2 = intersection
    is_on, s_x1, s_x2, s_y1, s_y2, s_z1, s_z2 = step
    result = []

    above = (
        is_on,
        s_x1,
        s_x2,
        i_y2 + 1, # y1 = intersection's y2. add 1 since we're integer cubes
        s_y2,
        s_z1,
        s_z2,
    )
    if is_valid(above):
        result.append(above)

    below = (
        is_on,
        s_x1,
        s_x2,
        s_y1,
        i_y1 - 1, # y2 = intersection's y1. subtract 1 since integer cubes
        s_z1,
        s_z2,
    )
    if is_valid(below):
        result.append(below)

    left = (
        is_on,
        s_x1,
        s_x2,
        max(s_y1, i_y1), # we cannot go below the intersection
        min(s_y2, i_y2), # we cannot go above the intersection
        s_z1,
        i_z1 - 1, # z2 = intersection's z1 - 1
    )
    if is_valid(left):
        result.append(left)

    # to the right and below the top of the intersection
    #             and above the bottom of the instersection
    right = (
        is_on,
        s_x1,
        s_x2,
        max(s_y1, i_y1), # we cannot go below the intersection
        min(s_y2, i_y2), # we cannot go above the intersection
        i_z2+1,
        s_z2,
    )
    if is_valid(right):
        result.append(right)

    # forward      and below the top of the intersection
    #             and above the bottom of the instersection
    #             and to the right of the left of the intersection
    #             and to the left of the right of the intersection
    forward = (
        is_on,
        i_x2 + 1,
        s_x2,
        max(s_y1, i_y1), # we cannot go below the intersection
        min(s_y2, i_y2), # we cannot go above the intersection
        max(s_z1, i_z1),
        min(s_z2, i_z2),
    )
    if is_valid(forward):
        result.append(forward)
    # backwards    and below the top of the intersection
    #             and above the bottom of the instersection
    #             and to the right of the left of the intersection
    #             and to the left of the right of the intersection
    backwards = (
        is_on,
        s_x1,
        i_x1 - 1,
        max(s_y1, i_y1), # we cannot go below the intersection
        min(s_y2, i_y2), # we cannot go above the intersection
        max(s_z1, i_z1),
        min(s_z2, i_z2),
    )
    if is_valid(backwards):
        result.append(backwards)
    return result

def split_cubes(step_a, step_b):
    intersection = get_intersection(step_a, step_b)

    return (
        intersection,
        split_by_intersection(intersection, step_a), # step_a split
        split_by_intersection(intersection, step_b), # step_b split
    )
