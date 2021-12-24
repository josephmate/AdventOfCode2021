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
import time




# inp a - Read an input value and write it to variable a.
# add a b - Add the value of a to the value of b, then store the result in variable a.
# mul a b - Multiply the value of a by the value of b, then store the result in variable a.
# div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
# mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
# eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
input_pattern = r'([a-z0-9-]+) ([a-z0-9-]+)'
operator_variable_pattern = r'([a-z]+) ([a-z]+) ([a-z]+)'
operator_literal_pattern = r'([a-z]+) ([a-z]+) ([0-9-]+)'
def parse_file(filename):
    alu_instructions = []
    with open(filename) as reader:
        r = 0
        for line in reader:
            line = line.rstrip()

            match = re.search(operator_variable_pattern, line)
            if match != None:
                alu_instructions.append((match.group(1), match.group(2), match.group(3)))
                continue

            match = re.search(operator_literal_pattern, line)
            if match != None:
                alu_instructions.append((match.group(1), match.group(2), int(match.group(3))))
                continue
            
            match = re.search(operator_literal_pattern, line)
            if match != None:
                alu_instructions.append((match.group(1), match.group(2)))
                continue

            print(f"Error parsing line: {line}")
    return alu_instructions

sample_2_line = parse_file('sample_2_line.txt')
sample_med = parse_file('sample_med.txt')
sample_large = parse_file('sample_large.txt')
input = parse_file('input.txt')

print(sample_2_line)
print(sample_med)
print(sample_large)
print(input)