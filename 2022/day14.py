import functools
import time
import pprint
import re
import sys

lines = open('input-14', 'r').readlines()

segments = []
for line in lines:
    line = line.strip()
    parts = line.split(" -> ")
    for i in range(1, len(parts)):
        segments.append([[int(parts[i-1].split(",")[0]), int(parts[i-1].split(",")[1])],
                         [int(parts[i].split(",")[0]), int(parts[i].split(",")[1])]])

min_y = 0
max_y = 0
min_x = 500
max_x = 0
for segment in segments:
    max_y = max(max_y, segment[0][1], segment[1][1])
    min_x = min(min_x, segment[0][0], segment[1][0])
    max_x = max(max_x, segment[0][0], segment[1][0])

max_y += 2
min_x -= 200
max_x += 200

width = max_x - min_x + 1
height = max_y - min_y + 1

grid = [ ["."] * width for i in range(height) ]
grid[height-1] = ["x"] * width

for segment in segments:
    if segment[0][0] == segment[1][0]:
        # vertical
        for i in range(min(segment[0][1], segment[1][1]),
                       max(segment[0][1], segment[1][1]) + 1):
            x = segment[0][0] - min_x
            y = i - min_y
            grid[y][x] = "x"
    else:
        # horizontal
        for i in range(min(segment[0][0], segment[1][0]),
                       max(segment[0][0], segment[1][0]) + 1):
            x = i - min_x
            y = segment[0][1] - min_y
            grid[y][x] = "x"

def sand():
    global grid
    x = 500 - min_x
    y = 0
    if grid[y][x] == "o":
        return False
    while True:
#        print(x, y)
        if y == height - 1:
            return False
        if grid[y+1][x] == ".":
            y += 1
        elif x == 0:
            grid[y][x] = "o"
            break
            #return False
        elif grid[y+1][x-1] == ".":
            x -= 1
            y += 1
        elif x == width - 1:
            grid[y][x] = "o"
            break
            #return False
        elif grid[y+1][x+1] == ".":
            x += 1
            y += 1
        else:
            grid[y][x] = "o"
            break
    return True

#for line in grid:
#    print("".join(line))

print(min_x, max_x, width, min_y, max_y, height)

count = 0
while sand():
    count += 1
    #if count > 900:
    #    for line in grid[-50:]:
    #        print("".join(line))
    #if count > 1500:
    #    sys.exit()
    continue

#for line in grid:
#x    print("".join(line))

print(count)
