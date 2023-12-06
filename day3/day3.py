import pprint
import re

numbers = []
symbols = []

lines = open('input', 'r').readlines()
line_number = 0
for line in lines:
    line = line.strip()
    current = None
    index = 0
    while index < len(line):
        match = re.match(r"([0-9]+)", line[index:])
        if match:
            numbers.append((line_number, index, index+len(match.group(1))-1, int(match.group(1))))
            index += len(match.group(1))
        else:
            if line[index] != ".":
                symbols.append((line_number, index, line[index]))
            index += 1
    line_number += 1

total = 0
for part in numbers:
    include = False
    for x in range(part[1] - 1, part[2] + 2):
        for y in range(part[0] - 1, part[0] + 2):
            if [ symbol for symbol in symbols if ( symbol[0] == y and symbol[1] == x ) ]:
                include = True
    if include:
        total += part[3]

print("Advent of Code, Day 3, Part 1")
print(total)

total = 0
for symbol in symbols:
    if symbol[2] == "*":
        adjacent = [ part for part in numbers if ( ( part[0] in (symbol[0] - 1, symbol[0], symbol[0] + 1)) and
                                                   ( ( part[1] >= symbol[1] - 1 and part[1] <= symbol[1] + 1 ) or
                                                     ( part[2] >= symbol[1] - 1 and part[2] <= symbol[1] + 1 ) )
                                                  ) ]
        if len(adjacent) == 2:
            total += adjacent[0][3] * adjacent[1][3]
print("Advent of Code, Day 3, Part 2")
print(total)
