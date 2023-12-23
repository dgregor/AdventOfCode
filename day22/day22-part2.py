bricks = []
bricks_after_fall = {}

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
    bricks_after_fall[brick[2]] = brick

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
            bricks_after_fall[new_brick[2]] = new_brick
            brick_supports[brick[2]] = set()
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    if maximums[x][y][0] == this_max_z:
                        brick_supports[brick[2]].add(maximums[x][y][1])
            for x in my_range(brick[0][0], brick[1][0]):
                for y in my_range(brick[0][1], brick[1][1]):
                    maximums[x][y] = ( (current_z - fall) + abs(brick[0][2] - brick[1][2]), brick[2] )
        else:
            bricks_after_fall[brick[2]] = brick
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

bricks_after_fall_by_z = {}
for brick in bricks_after_fall.values():
    min_z = min(brick[0][2], brick[1][2])
    bricks_after_fall_by_z.setdefault(min_z, set()).add(brick)

brick_supports_by_support = {}

brick_supports_by_z = {}
for index in range(len(brick_supports)):
    support_set = brick_supports[index]
    support_set_height = None
    for e in support_set:
        if e != -1:
            support_set_height = max(bricks_after_fall[e][0][2], bricks_after_fall[e][1][2])
        break
    if support_set_height is not None:
        f = frozenset(support_set)
        brick_supports_by_z.setdefault(support_set_height, set())
        brick_supports_by_z[support_set_height].add(f)
        brick_supports_by_support.setdefault(f, set())
        brick_supports_by_support[f].add(index)

total = 0
for brick in range(len(bricks_after_fall)):
    fallen = set([brick])
    height = max(bricks_after_fall[brick][0][2], bricks_after_fall[brick][1][2])
    if height not in brick_supports_by_z.keys():
        continue
    to_check = set([height])
    while to_check:
        this_height = min(to_check)
        to_check.discard(this_height)
        for set_at_this_height in brick_supports_by_z.get(this_height, []):
            if set_at_this_height.issubset(fallen):
                # whatever is supported by this combo will fall
                for falling_brick in brick_supports_by_support[set_at_this_height]:
                    fallen.add(falling_brick)
                    falling_brick_height = max(bricks_after_fall[falling_brick][0][2], bricks_after_fall[falling_brick][1][2])
                    to_check.add(falling_brick_height)
    fallen.discard(brick)
    total += len(fallen)

print("Advent of Code, Day 21, Part 2")
print(total)
