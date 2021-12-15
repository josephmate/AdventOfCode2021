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

print(input)
num_rows = len(input)
num_cols = len(input[0]) # all rows have same length
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

def get_next_moves(r,c):
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

max_distance = num_rows*num_cols*10
shortest_paths = {
    (0,0): 0
}
paths = {
    (0,0): [(0,0)]
}
queue = Queue()
queue.put((0,0,0, [(0,0)]))
while not queue.empty():
    (r,c,risk,path) = queue.get()
    for (next_r,next_c) in get_next_moves(r,c):
        next_risk = risk + input[r][c]
        if next_risk < shortest_paths.get((next_r,next_c), max_distance):
            shortest_paths[(next_r,next_c)] = next_risk
            next_path = path.copy()
            next_path.append((next_r,next_c))
            paths[(next_r,next_c)] = next_path
            queue.put((next_r,next_c,next_risk,next_path))

print("sample.txt 40")
print(paths[(num_rows-1,num_cols-1)])

def print_path(path):
    path_set = set(path)
    for r in range(0, num_rows):
        for c in range(0, num_cols):
            if (r,c) in path_set:
                print(">" + str(input[r][c]), end="")
            else:
                print(" " + str(input[r][c]), end="")
        print("")

print_path(paths[(num_rows-1,num_cols-1)])
print(shortest_paths[(num_rows-1,num_cols-1)])

manual_cost = -input[0][0]
for (r,c) in path:
    manual_cost += input[r][c]
print(manual_cost)