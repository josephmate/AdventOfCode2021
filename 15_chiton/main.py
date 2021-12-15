import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : list(map(lambda c: int(c), line)),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

num_rows = len(input)
num_cols = len(input[0]) # all rows have same length


def print_risk_map(risk_map):
    for row in risk_map:
        for ch in row:
            print(ch, end="")
        print("")
print_risk_map(input)
print(f"num_rows={num_rows} num_cols={num_cols}")


# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581

#            1
# (0,0) -> (0,1)      7
#                -> (0,2)
#                     4
#                -> (1,1)
#            1
# (0,0) -> (1,0)      4
#                -> (1,1) [duplicated so check if smaller, otherwise drop search]
#                     3
#                -> (2,0)  

def get_next_moves(r,c, num_rows, num_cols):
    moves = []
    if r - 1 >= 0:
        moves.append((r-1, c))
    if c - 1 >= 0:
        moves.append((r, c-1))
    if r + 1 < num_rows:
        moves.append((r+1, c))
    if c + 1 < num_cols:
        moves.append((r, c+1))
    return moves

def solve(risk_map):
    num_rows = len(risk_map)
    num_cols = len(risk_map[0])
    max_distance = num_rows*num_cols*10
    shortest_paths = {
        (0,0): 0
    }
    queue = PriorityQueue()
    queue.put((0, (0,0)))
    while not queue.empty():
        (risk, (r,c)) = queue.get()
        for (next_r,next_c) in get_next_moves(r,c, num_rows, num_cols):
            next_risk = risk + risk_map[next_r][next_c]
            if next_risk < shortest_paths.get((next_r,next_c), max_distance):
                shortest_paths[(next_r,next_c)] = next_risk
                queue.put((next_risk, (next_r,next_c)))
    return shortest_paths[(num_rows-1,num_cols-1)]

def print_path(risk_map, path):
    num_rows = len(risk_map)
    num_cols = len(risk_map[0])
    path_set = set(path)
    for r in range(0, num_rows):
        for c in range(0, num_cols):
            if (r,c) in path_set:
                print(">" + str(risk_map[r][c]), end="")
            else:
                print(" " + str(risk_map[r][c]), end="")
        print("")

smallest_risk = solve(input)
#(smallest_risk, shortest_path) = solve(input)
#print_path(input, shortest_path)
print("sample.txt 40")
print(smallest_risk)

bigger_risk_map = []
for r_tile in range(0,5):
    for r in range(0, num_rows):
        current_row = []
        for c_tile in range(0,5):
            for c in range(0, num_cols):
                tiled_risk = input[r][c] + r_tile + c_tile
                if tiled_risk > 9:
                    tiled_risk = tiled_risk - 9
                current_row.append(tiled_risk)
        bigger_risk_map.append(current_row)

print_risk_map(bigger_risk_map)
num_rows = len(bigger_risk_map)
num_cols = len(bigger_risk_map[0]) # all rows have same length
print(f"num_rows={num_rows} num_cols={num_cols}")
smallest_risk = solve(bigger_risk_map)
#(smallest_risk, shortest_path) = solve(bigger_risk_map)
#print_path(bigger_risk_map, shortest_path)
print("sample.txt 315")
print(smallest_risk)