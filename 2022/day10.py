import pprint
import re
import sys

register_values = [0]
next_value = 1

crt = []

lines = open('input-10', 'r').readlines()
for line in lines:
    line = line.strip()
    register_values.append(next_value)
    crt_position = (len(register_values) - 2) % 40
    if crt_position == 0:
        crt.append([])
    if abs(register_values[-1] - crt_position) <= 1:
        crt[-1].append("X")
    else:
        crt[-1].append(".")
    if line.startswith("addx"):
        register_values.append(register_values[-1])
        next_value += int(line.split()[1])
        crt_position = (len(register_values) - 2) % 40
        if crt_position == 0:
            crt.append([])
        if abs(register_values[-1] - crt_position) <= 1:
            crt[-1].append("X")
        else:
            crt[-1].append(".")
    else:
        next_value = register_values[-1]

for row in crt:
    print("".join(row))

