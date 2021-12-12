import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue


input = list(
    map(lambda line : line.split('-'),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)

# caves to set of connected caves
cave_map = {}
for (cave1, cave2) in input:
    if not cave1 in cave_map:
        cave_map[cave1] = set()    
    cave_map[cave1].add(cave2)
    # bi-directional
    if not cave2 in cave_map:
        cave_map[cave2] = set()    
    cave_map[cave2].add(cave1)

def is_big_cave(cave):
    ascii = ord(cave[0])
    return ascii >= 65 and ascii <= 90

def traverse_caves(cave_map, max_visits=1):
    num_of_paths = 0
    # BFS
    bfs_queue = Queue()
    bfs_queue.put(('start', ['start'], {'start': max_visits}))
    while not bfs_queue.empty():
        (current_cave, path_so_far, visited_so_far) = bfs_queue.get()
        
        for next_cave in cave_map[current_cave]:
            if next_cave == 'end':
                print(f"{path_so_far} {next_cave}")
                num_of_paths += 1
            elif is_big_cave(next_cave):
                path_branch = path_so_far.copy()
                path_branch.append(next_cave)
                bfs_queue.put((next_cave, path_branch, visited_so_far))
            elif visited_so_far.get(next_cave, 0) < max_visits:
                path_branch = path_so_far.copy()
                visited_branch = visited_so_far.copy()
                path_branch.append(next_cave)
                visited_branch[next_cave] = visited_branch.get(next_cave, 0) + 1
                bfs_queue.put((next_cave, path_branch, visited_branch))
    
    return num_of_paths
            

num_of_paths = traverse_caves(cave_map)
print("sample.txt 10 sample2.txt 19 sample3.txt 226")
print(num_of_paths)

num_of_paths = traverse_caves(cave_map, 2)
print("sample.txt 36 sample2.txt 103 sample3.txt 3509")
print(num_of_paths)