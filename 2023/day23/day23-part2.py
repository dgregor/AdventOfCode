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
            points[(x, y)].append((x + x2, y + y2))

# build up line segments
line_segments = {}
seen = set()
to_check = [ (start_point, next_point) for next_point in points[start_point] ]
while to_check:
    path = to_check.pop()
    segment_start_point = path[0]
    segment_end_point = path[1]
    if ( segment_start_point, segment_end_point) in seen:
        continue
    seen.add( (segment_start_point, segment_end_point) )
    count = 1
    prev_point = segment_start_point
    while True:
        count += 1
        next_points = points[segment_end_point]
        if len(next_points) != 2:
            break
        else:
            if next_points[0] == prev_point:
                prev_point = segment_end_point
                segment_end_point = next_points[1]
            else:
                prev_point = segment_end_point
                segment_end_point = next_points[0]
    if len(next_points) == 1:
        if segment_end_point == exit_point:
            line_segments.setdefault(segment_start_point, []).append((segment_end_point, count))
        else:
            # dead end
            continue
    else:
        line_segments.setdefault(segment_start_point, []).append((segment_end_point, count))
        if len(next_points) > 2:
            for next_point in next_points:
                if next_point == prev_point:
                    continue
                to_check.append((segment_end_point, next_point))
complete_paths = []
to_check = [ (start_point, 0, set()) ]
count = 0
while to_check:
    count += 1
    if count % 10000 == 0:
        print(count)
        print(len(complete_paths), [ i[0] for i in complete_paths])
    path = to_check.pop()
    current = path[0]
    count = path[1]
    seen = path[2]
    if current == exit_point:
        complete_paths.append([count, seen])
        continue
    for next_segment in line_segments[current]:
        next_segment_point = next_segment[0]
        next_segment_count = next_segment[1]
        if next_segment_point in seen:
            continue
        now_seen = seen.copy()
        now_seen.add(current)
        to_check.append((next_segment_point, count + next_segment_count - 1, now_seen))

print("Advent of Code, Day 23, Part 2")
print(max([ i[0] for i in complete_paths]))
