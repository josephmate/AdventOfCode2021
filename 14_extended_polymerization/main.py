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

print("""
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
""")

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

polymer = polymer_template
for step in range(1, 10+1):
    polymer = apply_rules(polymer, insertion_rules_map)
counts = {}
for c in polymer:
    counts[c] = counts.get(c, 0) + 1
min_freq = min(counts.values())
max_freq = max(counts.values())
diff = max_freq - min_freq
print("1749 - 161 = 1588")
print(f"{max_freq} - {min_freq} = {diff}")


polymer = polymer_template
for step in range(1, 40+1):
    polymer = apply_rules(polymer, insertion_rules_map)
counts = {}
for c in polymer:
    counts[c] = counts.get(c, 0) + 1
min_freq = min(counts.values())
max_freq = max(counts.values())
diff = max_freq - min_freq
print("2192039569602 - 3849876073 = 2188189693529")
print(f"{max_freq} - {min_freq} = {diff}")

