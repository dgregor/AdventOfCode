import pprint

rocks = set()
slopes = {}
points = {}

start_point = None
width = None
y = 0
last_line = None
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    last_line = line
    if width is None:
        width = len(line)
    if start_point is None:
        start_point = (line.find("."), y)
    for x in range(len(line)):
        if line[x] == "#":
            rocks.add((x, y))
        elif line[x] in (">", "<", "^", "v"):
            slopes[(x, y)] = line[x]
    y += 1

height = y
exit_point = (last_line.find("."), y-1)

for x in range(width):
    for y in range(height):
        if (x, y) in rocks:
            continue
        points[(x, y)] = []
        for x2, y2 in [ (-1, 0), (1, 0), (0, 1), (0, -1) ]:
            if x + x2 < 0 or x + x2 >= width:
                continue
            if y + y2 < 0 or y + y2 >= height:
                continue
            if (x + x2, y + y2) in rocks:
                continue
            if (x, y) in slopes:
                if slopes[(x, y)] == ">" and x2 != 1:
                    continue
                elif slopes[(x, y)] == "<" and x2 != -1:
                    continue
                elif slopes[(x, y)] == "^" and y2 != -1:
                    continue
                elif slopes[(x, y)] == "v" and y2 != 1:
                    continue
            points[(x, y)].append((x + x2, y + y2))

complete_paths = []
to_check = [ (start_point, set([start_point]) ) ]
while to_check:
    path = to_check.pop()
    current = path[0]
    seen = path[1]
    if current == exit_point:
        complete_paths.append(seen)
        continue
    for next_point in points[current]:
        if next_point in seen:
            continue
        now_seen = seen.copy()
        now_seen.add(current)
        to_check.append((next_point, now_seen))
print("Advent of Code, Day 23, Part 1")
print(max([ len(i) for i in complete_paths]))
