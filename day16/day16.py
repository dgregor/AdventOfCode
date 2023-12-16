NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

grid = []
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    grid.append(line)
width = len(grid[0])
height = len(grid)

def get_score(start):
    lights = []
    lights.append(start)
    seen = set()
    while lights:
        light = lights.pop()
        if light in seen:
            continue
        seen.add(light)
        y = light[1][1]
        x = light[1][0]
        cell = grid[y][x]
        new_dir = None
        if cell == ".":
            if light[0] == NORTH:
                y -= 1
            elif light[0] == EAST:
                x += 1
            elif light[0] == SOUTH:
                y += 1
            elif light[0] == WEST:
                x -= 1
            new_dir = light[0]
        elif cell == "/":
            if light[0] == NORTH:
                x += 1
                new_dir = EAST
            elif light[0] == EAST:
                y -= 1
                new_dir = NORTH
            elif light[0] == SOUTH:
                x -= 1
                new_dir = WEST
            elif light[0] == WEST:
                y += 1
                new_dir = SOUTH
        elif cell == "\\":
            if light[0] == NORTH:
                x -= 1
                new_dir = WEST
            elif light[0] == EAST:
                y += 1
                new_dir = SOUTH
            elif light[0] == SOUTH:
                x += 1
                new_dir = EAST
            elif light[0] == WEST:
                y -= 1
                new_dir = NORTH
        elif cell == "|":
            if light[0] == NORTH:
                y -= 1
                new_dir = NORTH
            elif light[0] == EAST:
                if (y - 1) >= 0:
                    lights.append((NORTH, (x, y-1)))
                y += 1
                new_dir = SOUTH
            elif light[0] == SOUTH:
                y += 1
                new_dir = SOUTH
            elif light[0] == WEST:
                if (y - 1) >= 0:
                    lights.append((NORTH, (x, y-1)))
                y += 1
                new_dir = SOUTH
        elif cell == "-":
            if light[0] == NORTH:
                if (x - 1) >= 0:
                    lights.append((WEST, (x-1, y)))
                x += 1
                new_dir = EAST
            elif light[0] == EAST:
                x += 1
                new_dir = EAST
            elif light[0] == SOUTH:
                if (x - 1) >= 0:
                    lights.append((WEST, (x-1, y)))
                x += 1
                new_dir = EAST
            elif light[0] == WEST:
                x -= 1
                new_dir = WEST
        if ( x >= 0 and x < width ) and ( y >= 0 and y < height ):
            lights.append((new_dir, (x, y)))
    cells = set([ x[1] for x in seen ])
    return(len(cells))

print("Advent of Code, Day 16, Part 1")
print(get_score((EAST, (0, 0))))

print("Advent of Code, Day 16, Part 2")
max_score = 0
for start_x in range(width):
    score = get_score((SOUTH, (start_x, 0)))
    max_score = max(score, max_score)
    score = get_score((NORTH, (start_x, height-1)))
    max_score = max(score, max_score)
for start_y in range(height):
    score = get_score((EAST, (0, start_y)))
    max_score = max(score, max_score)
    score = get_score((WEST, (width - 1, start_y)))
    max_score = max(score, max_score)
print(max_score)
