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

debug = True

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
    (1,3): '-',
    (1,4): '.',
    (1,5): '-',
    (1,6): '.',
    (1,7): '-',
    (1,8): '.',
    (1,9): '-',
    (1,10): '.',
    (1,11): '.',
    (2,3): 'A',
    (3,3): 'A',
    (4,3): 'A',
    (5,3): 'A',
    (2,5): 'B',
    (3,5): 'B',
    (4,5): 'B',
    (5,5): 'B',
    (2,7): 'C',
    (3,7): 'C',
    (4,7): 'C',
    (5,7): 'C',
    (2,9): 'D',
    (3,9): 'D',
    (4,9): 'D',
    (5,9): 'D',
}
sample = parse_file('sample.txt')
input = parse_file('input.txt')
print("\n".join(map(lambda pair: str(pair), cave_map.items())))
print()
print("\n".join(map(lambda pair: str(pair), sample.items())))
print()
print("\n".join(map(lambda pair: str(pair), input.items())))
print()


def print_map(amphipod_map, depth):
    for r in range (1,1+depth+1):
        for c in range (1,11+1):
            if (r,c) in amphipod_map:
                print(amphipod_map[(r,c)], end="")
            elif r == 1:
                print('.', end="")
            elif c in [3,5,7,9]:
                print('.', end="")
            else:
                print(" ", end="")
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
    for d in range(r-1, 2-1,-1):
        if (d,c) in amphipod_map:
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

# This is not a valid move:
# ...B...A.D.
#   . C B .  
#   A D C .  
# 
# ('A', (1, 8), (2, 3), 6, 2029)
# ...B.....D.
#   A C B .  
#   A D C . 
def get_move_into_room(amphipod_map, move_from, depth):
    letter = amphipod_map[(move_from)]
    if letter == 'A':
        column = 3
    elif letter == 'B':
        column = 5
    elif letter == 'C':
        column = 7
    else:# letter == 'D':
        column = 9

    # go in as far as possible
    destination = None
    for d in range(depth-1, 0-1, -1):
        r = d + 2
        if (r,column) not in amphipod_map:
            destination = r
            break
    # Couldn't find a spot
    if destination == None:
        return None

    # is there anything blocking within the room?
    for rr in range(r-1, 2-1, -1):
        if (rr,column) in amphipod_map and amphipod_map[(rr,column)] != letter:
            return None
    
    # is there anyone blocking the path on the way to the room?
    (r,c) = move_from
    if c <= column:
        for i in range(c+1, column+1):
            if (r,i) in amphipod_map:
                return None
    else: # c > column:
        for i in range(c-1, column, -1):
            if (r,i) in amphipod_map:
                return None

    return (letter, move_from, (destination, column))

def try_leaving_room(amphipod_map, c, depth) :
    for current_depth in range(0, depth):
        r = current_depth + 2
        if (r,c) in amphipod_map and not amphipod_map[(r,c)] == cave_map[(r,c)]:
            return get_moves_to_hallway(amphipod_map,(r,c))
        elif (r,c) in amphipod_map:
            # matches, but is there anyone after that I need to move for?
            all_match = True
            for j in range(current_depth+1, depth):
                rr = j + 2
                if not amphipod_map[(rr,c)] == cave_map[(rr,c)]:
                    all_match = False
                    break
            if not all_match or current_depth+1 == depth:
                return get_moves_to_hallway(amphipod_map,(r,c))
    return []


def get_moves(amphipod_map, depth):
    moves = []
    # moving out of the rooms
    for c in [3,5,7,9]:
        moves.extend(try_leaving_room(amphipod_map, c, depth))

    # moving out of the hallway
    for c in [1,2,4,6,8,10,11]:
        # if some one is in the halway
        if (1,c) in amphipod_map:
            move = get_move_into_room(amphipod_map, (1,c), depth)
            if not move == None:
                moves.append(move)


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

def min_energy(amphipod_map, depth):
    priority_queue = []
    id = 0
    visited = {}
    visited[freezemap(amphipod_map)] = 0
    paths = {}
    heappush(priority_queue, (0, 0, amphipod_map.copy(), []))
    while len(priority_queue) > 0:
        current_energy, _, current_map, path = heappop(priority_queue)
        for letter, move_from, move_to in get_moves(current_map, depth):
            additional_energy = energy(letter) * man_dist(move_from, move_to)
            next_energy = current_energy + additional_energy
            next_map = current_map.copy()
            del next_map[move_from]
            next_map[move_to] = letter
            next_map_frozen = freezemap(next_map)
            if next_map_frozen not in visited or next_energy < visited[next_map_frozen]:
                new_path = path.copy()
                new_path.append((letter, move_from, move_to, additional_energy, next_energy))
                visited[next_map_frozen] = next_energy
                paths[next_map_frozen] = new_path
                id = id + 1
                heappush(priority_queue, (next_energy, id, next_map, new_path))

    end_result = {}
    for i in range(0, depth):
        end_result[(i+2,3)] = 'A'
        end_result[(i+2,5)] = 'B'
        end_result[(i+2,7)] = 'C'
        end_result[(i+2,9)] = 'D'
    end_result_frozen = freezemap(end_result)
    return (visited[end_result_frozen], paths[end_result_frozen])




print("expected: 12521")
(me, path) = min_energy(sample, 2)
print(f"actual:   {me}")

def print_path(path, amphipod_map, depth):
    amphipod_map = amphipod_map.copy()
    print_map(amphipod_map, 2)
    for step in path:
        print()
        print(str(step))
        letter, move_from, move_to, _, _ = step
        del amphipod_map[move_from]
        amphipod_map[move_to] = letter
        print_map(amphipod_map, depth)

#print_path(path, sample, 2)

#print("puzzle input:")
#(me, path) = min_energy(input,2)
#print(me)

def unfold(amphipod_map):
    return {
        (2,3): amphipod_map[(2,3)],
        (3,3): 'D',
        (4,3): 'D',
        (5,3): amphipod_map[(3,3)],
        (2,5): amphipod_map[(2,5)],
        (3,5): 'C',
        (4,5): 'B',
        (5,5): amphipod_map[(3,5)],
        (2,7): amphipod_map[(2,7)],
        (3,7): 'B',
        (4,7): 'A',
        (5,7): amphipod_map[(3,7)],
        (2,9): amphipod_map[(2,9)],
        (3,9): 'A',
        (4,9): 'C',
        (5,9): amphipod_map[(3,9)],
    }

unfolded_sample = unfold(sample)
unfolded_input = unfold(input)

print()
print_map(unfolded_sample, 4)
print()
print_map(unfolded_input, 4)

print("expected: 44169")
(me, path) = min_energy(unfolded_sample, 4)
print()
