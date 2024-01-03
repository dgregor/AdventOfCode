current_coords = (0, 0)
dug_coords = [(0, 0)]

lines = open("input", 'r').readlines()
for line in lines:
    line = line.strip()
    direction, count, color = line.split()
    count = int(count)
    if direction == "U":
        new_coords = (current_coords[0], current_coords[1]+count)
    elif direction == "D":
        new_coords = (current_coords[0], current_coords[1]-count)
    elif direction == "R":
        new_coords = (current_coords[0]+count, current_coords[1])
    else:
        new_coords = (current_coords[0]-count, current_coords[1])
    dug_coords.append(new_coords)
    current_coords = new_coords

min_x = min([ coord[0] for coord in dug_coords ])
min_y = min([ coord[1] for coord in dug_coords ])
max_x = max([ coord[0] for coord in dug_coords ])
max_y = max([ coord[1] for coord in dug_coords ])

width = (max_x - min_x) + 1
height = (max_y - min_y) + 1

grid = []
for row in range(height):
    grid.append( [ False for x in range(width) ] )
grid[-min_y][-min_x] = True

current_coords = (0, 0)
dug_coords = [(0, 0)]

lines = open("input", 'r').readlines()
for line in lines:
    line = line.strip()
    direction, count, color = line.split()
    count = int(count)
    if direction == "U":
        new_coords = (current_coords[0], current_coords[1]+count)
        for j in range(1, count + 1):
            grid[current_coords[1]+j - min_y][current_coords[0] - min_x] = True
    elif direction == "D":
        new_coords = (current_coords[0], current_coords[1]-count)
        for j in range(1, count + 1):
            grid[current_coords[1]-j - min_y][current_coords[0] - min_x] = True
    elif direction == "R":
        new_coords = (current_coords[0]+count, current_coords[1])
        for j in range(1, count + 1):
            grid[current_coords[1] - min_y][current_coords[0] + j - min_x] = True
    else:
        new_coords = (current_coords[0]-count, current_coords[1])
        for j in range(1, count + 1):
            grid[current_coords[1] - min_y][current_coords[0] - j - min_x] = True
    dug_coords.append((current_coords, new_coords))
    current_coords = new_coords

colored = []
for row in range(height):
    colored.append( [ None for x in range(width) ] )

to_check = []
area = 0
for y in range(height):
    to_check.append((0, y))
    to_check.append((width-1, y))
for x in range(width):
    to_check.append((x, 0))
    to_check.append((x, height-1))

while to_check:
    cell_x, cell_y = to_check.pop()
    if colored[cell_y][cell_x] is not None:
        continue
    if grid[cell_y][cell_x]:
        colored[cell_y][cell_x] = False
        continue
    colored[cell_y][cell_x] = True
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if abs(x) + abs(y) >= 2:
                continue
            if (x == 0 and y == 0):
                continue
            if cell_x + x < 0 or cell_x + x >= width:
                continue
            if cell_y + y < 0 or cell_y + y >= height:
                continue
            if grid[cell_y + y][cell_x + x]:
                continue
            to_check.append((cell_x + x, cell_y + y))

area = (width * height) - sum([ len( [ x for x in range(width) if colored[y][x] ] ) for y in range(height) ])
print("Advent of Code, Day 18, Part 1")
print(area)
