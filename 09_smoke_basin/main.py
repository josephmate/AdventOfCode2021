import sys
import re
from queue import PriorityQueue


pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda columns : list(map(lambda column : int(column), columns)),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)
num_cols = len(input[0])
num_rows = len(input)

def check_adjacent_higher(lava_map, r, c):
    if r - 1 >= 0 and lava_map[r-1][c] <= lava_map[r][c]:
        return False
    if c - 1 >= 0 and lava_map[r][c-1] <= lava_map[r][c]:
        return False
    if r + 1 < num_rows and lava_map[r+1][c] <= lava_map[r][c]:
        return False
    if c + 1 < num_cols and lava_map[r][c+1] <= lava_map[r][c]:
        return False

    return True

count = 0
for r in range(0, num_rows):
    for c in range(0, num_cols):
        if check_adjacent_higher(input, r, c):
            count += 1 + input[r][c]
print(count)

# sorted by height ascending
posn_to_expand_queue = PriorityQueue()
posn_to_basn = []
for r in range(0, num_rows):
    current_row = []
    for c in range(0, num_cols):
        if check_adjacent_higher(input, r, c):
            posn_to_expand_queue.put((input[r][c], ((r, c),(r, c))))
        current_row.append(None) # no basin yet
    posn_to_basn.append(current_row)

def merge_basins(posn_to_basn, basin1_r, basin1_c, basin2_r, basin2_c):
    print("MERGE") # was never printed so we don't need to implement this
    print((basin1_r, basin1_c, basin2_r, basin2_c))

while not posn_to_expand_queue.empty():
    (height, ((r, c), (basin_r, basin_c))) = posn_to_expand_queue.get()
    # the height of the current position
    # the row of the current position
    # the column of the current position
    # the row of the basic the current position is being investigated by
    #     used for handling collisions
    # the col of the basic the current position is being investigated by
    #     used for handling collisions
    #print((height, ((r, c), (basin_r, basin_c))))

    # already visited and has appropriate basin
    if posn_to_basn[r][c] == (basin_r, basin_c):
        continue
    # need to merge basins
    if posn_to_basn[r][c] != None:
        merge_basins(posn_to_basn, posn_to_basn[r][c][0], posn_to_basn[r][c][1], basin_r, basin_c)
        continue
    
    posn_to_basn[r][c] = (basin_r, basin_c)
    if r - 1 >= 0 and input[r-1][c] < 9:
        posn_to_expand_queue.put((input[r-1][c], ((r-1, c), (basin_r, basin_c))))
    if c - 1 >= 0 and input[r][c-1] < 9:
        posn_to_expand_queue.put((input[r][c-1], ((r, c-1), (basin_r, basin_c))))
    if r + 1 < num_rows and input[r+1][c] < 9:
        posn_to_expand_queue.put((input[r+1][c], ((r+1, c), (basin_r, basin_c))))
    if c + 1 < num_cols and input[r][c+1] < 9:
        posn_to_expand_queue.put((input[r][c+1], ((r, c+1), (basin_r, basin_c))))


basin_size_count = {}
for r in range(0, num_rows):
    for c in range(0, num_cols):
        if posn_to_basn[r][c] != None:
            basin_size_count[posn_to_basn[r][c]] = basin_size_count.get(posn_to_basn[r][c], 0) + 1

print(basin_size_count)
sizes = []
for size in basin_size_count.values():
    sizes.append(size)
sizes.sort(reverse=True)
print (sizes[0]*sizes[1]*sizes[2])
