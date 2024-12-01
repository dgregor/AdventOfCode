import copy
import pprint
import sys

OPEN = "."
WALL = "#"
EMPTY = " "

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

cube_width = 50
mappings = {}

# mapping is (row, column, direction) -> (row, column, direction)

# face 1
for column in range(50, 100):
    # face 1 facing up
    mappings[(0, column, UP)] = (100 + column, 0, RIGHT)
#    # face 1 facing down
#    mappings[(49, column, DOWN)] = (50, column, DOWN)
for row in range(0, 50):
    # face 1 facing left
    mappings[(row, 50, LEFT)] = (149 - row, 0, RIGHT)
#    # face 1 facing right
#    mappings[(row, 99, RIGHT)] = (row, 100, RIGHT)

# face 2
for column in range(100, 150):
    # face 2 facing up
    mappings[(0, column, UP)] = (199, column - 100, UP)
    # face 2 facing down
    mappings[(49, column, DOWN)] = (column - 50, 99, LEFT)
for row in range(0, 50):
#    # face 2 facing left
#    mappings[(row, 50, LEFT)] = (199, 49 - row, UP)
    # face 2 facing right
    mappings[(row, 149, RIGHT)] = (149 - row, 99, LEFT)

# face 3
#for column in range(50, 100):
#    # face 3 facing up
#    mappings[(0, column, UP)] = (299 - column, 99, LEFT)
#    # face 3 facing down
#    mappings[(49, column, DOWN)] = (column - 50, 99, LEFT)
for row in range(50, 100):
    # face 3 facing left
    mappings[(row, 50, LEFT)] = (100, row - 50, DOWN)
    # face 3 facing right
    mappings[(row, 99, RIGHT)] = (49, row + 50, UP)

# face 4
for column in range(50, 100):
#    # face 4 facing up
#    mappings[(0, column, UP)] = (299 - column, 99, LEFT)
    # face 4 facing down
    mappings[(149, column, DOWN)] = (column + 100, 49, LEFT)
for row in range(100, 150):
#    # face 4 facing left
#    mappings[(row, 50, LEFT)] = (150, row - 100, DOWN)
    # face 4 facing right
    mappings[(row, 99, RIGHT)] = (149 - row, 149, LEFT)

# face 5
for column in range(0, 50):
    # face 5 facing up
    mappings[(100, column, UP)] = (column + 50, 50, RIGHT)
#    # face 5 facing down
#    mappings[(199, column, DOWN)] = (0, column, DOWN)
for row in range(100, 150):
    # face 5 facing left
    mappings[(row, 0, LEFT)] = (149 - row, 50, RIGHT)
#    # face 5 facing right
#    mappings[(row, 99, RIGHT)] = (0, 199 - row, DOWN)

# face 6
for column in range(0, 50):
#    # face 6 facing up
#    mappings[(150, column, UP)] = (column + 100, 50, RIGHT)
    # face 6 facing down
    mappings[(199, column, DOWN)] = (0, column + 100, DOWN)
for row in range(150, 200):
    # face 6 facing left
    mappings[(row, 0, LEFT)] = (0, row - 100, DOWN)
    # face 6 facing right
    mappings[(row, 49, RIGHT)] = (149, row - 100, UP)

pprint.pprint(mappings)

def print_grid(grid):
    for row in grid:
        print("".join(row))

grid = []
directions = []
fill_in_grid = True
lines = open('input-22', 'r').readlines()
for line in lines:
    if line.strip() == "":
        fill_in_grid = False
    elif fill_in_grid:
        grid.append(list(line.strip("\n")))
    else:
        number = ""
        for character in list(line.strip("\n")):
            if character in ("R", "L"):
                directions.append((int(number), character))
                number = ""
            else:
                number += character
        if number:
            directions.append((int(number), "STOP"))

max_grid_width = max(len(x) for x in grid)
for row in grid:
    for i in range(len(row), max_grid_width):
        row.append(EMPTY)

#print_grid(grid)
traversed = copy.deepcopy(grid)

beginning_of_row = []
end_of_row = []
for row in grid:
    seen_beginning = False
    seen_end = False
    for i in range(max_grid_width):
        if row[i] in (OPEN, WALL) and not seen_beginning:
            beginning_of_row.append(i)
            seen_beginning = True
        elif row[i] == EMPTY and seen_beginning and not seen_end:
            end_of_row.append(i-1)
            seen_end = True
        elif not seen_end and i == max_grid_width - 1:
            end_of_row.append(i)
beginning_of_column = []
end_of_column = []
for column in range(max_grid_width):
    seen_beginning = False
    seen_end = False
    for row in range(len(grid)):
        if grid[row][column] in (OPEN, WALL) and not seen_beginning:
            beginning_of_column.append(row)
            seen_beginning = True
        elif grid[row][column] == EMPTY and seen_beginning and not seen_end:
            end_of_column.append(row-1)
            seen_end = True
        elif not seen_end and row == len(grid) - 1:
            end_of_column.append(row)

location = (0, beginning_of_row[0])
facing = RIGHT

traversed[0][beginning_of_row[0]] = ">"

count = 0
for direction in directions:
    count += 1
    print(direction)
    for i in range(direction[0]):
        row = location[0]
        column = location[1]
        print("At", row, column, "facing", facing)
        flip = False
        new_row = row
        new_column = column
        new_facing = facing
        if (row, column, facing) in mappings:
            new_row, new_column, new_facing = mappings[(row, column, facing)]
            flip = True
        if facing == RIGHT:
            traversed[row][column] = ">"
            if not flip:
                new_column = column + 1
        elif facing == DOWN:
            traversed[row][column] = "v"
            if not flip:
                new_row = row + 1
        elif facing == LEFT:
            traversed[row][column] = "<"
            if not flip:
                new_column = column - 1
        elif facing == UP:
            traversed[row][column] = "^"
            if not flip:
                new_row = row - 1
        if grid[new_row][new_column] == OPEN:
            location = (new_row, new_column)
            facing = new_facing
        elif grid[new_row][new_column] == WALL:
            break
        else:
            print("OOPS", new_row, new_column)
            sys.exit(1)
    if direction[1] == "STOP":
        pass
    elif direction[1] == "R":
        facing = (facing + 1) % 4
    else:
        facing = 3 if facing == 0 else facing - 1
    if count == 10:
        pass
        #break


#print_grid(grid)
print_grid(traversed)
print(location)
print( ( 1000 * (location[0] + 1) ) + ( 4 * ( location[1] + 1 ) ) + facing )
