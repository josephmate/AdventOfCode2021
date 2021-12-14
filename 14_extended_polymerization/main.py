import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)
print(input[0])
print(input[2:len(input)])

pattern = r'(\w+) -> (\w+)'
polymer_template = input[0]
insertion_rules = list(
    map(lambda match: (match.group(1), match.group(2)),
    map(lambda line: re.search(pattern, line),
    input[2:len(input)])))

print(polymer_template)
print(insertion_rules)


def apply_rules(polymer, insertion_rules_map):
    buffer = [polymer[0]]

    first_char = polymer[0]
    for i in range(1, len(polymer)):
        second_char = polymer[i]
        potential_pair = first_char + second_char
        if potential_pair in insertion_rules_map:
            buffer.append(insertion_rules_map[potential_pair])
        buffer.append(second_char)
        first_char = second_char

    return ''.join(buffer) # efficient string concat

insertion_rules_map = {}
for (pair, insert) in insertion_rules:
    insertion_rules_map[pair] = insert

polymer = polymer_template
polymer = apply_rules(polymer, insertion_rules_map)
print( "Expected: NCNBCHB")
print(f"Actual:   {polymer}")
polymer = apply_rules(polymer, insertion_rules_map)
print( "Expected: NBCCNBBBCBHCB")
print(f"Actual:   {polymer}")
polymer = apply_rules(polymer, insertion_rules_map)
print( "Expected: NBBBCNCCNBBNBNBBCHBHHBCHB")
print(f"Actual:   {polymer}")
polymer = apply_rules(polymer, insertion_rules_map)
print( "Expected: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")
print(f"Actual:   {polymer}")

def count_freq(polymer):
    counts = {}
    for c in polymer:
        counts[c] = counts.get(c, 0) + 1
    return counts

def min_max_freq(polymer):
    counts = count_freq(polymer)
    min_freq = min(counts.values())
    max_freq = max(counts.values())
    diff = max_freq - min_freq
    return (diff, max_freq, min_freq)

polymer = polymer_template
for step in range(1, 10+1):
    polymer = apply_rules(polymer, insertion_rules_map)
(diff, max_freq, min_freq) = min_max_freq(polymer)
print("1749 - 161 = 1588")
print(f"{max_freq} - {min_freq} = {diff}")


def make_polymer_tracker(polymer):
    first_char = prev_char = polymer[0]
    last_char = polymer[len(polymer)-1]
    polymer_map = {}
    for c in polymer:
        second_char = c
        pair = prev_char + second_char
        polymer_map[pair] = polymer_map.get(pair, 0) + 1
        prev_char = second_char
    # first char and last char are not double counted
    # so the need to be added back or something.
    # I haven't figured out but I'm pretty sure they need
    # to be handled separately
    return (first_char, last_char, polymer_map)

def apply_rules_fast(polymer_map, insertion_rules):
    # TODO
    return polymer_map

def count_polymer_map(first_char, last_char, polymer_map):
    print(first_char)
    print(last_char)
    count = {}
    for (pair, freq) in polymer_map.items():
        count[pair[0]] = count.get(pair[0], 0) + freq
        count[pair[1]] = count.get(pair[1], 0) + freq
    
    count[first_char] = count[first_char] - 1
    count[last_char] = count[last_char] - 1

    final_count = {}
    for (c, freq) in count.items():
        final_count[c] = freq // 2
    final_count[first_char] = final_count[first_char] + 1
    final_count[last_char] = final_count[last_char] + 1
    return final_count

# try part 1 again but more efficiently
(first_char, last_char, polymer_map) = make_polymer_tracker(polymer_template)
print(f"Expected: {count_freq('NNCB')}")
print(f"Actual:   {count_polymer_map(first_char, last_char, polymer_map)}")
polymer_map = apply_rules_fast(polymer_map, insertion_rules_map)
print(f"Expected: {count_freq('NCNBCHB')}")
print(f"Actual:   {count_polymer_map(first_char, last_char, polymer_map)}")
polymer_map = apply_rules_fast(polymer_map, insertion_rules_map)
print(f"Expected: {count_freq('NBCCNBBBCBHCB')}")
print(f"Actual:   {count_polymer_map(first_char, last_char, polymer_map)}")
polymer_map = apply_rules_fast(polymer_map, insertion_rules_map)
print(f"Expected: {count_freq('NBBBCNCCNBBNBNBBCHBHHBCHB')}")
print(f"Actual:   {count_polymer_map(first_char, last_char, polymer_map)}")
polymer_map = apply_rules_fast(polymer_map, insertion_rules_map)
print(f"Expected: {count_freq('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')}")
print(f"Actual:   {count_polymer_map(first_char, last_char, polymer_map)}")

polymer = polymer_template
for step in range(1, 10+1):
    polymer = apply_rules(polymer, insertion_rules_map)
(diff, max_freq, min_freq) = min_max_freq(polymer)
print("1749 - 161 = 1588")
print(f"{max_freq} - {min_freq} = {diff}")