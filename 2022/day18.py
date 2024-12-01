import pprint
import sys


cubes = []
lines = open('input-18', 'r').readlines()
for line in lines:
    line = line.strip()
    cubes.append({ "x": int(line.split(",")[0]),
                   "y": int(line.split(",")[1]),
                   "z": int(line.split(",")[2]),
                   })

min_x = 100000
min_y = 100000
min_z = 100000
max_x = 0
max_y = 0
max_z = 0
for cube in cubes:
#    min_x = min(min_x, cube["x"])
#    min_y = min(min_y, cube["y"])
#    min_z = min(min_z, cube["z"])
    max_x = max(max_x, cube["x"])
    max_y = max(max_y, cube["y"])
    max_z = max(max_z, cube["z"])

min_x = 0
min_y = 0
min_z = 0

print(min_x, min_y, min_z, max_x, max_y, max_z)
x_range = range(min_x, max_x + 1)
y_range = range(min_y, max_y + 1)
z_range = range(min_z, max_z + 1)

AIR = 1
ROCK = 2
STEAM = 3

print(len(x_range))
space = [[[AIR] * len(z_range) for i in y_range ] for j in x_range]
for cube in cubes:
    print(cube, len(space), len(space[cube["x"]]), len(space[cube["x"]][cube["y"]]))
    space[cube["x"]][cube["y"]][cube["z"]] = ROCK

to_check = set()

# Steam from "front"
y = min_y
for x in x_range:
    for z in z_range:
        to_check.add((x, y, z))
# Steam from "back"
y = max_y
for x in x_range:
    for z in z_range:
        to_check.add((x, y, z))
# Steam from "left"
x = min_x
for y in y_range:
    for z in z_range:
        to_check.add((x, y, z))
# Steam from "right"
x = max_x
for y in y_range:
    for z in z_range:
        to_check.add((x, y, z))
# Steam from "bottom"
z = min_x
for x in x_range:
    for y in y_range:
        to_check.add((x, y, z))
# Steam from "top"
z = max_z
for x in x_range:
    for y in y_range:
        to_check.add((x, y, z))

while to_check:
    cell = to_check.pop()
    x = cell[0]
    y = cell[1]
    z = cell[2]
    if space[x][y][z] == AIR:
        space[x][y][z] = STEAM
        # "left"
        if x > min_x:
            to_check.add((x-1, y, z))
        # "right"
        if x < max_x:
            to_check.add((x+1, y, z))
        # "front"
        if y > min_y:
            to_check.add((x, y-1, z))
        # "back"
        if y < max_y:
            to_check.add((x, y+1, z))
        # "down"
        if z > min_z:
            to_check.add((x, y, z-1))
        # "up"
        if z < max_z:
            to_check.add((x, y, z+1))

#for y in y_range:
#    print(y)
#    for z in z_range:
#        print("".join([ str(space[x][y][z]) for x in x_range ]))

surface_area = 0
for x in x_range:
    for y in y_range:
        for z in z_range:
            if not space[x][y][z] == ROCK:
                continue
            # left
            if x == min_x or space[x-1][y][z] == STEAM:
                surface_area += 1
            # right
            if x == max_x or space[x+1][y][z] == STEAM:
                surface_area += 1
            # back
            if y == max_y or space[x][y+1][z] == STEAM:
                surface_area += 1
            # front
            if y == min_y or space[x][y-1][z] == STEAM:
                surface_area += 1
            # top
            if z == max_z or space[x][y][z+1] == STEAM:
                surface_area += 1
            # bottom
            if z == min_z or space[x][y][z-1] == STEAM:
                surface_area += 1
print(surface_area)


#surface_area = 0
#for cube in cubes:
#    # "left"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] - 1 and other_cube["y"] == cube["y"] and other_cube["z"] == cube["z"] ]:
#        surface_area += 1
#
#    # "right"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] + 1 and other_cube["y"] == cube["y"] and other_cube["z"] == cube["z"] ]:
#        surface_area += 1
#
#    # "back"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] and other_cube["y"] == cube["y"] + 1 and other_cube["z"] == cube["z"] ]:
#        surface_area += 1
#
#    # "front"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] and other_cube["y"] == cube["y"] - 1 and other_cube["z"] == cube["z"] ]:
#        surface_area += 1
#
#    # "top"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] and other_cube["y"] == cube["y"] and other_cube["z"] == cube["z"] + 1]:
#        surface_area += 1
#
#    # "bottom"
#    if not [ other_cube for other_cube in cubes if other_cube["x"] == cube["x"] and other_cube["y"] == cube["y"] and other_cube["z"] == cube["z"] - 1]:
#        surface_area += 1
#
#print(surface_area)
