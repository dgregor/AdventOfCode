import pprint

bricks = []
bricks_after_fall = []

max_x = 0
max_y = 0
max_z = 0

def my_range(val_a, val_b):
    return range(min(val_a, val_b), max(val_a, val_b) + 1)

count = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    first = line.split("~")[0]
    second = line.split("~")[1]
    brick = ( tuple(map(int, first.split(","))), tuple(map(int, second.split(","))), count)
    max_x = max(max_x, brick[0][0], brick[1][0])
    max_y = max(max_y, brick[0][1], brick[1][1])
    max_z = max(max_z, brick[0][2], brick[1][2])
    bricks.append(brick)
    count += 1

brick_supports = [ set() ] * count

maximums = [ [(0,-1)] * (max_y + 1) for i in range(max_x + 1) ]

bricks_by_z = {}
for brick in bricks:
    min_z = min(brick[0][2], brick[1][2])
    bricks_by_z.setdefault(min_z, set()).add(brick)

for brick in bricks_by_z.get(1):
    for x in my_range(brick[0][0], brick[1][0]):
        for y in my_range(brick[0][1], brick[1][1]):
            maximums[x][y] = ( max(brick[0][2], brick[1][2]), brick[2] )
    brick_supports[brick[2]] = set([-1])
    bricks_after_fall.append(brick)

current_z = 2
while current_z <= max(bricks_by_z.keys()):
    if not current_z in bricks_by_z:
        current_z += 1
        continue
    for brick in bricks_by_z[current_z]:
        this_max_z = 0
        for x in my_range(brick[0][0], brick[1][0]):
            for y in my_range(brick[0][1], brick[1][1]):
                this_max_z = max(this_max_z, maximums[x][y][0])
        if this_max_z < min(brick[0][2], brick[1][2]) - 1:
            fall = current_z - (this_max_z + 1)
            new_brick = ((brick[0][0], brick[0][1], brick[0][2] - fall),
                         (brick[1][0], brick[1][1], brick[1][2] - fall),
                         brick[2] )
            bricks_after_fall.append(new_brick)
            brick_supports[brick[2]] = set()
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    if maximums[x][y][0] == this_max_z:
                        brick_supports[brick[2]].add(maximums[x][y][1])
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    maximums[x][y] = ( (current_z - fall) + abs(brick[0][2] - brick[1][2]), brick[2] )
        else:
            bricks_after_fall.append(brick)
            brick_supports[brick[2]] = set()
            this_max_z = -1
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    this_max_z = max(this_max_z, maximums[x][y][0])
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    if maximums[x][y][0] == this_max_z:
                        brick_supports[brick[2]].add(maximums[x][y][1])
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    maximums[x][y] = ( max(brick[0][2], brick[1][2]), brick[2] )
    else:
        current_z += 1

count = 0
for brick in bricks:
    if not [ x for x in brick_supports if brick[2] in x and len(x) == 1 ]:
        count += 1

print("Advent of Code, Day 21, Part 1")
print(count)
