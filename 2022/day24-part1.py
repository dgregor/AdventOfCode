import copy
import pprint
import sys

# E/W blizzards are [row][column]
west_blizzards = []
east_blizzards = []

# N/S blizzards are [column][row]
north_blizzards = []
south_blizzards = []

start = None
end = None
whole_width = None # includes
row = 0
lines = open('input-24', 'r').readlines()
grid = []
for line in lines:
    line = line.strip()
    if row == 0:
        start = line.find(".") - 1
        whole_width = len(line)
    elif "##" in line:
        end = line.find(".") - 1
    else:
        west_blizzards.append([ 1 if line[i + 1] == "<" else 0 for i in range(len(line) - 2) ])
        east_blizzards.append([ 1 if line[i + 1] == ">" else 0 for i in range(len(line) - 2) ])
        grid.append(list(line[1:-1]))
    row += 1

height = len(east_blizzards)
width = whole_width - 2

for column in range(width):
    north_blizzards.append([ 1 if grid[i][column] == "^" else 0 for i in range(len(grid)) ])
    south_blizzards.append([ 1 if grid[i][column] == "v" else 0 for i in range(len(grid)) ])

def print_map(minutes_passed=0):
    global start
    global end
    global north_blizzards
    global south_blizzards
    global east_blizzards
    global west_blizzards

    height = len(east_blizzards)
    print("".join(["." if i == start + 1 else "#" for i in range(whole_width)]))
    for row in range(len(east_blizzards)):
        row_string = ["#"]
        for column in range(width):
            count = sum([east_blizzards[row][(column - minutes_passed) % width],
                         west_blizzards[row][(column + minutes_passed) % width],
                         north_blizzards[column][(row + minutes_passed) % height],
                         south_blizzards[column][(row - minutes_passed) % height]])
            if False and count > 1:
                row_string.append(str(count))
            elif count == 0:
                row_string.append(".")
            elif east_blizzards[row][(column - minutes_passed) % width]:
                row_string.append(">")
            elif west_blizzards[row][(column + minutes_passed) % width]:
                row_string.append("<")
            elif north_blizzards[column][(row + minutes_passed) % height]:
                row_string.append("^")
            elif south_blizzards[column][(row - minutes_passed) % height]:
                row_string.append("v")
        row_string.append("#")
        print("".join(row_string))
    print("".join(["." if i == end + 1 else "#" for i in range(whole_width)]))

def is_empty(minutes_passed, row=None, column=None):
    global north_blizzards
    global south_blizzards
    global east_blizzards
    global west_blizzards

    height = len(east_blizzards)

    if (row == -1 and column == start):
        return True

    if (row == height and column == width - 1):
        return True

    if (row < 0 or column < 0 or row >= height or column >= width):
        return False

    return sum([east_blizzards[row][(column - minutes_passed) % width],
                west_blizzards[row][(column + minutes_passed) % width],
                north_blizzards[column][(row + minutes_passed) % height],
                south_blizzards[column][(row - minutes_passed) % height]]) == 0

def min_minutes_passed(minutes_passed, row, column, leg):
    if leg == 0:
        return (minutes_passed + (width - column) + (height - row) + 1) + 2 * (height + width)
    elif leg == 1:
        return (minutes_passed + column + ( row + 1) ) + (height + width)
    else:
        return (minutes_passed + (width - column) + (height - row) + 1)

# row, column
location =(-1, start)

WAIT = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

closest = ( end - start ) + height + 1

# 0 - minutes passed
# 1 - path so far
# 2 - current location
# 3 - leg (0 == first, 1 == second, 2 == third)
to_check = {}
to_check[closest] = [((0, (), location, 0))]

seen = set()

for i in range(10):
    print("After {} minutes".format(i))
    print_map(minutes_passed=i)
    print()

best_score = None
best_path = None

count = 0

while to_check:
    count += 1
    while True:
        if len(to_check.keys()) == 0:
            print(best_score)
            print(best_path)
            sys.exit(0)
        closest = min(to_check.keys())
        if len(to_check[closest]) == 0:
            del to_check[closest]
        else:
            break
    check = to_check[closest].pop()
#    print(closest, check)
    if count % 10000 == 0:
        print(count, closest, len(to_check[closest]))
        print(check)
    minutes_passed = check[0]
    path = check[1]
    location = check[2]
    leg = check[3]
    row = location[0]
    column = location[1]


    if (leg == 2) and ( row == (height - 1) and column == end):
        if not best_score or minutes_passed < best_score:
            best_score = minutes_passed
            best_path = path
            print(best_score)
            print(best_path)
    elif (best_score is not None) and ( min_minutes_passed(minutes_passed, row, column, leg) > best_score ):
        # no way to beat the best score
        continue
    else:
        # DOWN
        if is_empty(minutes_passed=minutes_passed + 1,
                    row=row+1,
                    column=column):
            if (leg == 0) and (row == (height - 1) and column == end):
                next_leg = 1
            else:
                next_leg = leg
            next_item = (minutes_passed + 1,
                         #path + (( row + 1, column),),
                         path,
                         (row + 1, column),
                         next_leg)
            if next_item not in seen:
                distance = min_minutes_passed(minutes_passed, row + 1, column, next_leg)
                seen.add(next_item)
                to_check.setdefault(distance, []).append(next_item)
        # RIGHT
        if is_empty(minutes_passed=minutes_passed + 1,
                    row=row,
                    column=column+1):
            next_item = (minutes_passed + 1,
                         #path + ((row, column + 1),),
                         path,
                         (row, column+1),
                         leg)
            if next_item not in seen:
                distance = min_minutes_passed(minutes_passed, row, column + 1, leg)
                seen.add(next_item)
                to_check.setdefault(distance, []).append(next_item)
        # UP
        if is_empty(minutes_passed=minutes_passed + 1,
                    row=row-1,
                    column=column):
            if (leg == 1) and (row == 0 and column == start):
                next_leg = 2
            else:
                next_leg = leg
            next_item = (minutes_passed + 1,
                         #path + ((row - 1, column),),
                         path,
                         (row - 1, column),
                         next_leg)
            if next_item not in seen:
                distance = min_minutes_passed(minutes_passed, row - 1, column, next_leg)
                seen.add(next_item)
                to_check.setdefault(distance, []).append(next_item)
        # LEFT
        if is_empty(minutes_passed=minutes_passed + 1,
                    row=row,
                    column=column-1):
            next_item = (minutes_passed + 1,
                         #path + ((row, column - 1),),
                         path,
                         (row, column - 1),
                         leg)
            if next_item not in seen:
                distance = min_minutes_passed(minutes_passed, row, column - 1, leg)
                seen.add(next_item)
                to_check.setdefault(distance, []).append(next_item)
        # WAIT
        if is_empty(minutes_passed=minutes_passed + 1,
                    row=row,
                    column=column):
            next_item = (minutes_passed + 1,
                         #path + ((row, column),),
                         path,
                         (row, column),
                         leg)
            if next_item not in seen:
                distance = min_minutes_passed(minutes_passed, row, column, leg)
                to_check.setdefault(distance, []).append(next_item)
                seen.add(next_item)

