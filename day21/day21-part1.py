from itertools import chain

start = None

rocks = set()
width = None

y = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if not line:break
    if width is None:
        width = len(line)
    for x in range(len(line)):
        if line[x] == "#":
            rocks.add((x, y))
        if line.find("S") != -1:
            start = (line.find("S"), y)
    y += 1
height = len(lines)

def can_reach(point):
    good = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if abs(x) + abs(y) > 1:
                continue
            if point[x] + x < 0 or point[x] + x >= width:
                continue
            if point[y] + y < 0 or point[y] + y >= height:
                continue
            if (point[0] + x, point[1] + y) not in rocks:
                good.append((point[0] + x, point[1] + y))
    return set(good)

current_spots = can_reach(start)
for i in range(63):
    current_spots = set(chain.from_iterable([ can_reach(location) for location in current_spots ]))


print("Advent of Code, Day 21, Part 1")
print(len(current_spots))

