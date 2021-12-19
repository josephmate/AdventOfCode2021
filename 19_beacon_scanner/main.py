import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)

def parse_scanner(index, input):
    scanner = []
    index += 1

    while index < len(input) and input[index] != "":
        cols = input[index].split(",")
        scanner.append((int(cols[0]),int(cols[1]),int(cols[2])))
        index += 1
    index += 1

    return (index, scanner)

def parse_input(input):
    index = 0
    scanners = []
    while index < len(input):
        (index, scanner) = parse_scanner(index, input)
        scanners.append(scanner)
    return scanner

scanners = parse_input(input)
print (scanners)

# default orientation is
# facing_sign = 1 (positive)
# facing = 0  (x axis)
# up direction
def generate_orientation_v1(scanner, facing_sign, facing, up_direction):

    return []

def generate_orientations_v1(scanner):
    orientations = []

    # facing positive or negative
    facing_signs = [1, -1]
    # x, y, or z
    facings = [0,1,2]
    # any of four directions "up" from that facing.
    up_directions = [
        ( 1, 0),
        ( 0, 1),
        (-1, 0),
        ( 0,-1),
    ]

    for facing_sign in facing_signs:
        for facing in facings:
            for up_direction in up_directions:
                orientations.append(generate_orientation_v1(scanner, facing_sign, facing, up_direction))


    return orientations


def generate_orientations(scanner):
    # rotate 90 degrees 3 times to get all the up directions
    # flip
    # rotate 90 degrees 3 times to get all the up directions
    # swap x and y of original
    #   rotate 90 degrees 3 times to get all the up directions
    #   flip
    #   rotate 90 degrees 3 times to get all the up directions
    # swap x and z of original
    #   rotate 90 degrees 3 times to get all the up directions
    #   flip
    #   rotate 90 degrees 3 times to get all the up directions


for orientation in generate_orientations([(1,0,0)]):
    print(orientation)