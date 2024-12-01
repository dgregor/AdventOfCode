#     A B C
#   A D E F C
# A D E G E F C
# H E G E G E I
# J K E G E L M
#   J K E L M
#     J N M

import pprint
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
    for x, y in ( (-1, 0), (1, 0), (0, -1), (0, 1) ):
        if ((point[0] + x) % width, (point[1] + y) % height) not in rocks:
            good.append((point[0] + x, point[1] + y))
    return set(good)

def get_counts(spots):
    vals = {}
    for spot in spots:
        x_grid = spot[0] // width
        y_grid = spot[1] // height
        vals.setdefault((x_grid, y_grid), 0)
        vals[(x_grid, y_grid)] += 1
    return vals

ACROSS = 9
ACROSS_RANGE = list(range((-ACROSS // 2) + 1, (ACROSS // 2) + 1))

starting = {}
current_spots = set([start])
i = 1

while True:
    current_spots = set(chain.from_iterable([ can_reach(location) for location in current_spots ]))
    counts = get_counts(current_spots)
    missing = False
    for key in counts.keys():
        if starting.get(key) is None:
            starting[key] = {}
        starting[key][i] = counts[key]
    if i in [ (129 + (131 * j) + 67) for j in range(8) ]:
        print(i)
        for y in range(max( [ cell[1] for cell in counts.keys() ] ), min( [ cell[1] for cell in counts.keys() ] ) - 1, -1 ):
            print( " ".join([ f'{counts.get((x, y)):>8}' if (x, y) in counts else "        " for x in range(min( [ cell[0] for cell in counts.keys() ] ), max( [ cell[0] for cell in counts.keys() ] ) + 1 ) ]))
        import pprint
        pprint.pprint(starting)
    i += 1

