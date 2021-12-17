import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import math

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))
hex = input[0]

DEBUG = False

decode_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

def hex_to_binary(hex):
    binary = ""
    for c in hex:
        binary = binary + decode_map[c]
    return binary

print("Expected: 110100101111111000101000")
print(f"Actual:   {hex_to_binary('D2FE28')}")

def binary_to_int(binary):
    result = 0
    power = 1
    for i in range(len(binary)-1, 0-1, -1):
        result += int(binary[i]) * power
        power = power * 2
    return result

print("Expected: 6")
print(f"Actual:   {binary_to_int('110')}")
print("Expected: 5")
print(f"Actual:   {binary_to_int('101')}")
print("Expected: 4")
print(f"Actual:   {binary_to_int('100')}")

def parse_literal_packet(binary_packet):
    version = binary_to_int(binary_packet[0:3])
    type = binary_to_int(binary_packet[3:6])

    binary_literal = ""
    for i in range(6, len(binary_packet), 5):
        cont = binary_packet[i]
        binary_literal += binary_packet[i+1:i+5]
        if cont == "0":
            break

    return (version, type, binary_to_int(binary_literal))

print("Expected: version=6 type=4 literal=2021")
(version, type, literal) = parse_literal_packet(hex_to_binary('D2FE28'))
print(f"Actual:   version={version} type={type} literal={literal}")



def tab(tabs):
    res = ""
    for i in range(0, tabs):
        res += "  "
    return res

def process_literal(binary_packet, index):
    binary_literal = ""
    while True:
        cont = binary_packet[index]
        binary_literal += binary_packet[index+1:index+5]
        index += 5
        if cont == "0":
            break

    return (index, binary_to_int(binary_literal))

def process_length_type_0(binary_packet, index, tabs):
    length = binary_to_int(binary_packet[index:index+15])
    index+=15
    (_, res) = process_packet(binary_packet, index, index+length, len(binary_packet), tabs+1)
    return (index+length, length, res)

def process_length_type_1(binary_packet, index, tabs):
    length = binary_to_int(binary_packet[index:index+11])
    index+=11
    (index, packets) = process_packet(binary_packet, index, len(binary_packet), length, tabs+1)
    return (index, length, packets)

def process_packet(binary_packet, index, end, times, tabs):
    packets = []

    current_times = 0
    while index+6 < end and current_times < times:
        if DEBUG:
            print(f"{tab(tabs)} index={index} version={binary_packet[index:index+3]}")
        version = binary_to_int(binary_packet[index:index+3])
        index += 3
        type = binary_to_int(binary_packet[index:index+3])
        index += 3
        if DEBUG:
            print(f"{tab(tabs)}{version} {type}")

        if type == 4: # literal
            (index, packet) = process_literal(binary_packet, index)
            packets.append((version, type, packet))
        else: # operator
            length_type = int(binary_packet[index])
            index += 1
            if length_type == 0:
                (index, length, sub_packets) = process_length_type_0(binary_packet, index, tabs)
                packets.append((version, type, (length, sub_packets)))
            elif length_type == 1:
                (index, length, sub_packets) = process_length_type_1(binary_packet, index, tabs)
                packets.append((version, type, (length, sub_packets)))
            else:
                print(f"unsupported index={index} type={type} length_type={length_type}")

        current_times += 1
    
    return (index, packets)

def decode(hex):
    binary = hex_to_binary(hex)
    (_, res) = process_packet(binary, index=0, end=len(binary), times=len(binary), tabs=0)
    return res

print("")
print(decode("D2FE28"))
print("")
print(decode("38006F45291200"))
print("")
print(decode("EE00D40C823060"))

print("sample.txt 16   sample2.txt 12   sample3.txt 23   sample4.txt 31")

def count_version_num(packets):
    sum = 0

    for (version, type, data) in packets:
        sum += version
        if type != 4:
            (_, sub_packets) = data
            sum += count_version_num(sub_packets)

    return sum

print(count_version_num(decode("8A004A801A8002F478")))
print("16")
print("")
print(count_version_num(decode("620080001611562C8802118E34")))
print("12")
print(count_version_num(decode("C0015000016115A2E0802F182340")))
print("23")
print("")
print(count_version_num(decode("A0016C880162017C3686B18A3D4780")))
print("31")
print("")
print(decode(hex))
print(count_version_num(decode(hex)))


def evaluate_impl(packet):
    (version, type, data) = packet
    if type == 4: # literal
        return data
    else:
        (_, sub_packets) = data
        #Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        if type == 0:
            return sum(map(lambda sub_packet: evaluate_impl(sub_packet), sub_packets))
        #Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        elif type == 1:
            return math.prod(map(lambda sub_packet: evaluate_impl(sub_packet), sub_packets))
        #Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        elif type == 2:
            return min(map(lambda sub_packet: evaluate_impl(sub_packet), sub_packets))
        #Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        elif type == 3:
            return max(map(lambda sub_packet: evaluate_impl(sub_packet), sub_packets))
        else:
            sub_packets = list(map(lambda sub_packet: evaluate_impl(sub_packet), sub_packets))
            #Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
            if type == 5:
                if sub_packets[0] > sub_packets[1]:
                    return 1
                else:
                    return 0
            #Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
            elif type == 6:
                if sub_packets[0] < sub_packets[1]:
                    return 1
                else:
                    return 0
            #Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
            elif type == 7:
                if sub_packets[0] == sub_packets[1]:
                    return 1
                else:
                    return 0
            else:
                print("ERROR")
                return -1

def evaluate(packets):
    return evaluate_impl(packets[0])


print("")
print(evaluate(decode("C200B40A82")))
print("3")
print("")
print(evaluate(decode("04005AC33890")))
print("54")
print("")
print(evaluate(decode("880086C3E88112")))
print("7")
print("")
print(evaluate(decode("CE00C43D881120")))
print("9")
print("")
print(evaluate(decode("D8005AC2A8F0")))
print("1")
print("")
print(evaluate(decode("F600BC2D8F")))
print("0")
print("")
print(evaluate(decode("9C005AC2F8F0")))
print("0")
print("")
print(evaluate(decode("9C0141080250320F1802104A08")))
print("1")
print("")


print(evaluate(decode(hex)))