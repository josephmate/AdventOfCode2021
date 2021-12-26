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
from collections import deque
from time import time as current_time


# inp a - Read an input value and write it to variable a.
# add a b - Add the value of a to the value of b, then store the result in variable a.
# mul a b - Multiply the value of a by the value of b, then store the result in variable a.
# div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
# mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
# eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
input_pattern = r'([a-z]+) ([a-z]+)'
operator_variable_pattern = r'([a-z]+) ([a-z]+) ([a-z]+)'
operator_literal_pattern = r'([a-z]+) ([a-z]+) ([0-9-]+)'

def parse_lines(lines):
    alu_instructions = []
    for line in lines:
        line = line.rstrip()

        match = re.search(operator_variable_pattern, line)
        if match != None:
            alu_instructions.append((match.group(1), match.group(2), match.group(3)))
            continue

        match = re.search(operator_literal_pattern, line)
        if match != None:
            alu_instructions.append((match.group(1), match.group(2), int(match.group(3))))
            continue
        
        match = re.search(input_pattern, line)
        if match != None:
            alu_instructions.append((match.group(1), match.group(2)))
            continue

        print(f"Error parsing line: {line}")
    return alu_instructions

def parse_file(filename):
    lines = []
    with open(filename) as reader:
        for line in reader:
            lines.append(line)
    return parse_lines(lines)

sample_2_line = parse_file('sample_2_line.txt')
sample_med = parse_file('sample_med.txt')
sample_large = parse_file('sample_large.txt')
input = parse_file('input.txt')

#print(sample_2_line)
#print(sample_med)
#print(sample_large)
print("\n".join(map(lambda t: str(t), input)))

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
    problem = LpProblem("MONAD_Problem", LpMaximize)
    
    # add variables for each digit of the model number
    model_vars = []
    objective_sum = []
    for i in range(0, 14):
        model_vars.append(LpVariable("model_" + str(i), 1, 9, LpInteger))
        objective_sum.append(model_vars[i]*10**(13-i))
    
    # objective function to maximize
    problem += lpSum(objective_sum), "max_model_number"
    
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
        'x_0': LpVariable('x_0', None, None, LpInteger),
        'y_0': LpVariable('y_0', None, None, LpInteger),
        'z_0': LpVariable('z_0', None, None, LpInteger),
    }
    # all variables start off as 0
    for variable_name in variable_map.keys():
        problem += (
            variable_map[variable_name] == 0,
            f"input_instruction_{variable_name}=0"
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
                f"input_instruction_{new_resolved_variable_name}=model[{current_model_digit}]"
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
                new_var_divisor = LpVariable(new_resolved_variable_name + '_divisor', None, None, LpInteger)
                # create a new variable for the division
                problem += (
                    new_var_divisor*alu_inst[2] <= prev_var
                )
                problem += (
                     prev_var <= (new_var_divisor*(alu_inst[2]+1))-1
                )
                # the division is the remainder of the division
                problem += (
                    new_var == ((new_var_divisor+1) * alu_inst[2]) - new_var_divisor * alu_inst[2]
                )
                # could be exact (remainder 0) so don't allow the modulus value
                problem += (
                    new_var <= alu_inst[2] - 1
                )
                problem += (
                    new_var >= 0
                )
            elif alu_inst[0] == 'eql':
                #eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
                # a2 = [0,1] 
                # 0 = a2*(a1-b1)
                problem += (
                    new_var >= 0
                )
                problem += (
                    new_var <= 1
                )
                problem += (
                    # error from pulp Non-constant expressions cannot be multiplied
                    # nnoooooooo there's no way around this one
                    0 == new_var*(prev_var-alu_inst[2])
                )
            #add a b - Add the value of a to the value of b, then store the result in variable a.
            #mul a b - Multiply the value of a by the value of b, then store the result in variable a.
            #div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
            #mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
            #eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
            # a2 = [0,1] 
            # 0 = a2*(a1-b1)
            else:
                print(f"TODO {alu_inst}")
        else:
            print(f"TODO {alu_inst}")

        variable_counter[unresolved_variable_name] = new_variable_count


#solve_pulp(input)

# I cannot get integer programming to work with modulus
# and cannot figure out a workaround so back to the
# drawing board
debug = False
module_pattern = r'm\d+'
def gen_final_expression(alu_instructions):
    model_counter = 0
    variable_map = {}
    idx = 0
    for alu_inst in alu_instructions:
        idx += 1
        if len(alu_inst) == 2:
            # inp a - Read an input value and write it to variable a.
            variable_map[alu_inst[1]] = deque(["m" + str(model_counter)])
            if debug:
                print(f"{alu_inst} reading m{model_counter} into {alu_inst[1]}")
            model_counter += 1
        else:
            old_eqn = variable_map.get(alu_inst[1], deque(["0"]))

            # optimizations to reduce equation size
            if (alu_inst[0] == 'mul'
                and (
                    (isinstance(alu_inst[2], int) and alu_inst[2] == 0)
                    or (
                        not isinstance(alu_inst[2], int)
                        and len(variable_map.get(alu_inst[2], deque(["0"]))) == 1
                        and variable_map.get(alu_inst[2], deque(["0"]))[0] == "0"
                    )
                    or (
                        len(variable_map.get(alu_inst[1], deque(["0"]))) == 1
                        and variable_map.get(alu_inst[1], deque(["0"]))[0] == "0"
                    )
                )
            ):
                # a * 0 = 0
                # 0 * b = 0
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} 0 multiply optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")
                variable_map[alu_inst[1]] = deque(["0"])
            elif(alu_inst[0] == 'add'
                and (
                    (isinstance(alu_inst[2], int) and alu_inst[2] == 0)
                    or (
                        not isinstance(alu_inst[2], int)
                        and len(variable_map.get(alu_inst[2], deque(["0"]))) == 1
                        and variable_map.get(alu_inst[2], deque(["0"]))[0] == "0"
                    )
                )
            ):
                # a + 0 = a
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} add 0 optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")
                continue
            elif (alu_inst[0] == 'eql'
                and (
                    len(variable_map.get(alu_inst[1], deque(["0"]))) == 1
                    and variable_map.get(alu_inst[1], deque(["0"]))[0] == "0"
                )
                and (
                    not isinstance(alu_inst[2], int)
                    and len(variable_map.get(alu_inst[2], deque(["0"]))) == 1
                    and re.search(module_pattern, variable_map.get(alu_inst[2], deque(["0"]))[0]) != None
                )
            ):
                # 0==m0 -> 0 because modules digits are between 1 and 9
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} 0=m\d+ optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")
                variable_map[alu_inst[1]] = deque(["0"])
            elif (
                (
                    isinstance(alu_inst[2], int)
                    or (
                        not isinstance(alu_inst[2], int)
                        and len(variable_map.get(alu_inst[2], deque(["0"]))) == 1
                        and variable_map.get(alu_inst[2], deque(["0"]))[0].isnumeric()
                    )
                )
                and len(old_eqn) == 1
                and old_eqn[0].isnumeric()
            ):
                # literal op literal = literal
                literal1 = int(old_eqn[0])
                if isinstance(alu_inst[2], int):
                    literal2 = int(alu_inst[2])
                else:
                    literal2 = int(variable_map.get(alu_inst[2], deque(["0"]))[0])
                
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} 2 literals optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")

                if alu_inst[0] == 'add':
                    result = literal1 + literal2
                elif alu_inst[0] == 'mul':
                    result = literal1 * literal2
                elif alu_inst[0] == 'div':
                    result = literal1 // literal2
                elif alu_inst[0] == 'mod':
                    result = literal1 % literal2
                elif alu_inst[0] == 'eql':
                    result = 1 if literal1 == literal2 else 0
                else:
                    print(f"TODO {alu_inst}")
                variable_map[alu_inst[1]] = deque([str(result)])
            elif (alu_inst[0] == 'mul'
                and (
                    (isinstance(alu_inst[2], int) and alu_inst[2] == 1)
                    or (
                        not isinstance(alu_inst[2], int)
                        and len(variable_map.get(alu_inst[2], deque(["0"]))) == 1
                        and variable_map.get(alu_inst[2], deque(["0"]))[0] == "1"
                    )
                )
            ):
                # a * 1 = a
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} a * 1 optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")
                continue
            elif(alu_inst[0] == 'add'
                and (
                    len(variable_map.get(alu_inst[1], deque(["0"]))) == 1
                    and variable_map.get(alu_inst[1], deque(["0"]))[0] == "0"
                )
            ):
                # 0 + b = b
                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} add 0 optimization (ii) {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")
                variable_map[alu_inst[1]] = variable_map[alu_inst[2]]
            else:
                if isinstance(alu_inst[2], int):
                    rhs = str(alu_inst[2])
                elif alu_inst[2].isnumeric():
                    rhs = alu_inst[2]
                else:
                    rhs = variable_map.get(alu_inst[2], deque(["0"]))

                if debug:
                    if isinstance(alu_inst[2], int):
                        other = alu_inst[2]
                    else:
                        other = variable_map.get(alu_inst[2], deque(["0"]))
                    print(f"{alu_inst} no optimization {alu_inst[1]}={variable_map.get(alu_inst[1], deque(['0']))} {alu_inst[2]}={other}")

                #add a b - Add the value of a to the value of b, then store the result in variable a.
                if alu_inst[0] == 'add':
                    operator = '+'
                elif alu_inst[0] == 'mul':
                    operator = '*'
                elif alu_inst[0] == 'div':
                    operator = "/"
                elif alu_inst[0] == 'mod':
                    operator = "%"
                elif alu_inst[0] == 'eql':
                    operator = "=="
                else:
                    print(f"TODO {alu_inst}")
                new_eqn = old_eqn.copy()
                new_eqn.appendleft('(')
                new_eqn.append(operator)
                new_eqn.extend(rhs)
                new_eqn.append(')')
                variable_map[alu_inst[1]] = new_eqn

    return variable_map

#variable_map = gen_final_expression(input)
#print("0 = " + "".join(variable_map["z"]))

# 0 = m13*((((m12*((((m11*((((m10*((((m9*((((m8*((((m7*((((m6*((((m5*((((m4*((((m3*((((m2*((((m1*((((m0*((0==m0)==0))%26)==m1)==0))%26)==m2)==0))%26)==m3)==0))%26)==m4)==0))%26)==m5)==0))%26)==m6)==0))%26)==m7)==0))%26)==m8)==0))%26)==m9)==0))%26)==m10)==0))%26)==m11)==0))%26)==m12)==0))%26)==m13)==0)
# after 0==m0 optimization
# 0 = m13*((((m12*((((m11*((((m10*((((m9*((((m8*((((m7*((((m6*((((m5*((((m4*((((m3*((((m2*((((m1*((((m0*1)%26)==m1)==0))%26)==m2)==0))%26)==m3)==0))%26)==m4)==0))%26)==m5)==0))%26)==m6)==0))%26)==m7)==0))%26)==m8)==0))%26)==m9)==0))%26)==m10)==0))%26)==m11)==0))%26)==m12)==0))%26)==m13)==0)
# notice (m0*1)
# could be simplified to m0
# 0 = m13*((((m12*((((m11*((((m10*((((m9*((((m8*((((m7*((((m6*((((m5*((((m4*((((m3*((((m2*((((m1*(((m0%26)==m1)==0))%26)==m2)==0))%26)==m3)==0))%26)==m4)==0))%26)==m5)==0))%26)==m6)==0))%26)==m7)==0))%26)==m8)==0))%26)==m9)==0))%26)==m10)==0))%26)==m11)==0))%26)==m12)==0))%26)==m13)==0)
#  (((m0%26)==m1)==0)
#  m0%26 == m0
#  ((m0==m1)==0)
#  m0!=m1
# 0 = m13*((((m12*((((m11*((((m10*((((m9*((((m8*((((m7*((((m6*((((m5*((((m4*((((m3*((((m2*((((m1*(m0!=m1))%26)==m2)==0))%26)==m3)==0))%26)==m4)==0))%26)==m5)==0))%26)==m6)==0))%26)==m7)==0))%26)==m8)==0))%26)==m9)==0))%26)==m10)==0))%26)==m11)==0))%26)==m12)==0))%26)==m13)==0)
#   ((m1*(m0!=m1))%26)
#   can drop the %26 since it's m1 * 1 or 0
#   (m1*(m0!=m1))
# 0 = m13*((((m12*((((m11*((((m10*((((m9*((((m8*((((m7*((((m6*((((m5*((((m4*((((m3*((((m2*(((m1*(m0!=m1))==m2)==0))%26)==m3)==0))%26)==m4)==0))%26)==m5)==0))%26)==m6)==0))%26)==m7)==0))%26)==m8)==0))%26)==m9)==0))%26)==m10)==0))%26)==m11)==0))%26)==m12)==0))%26)==m13)==0)
#   m13 * (m12!=m13 or 0)

# tried taking away all the mods because it didn't look like it did anything
# 0 = (m13*(((m12*(((m11*(((m10*(((m9*(((m8*(((m7*(((m6*(((m5*(((m4*(((m3*(((m2*(((m1*((m0==m1)==0))==m2)==0))==m3)==0))==m4)==0))==m5)==0))==m6)==0))==m7)==0))==m8)==0))==m9)==0))==m10)==0))==m11)==0))==m12)==0))==m13)==0))
#   (m13*(((m12*(((m11*(((m10*(((m9*(((m8*(((m7*(((m6*(((m5*(((m4*(((m3*(((m2*(((m1*(m0!=m1)))==m2)==0))==m3)==0))==m4)==0))==m5)==0))==m6)==0))==m7)==0))==m8)==0))==m9)==0))==m10)==0))==m11)==0))==m12)==0))==m13)==0))
#   ??? m13 != m12 != m11 != m11 ... != m0
#   m3*(
#       0==(
#           m3==(
#               m2*(
#                   0==(
#                       m2==(
#                           m1*(
#                               0==(
#                                   m0==m1
#                               )
#                           )
#                       )
#                   )
#               )
#           )
#       )
#   )
#
# m13*(
#   0==(
#     m13==(
#       m12*(
#         0==(
#           (m11*(((m10*(((m9*(((m8*(((m7*(((m6*(((m5*(((m4*(((m3*(((m2*(((m1*(m0!=m1)))==m2)==0))==m3)==0))==m4)==0))==m5)==0))==m6)==0))==m7)==0))==m8)==0))==m9)==0))==m10)==0))==m11)==0))==m12)
#       )
#     )
#   )
# )
# m13 == m12

variable_map = gen_final_expression([
    ("inp", "w"),
    ("inp", "x"),
    ("inp", "y"),
    ("div", "x", "y"),
    ("add", "z", "x"),
])
print("".join(variable_map.get("w", ["0"])))
print("".join(variable_map.get("x", ["0"])))
print("".join(variable_map.get("y", ["0"])))
print("".join(variable_map.get("z", ["0"])))
print()
variable_map = gen_final_expression([
    ("inp", "w"),
    ("inp", "x"),
    ("inp", "y"),
    ("mod", "x", "y"),
    ("add", "z", "x"),
])
print("".join(variable_map.get("w", ["0"])))
print("".join(variable_map.get("x", ["0"])))
print("".join(variable_map.get("y", ["0"])))
print("".join(variable_map.get("z", ["0"])))
print()
variable_map = gen_final_expression([
    ("inp", "w"),
    ("inp", "x"),
    ("inp", "y"),
    ("div", "x", "3"),
    ("add", "z", "x"),
])
print("".join(variable_map.get("w", ["0"])))
print("".join(variable_map.get("x", ["0"])))
print("".join(variable_map.get("y", ["0"])))
print("".join(variable_map.get("z", ["0"])))
print()

# after fixing my bugs, my optimizations do very little
# to reduce the length of the equation
# looks like there is a lot of stuff to solve
# variable_map = gen_final_expression(input)
# print("0 = " + "".join(variable_map["z"]))

INPUT = 0
ADD = 1
MULTIPLY = 2
DIVIDE = 3
MODULUS = 4
EQUAL = 5
VARIABLE = 0
LITERAL = 1

def make_efficient_instructions(alu_instructions):
    varible_to_register_map = {
        'w': 0,
        'x': 1,
        'y': 2,
        'z': 3,
    }

    efficient_instructions = []
    for alu_inst in alu_instructions:
        if alu_inst[0] == "inp":
            efficient_instructions.append((INPUT, varible_to_register_map[alu_inst[1]]))
        else:
            if isinstance(alu_inst[2], int):
                literal_or_var = LITERAL
                value = alu_inst[2]
            elif alu_inst[2].isnumeric():
                literal_or_var = LITERAL
                value = int(alu_inst[2])
            else:
                literal_or_var = VARIABLE
                value = varible_to_register_map[alu_inst[2]]
            
            if alu_inst[0] == 'add':
                operator = ADD
            elif alu_inst[0] == 'mul':
                operator = MULTIPLY
            elif alu_inst[0] == 'div':
                operator = DIVIDE
            elif alu_inst[0] == 'mod':
                operator = MODULUS
            elif alu_inst[0] == 'eql':
                operator = EQUAL
            else:
                print(f"TODO {alu_inst}")
            
            efficient_instructions.append((operator, varible_to_register_map[alu_inst[1]], literal_or_var, value))


    return efficient_instructions

def run_instructions(efficient_instructions, function_input):
    registers = [
        0,
        0,
        0,
        0,
    ]
    input_idx = 0
    for inst in efficient_instructions:
        inst_type = inst[0]
        destination_register = inst[1]
        register_value = registers[destination_register]
        if inst_type == INPUT:
            registers[destination_register] = function_input[input_idx]
            input_idx += 1
        else:
            if inst[2] == LITERAL:
                value = inst[3]
            else:
                value = registers[inst[3]]
            
            if inst_type == ADD:
                registers[destination_register] = register_value + value
            elif inst_type == MULTIPLY:
                registers[destination_register] = register_value * value
            elif inst_type == DIVIDE:
                registers[destination_register] = register_value // value
            elif inst_type == MODULUS:
                registers[destination_register] = register_value % value
            elif inst_type == EQUAL:
                registers[destination_register] = 1 if register_value == value else 0

    return registers


insts = make_efficient_instructions(parse_lines("""inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
""".splitlines()))
print("\n".join(map(lambda t: str(t), insts)))
print()
print("\n".join(map(lambda t: str(t), run_instructions(insts, [1]))))
print()
print("\n".join(map(lambda t: str(t), run_instructions(insts, [2]))))
print()
print("\n".join(map(lambda t: str(t), run_instructions(insts, [4]))))
print()
print("\n".join(map(lambda t: str(t), run_instructions(insts, [8]))))
print()
print("\n".join(map(lambda t: str(t), run_instructions(insts, [15]))))
print()

def find_monad_slow(alu_instructions):
    efficient_instructions = make_efficient_instructions(alu_instructions)
    
    for a in range (9, 1-1, -1): # 1 : 5.3 years
        for b in range (9, 1-1, -1): # 2 : 215 days
            for c in range (9, 1-1, -1): # 3 : 23.9203125 days
             for d in range (9, 1-1, -1): # 4 : 63.7875 hours
                for e in range (9, 1-1, -1): # 5 : 7.0875 hours
                    for f in range (9, 1-1, -1): # 6 : 47.25 minutes
                        for g in range (9, 1-1, -1): # 7 : 315 seconds per loop (5.25 min)
                            print(g)
                            start = current_time()
                            for h in range (9, 1-1, -1): # 8 : 35 seconds per loop
                                for i in range (9, 1-1, -1): # 9 : 4 seconds per loop
                                    for j in range (9, 1-1, -1): # 10
                                        for k in range (9, 1-1, -1): # 11
                                            for l in range (9, 1-1, -1): # 12
                                                for m in range (9, 1-1, -1): # 13
                                                    for n in range (9, 1-1, -1): # 14
                                                        result = run_instructions(
                                                            efficient_instructions,
                                                            [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
                                                        )
                                                        if result[3] == 0:
                                                            return [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
                            end = current_time()
                            print(end-start)
    return None
            

# running the program 9^14 times will take 5 years :(
#find_monad_slow(input)

# break up the lines by input to check if there
# is any difference
lines = []
with open('input.txt') as reader:
    for line in reader:
        line = line.rstrip()
        lines.append(line)

split_by_input = []
current_split = []
for line in lines:
    if line.startswith("inp"):
        if len(current_split) > 0:
             split_by_input.append(current_split)
        current_split = []
    current_split.append(line)
if len(current_split) > 0:
    split_by_input.append(current_split)

longest_split = max(map(lambda split: len(split), split_by_input))
longest_line = max(map(lambda s: len(s), lines))

for r in range(0, longest_split):
    for c in range(0, len(split_by_input)):
        if r < len(split_by_input[c]):
            line = split_by_input[c][r]
        else:
            line = ""
        suffix = ""
        for i in range(0, longest_line - len(line) + 3):
            suffix += " "
        print(f"{line}{suffix}", end="")
    print()

# each input follows the pattern:
# inp w        # load next input
# mul x 0      # x register to 0
# add x z      # copy whatever is accumuated so far from z to x
# mod x 26
# div z 1      # sometimes this is 1, sometimes this is 26
#              # div by 1 does nothing
#              # mod by 26 then div by 26 is always 0
# add x 12     # this is a random number
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 1
# mul y x
# add z y
