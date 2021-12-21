import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

image_enhancement_algorithm = input[0]
input_image = input[2:]

print(image_enhancement_algorithm)
print()
print(input_image)
print()

light_pixels = set()
for r in range(0,len(input_image)):
    for c in range (0, len(input_image[r])):
        if input_image[r][c] == '#':
            light_pixels.add((r,c))

def print_light_pixels(light_pixels):
    min_r = min(map(lambda rc: rc[0], light_pixels))
    max_r = max(map(lambda rc: rc[0], light_pixels))
    min_c = min(map(lambda rc: rc[1], light_pixels))
    max_c = max(map(lambda rc: rc[1], light_pixels))

    for r in range(min_r, max_r+1):
        for c in range(min_c, max_c+1):
            if (r,c) in light_pixels:
                print("#", end="")
            else:
                print(".", end="")
        print()

print_light_pixels(light_pixels)
print()


# originally, I was thinking to optimize this similar to the game of life
# where i keep track of the live/lit cells. Then only the lit cells and
# neighbours need to be considered for the calculation of the next step.
# This looked like it would work because the sample image enhancement
# algorithm had a dark/unlit for the 0th position.
# In the actual input it's 1! That means there are an infinite number of
# lit cells to track. That's not possible.
#
# Then I thought, what if I just compute the nth step recursively, without
# storing anything. I could hard code a bounding box and adjust it as needed
# until I get a decent looking result.

def gen_points_to_consider(r,c):
    return [
        (r-1,c-1), (r-1,c), (r-1,c+1),
        (r  ,c-1), (r  ,c), (r  ,c+1),
        (r+1,c-1), (r+1,c), (r+1,c+1),
    ]

def binary_to_int(binary_num):
    result = 0
    power = 1
    for i in range(len(binary_num)-1, 0-1, -1):
        result += binary_num[i]*power
        power *= 2
    return result

def calc_posn(light_pixels, steps, r, c):
    if steps == 0:
        return "#" if (r,c) in light_pixels else "."
    else:
        points_to_consider = gen_points_to_consider(r, c)
        binary_num = []
        for (consider_r, consider_c) in points_to_consider:
            digit = 1 if calc_posn(light_pixels, steps -1, consider_r, consider_c) == "#" else 0
            binary_num.append(digit)
        return image_enhancement_algorithm[binary_to_int(binary_num)]


def calc_nth_step(light_pixels, steps):
    min_r = -steps*4
    min_c = -steps*4
    max_r = len(input_image) + steps*4
    max_c = len(input_image[0]) + steps*4

    result = []
    for r in range(min_r, max_r+1):
        current_row = []
        for c in range(min_c, max_c+1):
            current_row.append(calc_posn(light_pixels, steps, r, c))
        result.append("".join(current_row))
    return result

one_step = calc_nth_step(light_pixels, 1)
two_step = calc_nth_step(light_pixels, 2)

print(
    "\n".join(one_step)
)
print(
    "\n".join(two_step)
)

count = 0
for row in two_step:
    for ch in row:
        if ch == "#":
            count+=1
print(count)


fifty_step = calc_nth_step(light_pixels, 50)
count = 0
for row in fifty_step:
    for ch in row:
        if ch == "#":
            count+=1
print(count)