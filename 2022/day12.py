import time
import pprint
import re
import sys

lines = open('input-12', 'r').readlines()

grid = []

MAX = 1000000

start = None
end = None

def eval_cell(x, y):
    global min_grid
    global grid
    to_check = []
    if y > 0:
        if min_grid[y-1][x] > min_grid[y][x] and grid[y-1][x] >= grid[y][x] - 1:
            min_grid[y-1][x] = min_grid[y][x] + 1
            to_check.append((x, y-1))
    if y < len(min_grid) - 1:
        if min_grid[y+1][x] > min_grid[y][x] and grid[y+1][x] >= grid[y][x] - 1:
            min_grid[y+1][x] = min_grid[y][x] + 1
            to_check.append((x, y+1))
    if x > 0:
        if min_grid[y][x-1] > min_grid[y][x] and grid[y][x-1] >= grid[y][x] - 1:
            min_grid[y][x-1] = min_grid[y][x] + 1
            to_check.append((x-1, y))
    if x < len(min_grid[0]) - 1:
        if min_grid[y][x+1] > min_grid[y][x] and grid[y][x+1] >= grid[y][x] - 1:
            min_grid[y][x+1] = min_grid[y][x] + 1
            to_check.append((x+1, y))
    return to_check

for line in lines:
    line = line.strip()
    if line.find("S") > -1:
        start = (line.find("S"), len(grid))
        line = line.replace("S", "a")
    if line.find("E") > -1:
        end = (line.find("E"), len(grid))
        line = line.replace("E", "z")
    grid.append([ ord(x) for x in line ])

min_grid = [ [MAX] * len(grid[0]) for i in range(len(grid)) ]
min_grid[end[1]][end[0]] = 0

to_check = set([(end[0], end[1])])
checked = 0
while to_check:
    this_cell = to_check.pop()
    checked += 1
    print(checked, "checked")
    print(len(to_check), "to check")
    print(this_cell)
    for additional_cell in eval_cell(this_cell[0], this_cell[1]):
#        print(additional_cell)
        to_check.add(additional_cell)

for row in min_grid:
    print(" ".join([ str(x) for x in row]))

overall_min = 1000
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == ord("a"):
            if min_grid[y][x] < overall_min:
                overall_min = min_grid[y][x]
print(overall_min)
