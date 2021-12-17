import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))
hex = input[0]

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
        print(f"{tab(tabs)} index={index} version={binary_packet[index:index+3]}")
        version = binary_to_int(binary_packet[index:index+3])
        index += 3
        type = binary_to_int(binary_packet[index:index+3])
        index += 3

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