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

# lets say we're facing the x 'into the screen'
# y is going 'up'
# z is left and right
#
#       y   x
#       |  /
#       | /
# ------+------- z
#      /
#     /
# if we're rotating around the x axis, we can ignore the x component
# and we're left with:
#
# (y=3,z=-2)
#       y
#     d |   (y=2, z=3)
#       |  a
#       |   
# ------+------- z
#       |    
#    c  |  
#       |  b (y=-3, z=2)
# (y=-2, z=-3)
# swap then multiply y by -1 gets the result we need:
# ( 2,  3)
# (-3,  2)
# (-2, -3)
# ( 3, -2)
def rotate_around_x(coords):
    rotated = []
    for (x, y, z) in coords:
        rotated.append((x, z*-1, y))
    return rotated

def rotate_around_z(coords):
    rotated = []
    for (x, y, z) in coords:
        rotated.append((y*-1, x, z))
    return rotated

def rotate_around_y(coords):
    rotated = []
    for (x, y, z) in coords:
        rotated.append((z*-1, y, x))
    return rotated


def flip_x(coords):
    flipped_coords = []
    for (x,y,z) in coords:
        flipped_coords.append((x*-1,y,z))
    return flipped_coords
def flip_y(coords):
    flipped_coords = []
    for (x,y,z) in coords:
        flipped_coords.append((x,y*-1,z))
    return flipped_coords
def flip_z(coords):
    flipped_coords = []
    for (x,y,z) in coords:
        flipped_coords.append((x,y,z*-1))
    return flipped_coords

def swap(coords, col1, col2):
    swapped = []
    for coord in coords:
        swapped_cord = [0, 0, 0]
        swapped_cord[col1] = coord[col2]
        swapped_cord[col2] = coord[col1]
        swapped.append(swapped_cord)
    return swapped

def generate_orientations(coords):
    # rotate 90 degrees on yz 3 times to get all the up directions
    # flip
    # rotate 90 degrees on yz 3 times to get all the up directions
    # swap x and y of original
    #   rotate 90 degrees on 'new yz' 3 times to get all the up directions
    #   flip
    #   rotate 90 degrees 'new yz' 3 times to get all the up directions
    # swap x and z of original
    #   rotate 90 degrees 'new yz' 3 times to get all the up directions
    #   flip
    #   rotate 90 degrees 'new yz' 3 times to get all the up directions
    orientations = [coords]
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( flip_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    
    #       y   x
    #       |  /
    #       | /
    # ------+------- z
    #      /
    #     /
    # If I'm facing the x axis but I want to face the y axis, then I need to
    # rotated about the z axis
    orientations.append(rotate_around_z(coords))
    # now I can rotate as if I'm facing the x-axis?
    # nah, I think it makes more sense to rotate in y?
    # nah, the result looks weird. the (1,0,0) repeated as
    #   4 (1,0,0), 4 (0,1,0) 4 (0,0,1)
    #   so i'm going back to rotating around x
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( flip_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    # same thing but instead turn to face the y axis
    orientations.append(rotate_around_y(coords))
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( flip_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    orientations.append( rotate_around_x(orientations[len(orientations)-1]) )
    return orientations  



for orientation in generate_orientations([(1,0,0)]):
    print(orientation)

def render_absolute_map(scanners):
    # find the scanners that are common with 0,
    # then use the values from the orientation that match
    # also figure out the translation and translate those coords
    # then regenerate the orientations relative to scanner 0
    # so that the reset are scanner 0
    # remove scanner 0 from the pool
    # try with the next list of potential scanners
    # remove it after done
    # keep doing this until no more scanners left
    scanner_queue = Queue()
    scanner_queue.put(scanners[0])
    unprocessed_scanners = Queue()
    for i in range(1, len(scanners)):
        scanner_queue.put(scanners[i])
    
    processed_scanners = []
    while not scanner_queue.empty():
        next_scanner = scanner_queue.get()

    print("TODO")
