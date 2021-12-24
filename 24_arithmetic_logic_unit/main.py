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

# log(9^14)/log(2)
# = 44
# aprox 2^44 possible inputs
# as a result we cannot brute for this
# iterating over 2^44 will take about 28 minutes to 14 hours...
# binary search doesn't make sense because the possible values
# are not sorted by valid/invalid
# 
# Maybe there's a way to start from z=0 at the end of the input
# and solve it backwards. For example the last 5 lines of my
# input are:
# mul y 0
# add y w
# add y 1
# mul y x
# add z y
# We can develop a system of equations:
# z1 = 0
# z1 = z2 + y1
# y1 = y2 + x1
# y2 = y3 + 1
# y3 = y4 + w1
# y4 = y5 * 0
#   y4 = 0
#   y3 = w1
#   y2 = w1 + 1

# pip3 install python-constraint
# from constraint import *
# tried implemented wit python-constraint and 
# discovered that the variable range needs to be defined
# and I have no idea what the range on some of the variables are

# pip3 install pulp
from pulp import *

def solve_pulp(alu_instructions):
    problem = LpProblem("MONAD Problem", LpMaximize)
    
    # add variables for each digit of the model number
    model_vars = []
    objective_sum = []
    for i in range(0, 14):
        model_vars.append(LpVariable("model_" + str(i), 1, 9, LpInteger))
        objective_sum.append(model_vars[i]*10**(13-i))
    
    # objective function to maximize
    problem += lpSum(objective_sum), "max model number"
    
    current_model_digit = 0
    variable_counter = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }
    # map of string to the pulp variable
    variable_map = {
        'w_0': LpVariable('w_0', None, None, LpInteger),
        'x_0': LpVariable('w_0', None, None, LpInteger),
        'y_0': LpVariable('w_0', None, None, LpInteger),
        'z_0': LpVariable('w_0', None, None, LpInteger),
    }
    # all variables start off as 0
    for variable_name in variable_map.keys():
        problem += (
            variable_map[variable_name] == 0,
            f"input instruction {variable_name}=0"
        )

    for alu_inst in alu_instructions:
        unresolved_variable_name = alu_inst[1]
        new_variable_count = variable_counter[unresolved_variable_name] + 1
        new_resolved_variable_name = unresolved_variable_name + "_" + str(new_variable_count)
        new_var = LpVariable(new_resolved_variable_name, None, None, LpInteger)
        variable_map[new_resolved_variable_name] = new_var
        if len(alu_inst) == 2:
            # inp a - Read an input value and write it to variable a.
            problem += (
                variable_map[new_resolved_variable_name] == model_vars[current_model_digit],
                f"input instruction {new_resolved_variable_name}=model[{current_model_digit}]"
            )
            current_model_digit += 1
        elif isinstance(alu_inst[2], int):
            prev_var_name = alu_inst[1] + "_" + str(variable_counter[alu_inst[1]])
            prev_var = variable_map[prev_var_name]

            #add a b - Add the value of a to the value of b, then store the result in variable a.
            if alu_inst[0] == 'add':
                problem += (
                    new_var == prev_var + alu_inst[2]
                )
            elif alu_inst[0] == 'mul':
                problem += (
                    new_var == prev_var * alu_inst[2]
                )
            elif alu_inst[0] == 'div':
                # integer division not implemented in pulp :(
                # even if you reformulate it to 
                # new_var*alu_inst[2] == prev_var
                # that doesn't work because it doesn't get the values that were rounded down
                # but what does integer division really mean?
                # it means:
                # new_var*alu_inst[2] <= prev_var
                # and
                # new_var*(alu_inst[2]+1) > prev_var
                problem += (
                    new_var*alu_inst[2] <= prev_var
                )
                problem += (
                    # TypeError: '>' not supported between instances of 'LpAffineExpression' and 'LpVariable'
                    # so need to use >= somehow
                    # since it's integer we can reduce by 1
                    # and that should get us the <=
                    prev_var <= new_var*(alu_inst[2]+1)-1
                )
            elif alu_inst[0] == 'mod':
                continue
                # modulus not implemented in pulp :(
                problem += (
                    new_var == prev_var % alu_inst[2]
                )
            #add a b - Add the value of a to the value of b, then store the result in variable a.
            #mul a b - Multiply the value of a by the value of b, then store the result in variable a.
            #div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
            #mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
            #eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
            # a2 = [0,1] 
            # 0 = a2*(a1-b1)
            print("TODO")

        variable_counter[unresolved_variable_name] = new_variable_count


solve_pulp(input)

# so integer programming won't work so now back to the drawing board
