import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)

def parse_scanner(index, input):
    scanner = []
    index += 1

    while index < len(input) and input[index] != "":
        cols = input[index].split(",")
        scanner.append((int(cols[0]),int(cols[1]),int(cols[2])))
        index += 1
    index += 1

    return (index, scanner)

def parse_input(input):
    index = 0
    scanners = []
    while index < len(input):
        (index, scanner) = parse_scanner(index, input)
        scanners.append(scanner)
    return scanner

scanners = parse_input(input)
print (scanners)

