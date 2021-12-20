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