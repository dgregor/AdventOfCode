import pprint
import re
import sys

grand_total = 0

def get_dir_size(directory):
    if directory['size'] > 0:
        return directory['size']
    total = 0
    for item, value in directory['contents'].items():
        if isinstance(value, int):
            total += value
        else:
            total += get_dir_size(value)
    directory['size'] = total
    if total <= 100000:
        global grand_total
        grand_total += total

    return total

contents = { '/': { 'size': 0,
                    'contents': {} } }

stack = []

lines = open('input-7', 'r').readlines()
for line in lines:
    line = line.strip()
    if line.startswith("$ cd"):
        if line == "$ cd /":
            stack = ["/"]
        elif line == "$ cd ..":
            stack.pop()
        else:
            parts = line.split()
            stack.append(parts[2])
    elif line.startswith("$ ls"):
        continue
    else:
        this_dir = contents
        for part in stack:
            this_dir = this_dir[part]['contents']
        parts = line.split()
        if parts[0] == "dir":
            this_dir.setdefault(parts[1], { 'size': 0, 'contents': {} })
        else:
            this_dir[parts[1]] = int(parts[0])

get_dir_size(contents['/'])

print(grand_total)

min_dir = 70000000
free_space = 30000000 - (70000000 - contents['/']['size'])

def check_dir(directory):
    global free_space
    global min_dir
    print(directory['size'], free_space, min_dir)
    if (directory['size'] > free_space) and (directory['size'] < min_dir):
        min_dir = directory['size']
    for item, value in directory['contents'].items():
        if not isinstance(value, int):
            check_dir(value)

check_dir(contents['/'])
print(free_space)
print(min_dir)
