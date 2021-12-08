import sys
import re

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda columns : [columns[0], columns[1].split(" ")],
    map(lambda line : line.split(" | "),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))))

print(input)

seven_segment_display = [
    set(['a', 'b', 'c', 'e', 'f', 'g']),      # 0
    set(['c', 'f']),                          # 1
    set(['a', 'c', 'd', 'e', 'g']),           # 2
    set(['a', 'c', 'd', 'f', 'g']),           # 3
    set(['b', 'c', 'd', 'f']),                # 4
    set(['a', 'b', 'd', 'f', 'g']),           # 5
    set(['a', 'b', 'd', 'e', 'f', 'g']),      # 6
    set(['a', 'c', 'f']),                     # 7
    set(['a', 'b', 'c', 'd', 'e', 'f', 'g']), # 8
    set(['a', 'b', 'c', 'd', 'f', 'g']),      # 9
]

group_by_num_of_segments = {}
for i in range(0, len(seven_segment_display)):
    num_segments = len(seven_segment_display[i])
    if num_segments in group_by_num_of_segments:
        group_by_num_of_segments[num_segments].append(i)
    else:
        group_by_num_of_segments[num_segments] = [i]

print(group_by_num_of_segments)

num_of_uniq = 0
for (_, displays) in input:
    for display in displays:
        print(f"{len(display)} {display}")
        if len(group_by_num_of_segments[len(display)]) == 1:
            num_of_uniq += 1
print(num_of_uniq)