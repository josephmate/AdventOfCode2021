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
from heapq import *

# on x=10..12,y=10..12,z=10..12
# off x=9..11,y=9..11,z=9..11
pattern = r'(\w+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)'
def parse_file(filename):
    amphipod_map = {}
    with open(filename) as reader:
        r = 0
        for line in reader:
            line = line.rstrip()
            for c in range(0, len(line)):
                if line[c] in ['A', 'B', 'C', 'D']:
                    amphipod_map[(r,c)] = line[c]
            r+=1
    return amphipod_map

cave_map = {
    (1,1): '.',
    (1,2): '.',
    (1,3): 'M',
    (1,4): '.',
    (1,5): 'M',
    (1,6): '.',
    (1,7): 'M',
    (1,8): '.',
    (1,9): 'M',
    (1,10): '.',
    (1,11): '.',
    (2,3): 'A',
    (3,3): 'A',
    (2,5): 'B',
    (3,5): 'B',
    (2,7): 'C',
    (3,7): 'C',
    (2,9): 'D',
    (3,9): 'D',
}
sample = parse_file('sample.txt')
input = parse_file('input.txt')
print("\n".join(map(lambda pair: str(pair), cave_map.items())))
print()
print("\n".join(map(lambda pair: str(pair), sample.items())))
print()
print("\n".join(map(lambda pair: str(pair), input.items())))
print()


# Amphipods will never stop on the space immediately outside any room.
#   They can move into that space so long as they immediately continue moving.
#   (Specifically, this refers to the four open spaces in the hallway that are
#    directly above an amphipod starting position.)
# Amphipods will never move from the hallway into a room unless that room is
#   their destination room and that room contains no amphipods which do not
#   also have that room as their own destination. If an amphipod's starting
#   room is not its destination room,
#   it can stay in that room until it leaves the room.
#   (For example, an Amber amphipod will not move from the hallway into the
#   right three rooms,
#   and will only move into the leftmost room if that room is empty or if it
#   only contains other Amber amphipods.)
# Once an amphipod stops moving in the hallway,
#   it will stay in that spot until it can move into a room.
#   (That is, once any amphipod starts moving,
#   any other amphipods currently in the hallway are locked in place and will
#   not move again until they can move fully into a room.)

def is_home(posn):
    r,_ = posn
    return r == 2 or r == 3

def is_hallway(posn):
    r,_ = posn
    return r == 1

def get_moves_to_hallway(amphipod_map, move_from):
    (r,c) = move_from
    # something is blocking on the way out, so return nothing
    if c == 3 and (r,2) in amphipod_map:
        return []
    
    letter = amphipod_map[move_from]
    moves = []
    # move from doormat to the left until you hit something
    for leftc in range(c-1, 1-1, -1):
        if (1,leftc) not in amphipod_map:
            if cave_map[(1,leftc)] == '.':
                moves.append((letter, move_from, (1,leftc)))
        else:
            break
    # move from doormat to the right until you hit something
    for rightc in range(c+1, 11+1, 1):
        if (1,rightc) not in amphipod_map:
            if cave_map[(1,rightc)] == '.':
                moves.append((letter, move_from, (1,rightc)))
        else:
            break
    return moves

def get_move_into_room(amphipod_map, move_from):
    letter = amphipod_map[(move_from)]
    if letter == 'A':
        column = 3
    elif letter == 'B':
        column = 5
    elif letter == 'C':
        column = 7
    else:# letter == 'D':
        column = 9

    # is anyone blocking the front position?
    # then there's no way we can go to the front or back position
    if (2,column) in amphipod_map:
        return None
    
    # is there anyone blocking the path on the way to the room?
    (r,c) = move_from
    if c <= column:
        for i in range(c+1, column+1):
            if (r,i) in amphipod_map:
                return None
    else: # c > column:
        for i in range(column, c, -1):
            if (r,i) in amphipod_map:
                return None

    if (3,column) not in amphipod_map:
        row = 3
    else:
        row = 2

    return (letter, move_from, (row, column))

def get_moves(amphipod_map):
    moves = []
    # moving out of the rooms
    # at least one in the room is not correct, so we need to vacate them
    for c in [3,5,7,9]:
        if not amphipod_map.get((2,c), '') == cave_map[(2,c)] or not amphipod_map[(3,c)] == cave_map[(3,c)]:
            # the top guy must move if he's there
            if (2,c) in amphipod_map:
                moves.extend(get_moves_to_hallway(amphipod_map,(2,c)))
            # the bottom guy moves if he's not already in the right location
            #   and there is no one blocking him
            if (3,c) in amphipod_map and not amphipod_map[(3,c)] == cave_map[(3,c)] and (2,c) not in amphipod_map:
                moves.extend(get_moves_to_hallway(amphipod_map,(3,c)))

    for c in [1,2,4,6,8,10,11]:
        # if some one is in the halway
        if (1,c) in amphipod_map:
            move = get_move_into_room(amphipod_map, (1,c))
            if not move == None:
                moves.append(move)


    # moving out of the hallway
    return moves

def man_dist(a, b):
    (ar, ac) = a
    (br, bc) = b
    return abs(ar-br) + abs(ac-bc)

# Amber amphipods require 1 energy per step,
# Bronze amphipods require 10 energy,
# Copper amphipods require 100,
# and Desert ones require 1000.
def energy(letter):
    if letter == 'A':
        return 1
    if letter == 'B':
        return 10
    if letter == 'C':
        return 100
    else: # letter == 'D':
        return 1000

def freezemap(mutable_map):
    frozenmap = []
    for (r,c), value in mutable_map.items():
        frozenmap.append((r,c,value))
    frozenmap.sort()
    return tuple(frozenmap)

def min_energy(amphipod_map):
    priority_queue = []
    id = 0
    visited = {}
    visited[freezemap(amphipod_map)] = 0
    heappush(priority_queue, (0, 0, amphipod_map.copy()))
    while len(priority_queue) > 0:
        current_energy, _, current_map = heappop(priority_queue)
        for letter, move_from, move_to in get_moves(current_map):
            next_energy = current_energy + energy(letter) * man_dist(move_from, move_to)
            next_map = current_map.copy()
            del next_map[move_from]
            next_map[move_to] = letter
            next_map_frozen = freezemap(next_map)
            if next_map_frozen not in visited or next_energy < visited[next_map_frozen]:
                visited[next_map_frozen] = next_energy
                id = id + 1
                heappush(priority_queue, (next_energy, id, next_map))

    end_result = {
        (2,3): 'A',
        (3,3): 'A',
        (2,5): 'B',
        (3,5): 'B',
        (2,7): 'C',
        (3,7): 'C',
        (2,9): 'D',
        (3,9): 'D',
    }
    return visited[freezemap(end_result)]




print("expected: 12521")
print(min_energy(sample))
