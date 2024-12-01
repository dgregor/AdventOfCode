# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def print_seen(width, height, seen, outside):
    for y in range(height):
        line = "".join([ "X" if (x, y) in seen else "!" if (x, y) in outside else " " for x in range(width) ])
        print(line)

def traverse(grid, current_x, current_y, heading, seen, outside):
    if current_x < 0 or current_y < 0:
        return False
    if current_x > len(grid[0]) or current_y > len(grid):
        return False
    if (current_x, current_y) in seen:
        return True
    seen.add((current_x, current_y))
    if grid[current_y][current_x] == "S":
        if heading == NORTH:
            return (current_x, current_y-1, NORTH)
        if heading == EAST:
            return (current_x+1, current_y, EAST)
        if heading == SOUTH:
            return (current_x, current_y+1, SOUTH)
        else:
            return (current_x-1, current_y, WEST)
    elif grid[current_y][current_x] == "|":
        if heading == NORTH:
            outside.add((current_x-1, current_y))
            return (current_x, current_y-1, NORTH)
        elif heading == SOUTH:
            outside.add((current_x+1, current_y))
            return (current_x, current_y+1, SOUTH)
        else:
            return False
    elif grid[current_y][current_x] == "-":
        if heading == EAST:
            outside.add((current_x, current_y-1))
            return (current_x+1, current_y, EAST)
        elif heading == WEST:
            outside.add((current_x, current_y+1))
            return (current_x-1, current_y, WEST)
        else:
            return False
    elif grid[current_y][current_x] == "L":
        if heading == SOUTH:
            outside.add((current_x+1, current_y-1))
            return (current_x+1, current_y, EAST)
        elif heading == WEST:
            outside.add((current_x, current_y+1))
            outside.add((current_x-1, current_y))
            outside.add((current_x-1, current_y+1))
            return (current_x, current_y-1, NORTH)
        else:
            return False
    elif grid[current_y][current_x] == "J":
        if heading == SOUTH:
            outside.add((current_x+1, current_y))
            outside.add((current_x+1, current_y+1))
            outside.add((current_x, current_y+1))
            return (current_x-1, current_y, WEST)
        elif heading == EAST:
            outside.add((current_x-1, current_y-1))
            return (current_x, current_y-1, NORTH)
        else:
            return False
    elif grid[current_y][current_x] == "7":
        if heading == NORTH:
            outside.add((current_x-1, current_y+1))
            return (current_x-1, current_y, WEST)
        elif heading == EAST:
            outside.add((current_x, current_y-1))
            outside.add((current_x+1, current_y-1))
            outside.add((current_x+1, current_y))
            return (current_x, current_y+1, SOUTH)
        else:
            return False
    elif grid[current_y][current_x] == "F":
        if heading == NORTH:
            outside.add((current_x-1, current_y))
            outside.add((current_x-1, current_y-1))
            outside.add((current_x, current_y-1))
            return (current_x+1, current_y, EAST)
        elif heading == WEST:
            outside.add((current_x+1, current_y+1))
            return (current_x, current_y+1, SOUTH)
        else:
            return False
    return False

grid = []
start = None
count = 0

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    this_row = list(line)
    grid.append(this_row)
    if 'S' in this_row:
        start = (line.index("S"), count)
    count += 1

for direction in (NORTH, EAST, SOUTH, WEST):
    x = start[0]
    y = start[1]
    new_direction = direction
    seen = set()
    outside = set()
    complete = False
    while True:
        rv = traverse(grid, x, y, new_direction, seen, outside)
        if rv is True:
            complete = True
            break
        elif rv == False:
            break
        else:
            (x, y, new_direction) = rv
    if complete:
        print("Advent of Code, Day 10, Part 1")
        if len(seen) % 2 == 0:
            print(int(len(seen) / 2))
        else:
            print(int(len(seen) // 2))

        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if (x, y) in seen:
                    break
                outside.add((x, y))
            for y in range(len(grid), -1, -1):
                if (x, y) in seen:
                    break
                outside.add((x, y))
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in seen:
                    break
                outside.add((x, y))
            for x in range(len(grid[0]), -1, -1):
                if (x, y) in seen:
                    break
                outside.add((x, y))
        count_inside = 0
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if not ( (x, y) in seen or (x, y) in outside ):
                    count_inside += 1
        print("Advent of Code, Day 10, Part 2")
        print(count_inside)
        break
