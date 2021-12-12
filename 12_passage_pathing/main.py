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

def traverse_caves(cave_map):
    num_of_paths = 0
    # BFS
    bfs_queue = Queue()
    bfs_queue.put(('start', ['start'], set(['start'])))
    while not bfs_queue.empty():
        (current_cave, path_so_far, visited_so_far) = bfs_queue.get()

        for next_cave in cave_map[current_cave]:
            if next_cave == 'end':
                print(f"{path_so_far} {next_cave}")
                num_of_paths += 1
            elif is_big_cave(next_cave) or not next_cave in visited_so_far:
                path_branch = path_so_far.copy()
                visited_branch = visited_so_far.copy()
                path_branch.append(next_cave)
                visited_branch.add(next_cave)
                bfs_queue.put((next_cave, path_branch, visited_branch))

    return num_of_paths
            
num_of_paths = traverse_caves(cave_map)

print("sample.txt 10 sample2.txt 19 sample3.txt 226")
print(num_of_paths)


def traverse_caves_at_most_twice(cave_map):
    num_of_paths = 0
    # BFS
    bfs_queue = Queue()
    bfs_queue.put(('start', ['start'], False, set(['start'])))
    while not bfs_queue.empty():
        (current_cave, path_so_far, visited_twice, visited_so_far) = bfs_queue.get()
        
        for next_cave in cave_map[current_cave]:
            if next_cave == 'end':
                print(f"{path_so_far} {next_cave}")
                num_of_paths += 1
            elif next_cave == 'start':
                continue
            elif is_big_cave(next_cave) or not next_cave in visited_so_far:
                path_branch = path_so_far.copy()
                visited_branch = visited_so_far.copy()
                path_branch.append(next_cave)
                visited_branch.add(next_cave)
                bfs_queue.put((next_cave, path_branch, visited_twice, visited_branch))
            elif next_cave in visited_so_far and not visited_twice:
                path_branch = path_so_far.copy()
                visited_branch = visited_so_far.copy()
                path_branch.append(next_cave)
                visited_branch.add(next_cave)
                bfs_queue.put((next_cave, path_branch, True, visited_branch))
    
    return num_of_paths


num_of_paths = traverse_caves_at_most_twice(cave_map)
print("sample.txt 36 sample2.txt 103 sample3.txt 3509")
print(num_of_paths)
