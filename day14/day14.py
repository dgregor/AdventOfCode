def get_score(rocks, num_rows):
    score = 0
    for row in range(1, num_rows - 1):
        score += (num_rows - row - 1) * len( [ x for x in range(len(rocks)) if row in rocks[x] ] )
    return score

def rocks_to_tuples(rocks):
    return tuple([ tuple(rocks[x]) for x in range(len(rocks)) ])

def my_max(alist):
    if alist:
        return max(alist)
    return 0

def print_grid(rocks, stops):
    max_y = max([ max(my_max(rocks[x]), my_max(stops[x])) for x in range(len(rocks)) ])
    for y in range(max_y+1):
        print("".join([ "#" if y in stops[x] else "O" if y in rocks[x] else "." for x in range(len(rocks)) ]))
    print()

def shift_north_south(rocks, stops, north=True):
    for x in range(len(rocks)):
        if not rocks[x]:
            continue
        stop_index = len(stops[x])
        rock_index = len(rocks[x]) - 1
        prev_stop = stops[x][stop_index - 1]
        while True:
            if rock_index < 0:
                break
            stop_index -= 1
            if stop_index < 0:
                break
            current_stop = stops[x][stop_index]
            count = 0
            for y in range(rock_index, -1, -1):
                if rocks[x][y] > current_stop:
                    count += 1
                else:
                    break
            if count > 0:
                rock_index -= count
                if rock_index < 0:
                    if north:
                        rocks[x] = [ current_stop + 1 + more for more in range(count) ] + rocks[x][rock_index+count+1:]
                    else:
                        rocks[x] = [ prev_stop - 1 - more for more in range(count) ] + rocks[x][rock_index+count+1:]
                else:
                    if north:
                        rocks[x] = rocks[x][:rock_index+1] + [ current_stop + 1 + more for more in range(count) ] + rocks[x][rock_index+count+1:]
                    else:
                        rocks[x] = rocks[x][:rock_index+1] + [ prev_stop - 1 - more for more in range(count) ] + rocks[x][rock_index+count+1:]
            prev_stop = current_stop

def shift_east_west(rocks, stops, east=True):
    max_y = max([ max(my_max(rocks[x]), my_max(stops[x])) for x in range(len(rocks)) ])
    y_rocks = [ [] for x in range(max_y + 1) ]
    y_stops = [ [] for x in range(max_y + 1) ]
    for y in range(max_y + 1):
        y_rocks[y] = [ x for x in range(len(rocks)) if y in rocks[x] ]
        if not y_rocks[y]:
            continue
        y_stops[y] = [ x for x in range(len(stops)) if y in stops[x] ]
        stop_index = len(y_stops[y])
        rock_index = len(y_rocks[y]) - 1
        prev_stop = y_stops[y][stop_index - 1]
        while True:
            if rock_index < 0:
                break
            stop_index -= 1
            if stop_index < 0:
                break
            current_stop = y_stops[y][stop_index]
            count = 0
            for x in range(rock_index, -1, -1):
                if y_rocks[y][x] > current_stop:
                    count += 1
                else:
                    break
            if count > 0:
                rock_index -= count
                if rock_index < 0:
                    if not east:
                        y_rocks[y] = [ current_stop + 1 + more for more in range(count) ] + y_rocks[y][rock_index+count+1:]
                    else:
                        y_rocks[y] = [ prev_stop - 1 - more for more in range(count) ] + y_rocks[y][rock_index+count+1:]
                else:
                    if not east:
                        y_rocks[y] = y_rocks[y][:rock_index+1] + [ current_stop + 1 + more for more in range(count) ] + y_rocks[y][rock_index+count+1:]
                    else:
                        y_rocks[y] = y_rocks[y][:rock_index+1] + [ prev_stop - 1 - more for more in range(count) ] + y_rocks[y][rock_index+count+1:]
            prev_stop = current_stop
    for x in range(len(rocks)):
        rocks[x] = [ y for y in range(len(y_rocks)) if x in y_rocks[y] ]

def read_file():
    columns = []
    rows = []

    rocks = []
    stops = []

    lines = open('input', 'r').readlines()
    for line in lines:
        line = line.strip()
        rows.append(line)

    for i in range(len(rows[0])):
        columns.append([ rows[x][i] for x in range(len(rows)) ])
        rocks.append([])
        stops.append([])

    for x in range(len(columns)):
        rocks[x] = [ y + 1 for y in range(len(columns[x])) if columns[x][y] == "O" ]
        stops[x] = [ y + 1 for y in range(len(columns[x])) if columns[x][y] == "#" ]
        stops[x].insert(0, 0)
        stops[x].append(len(columns[x])+1)
    rocks.insert(0, [])
    stops.insert(0, [ y for y in range(len(columns[0]) + 2) ] )
    rocks.append([])
    stops.append([ y for y in range(len(columns[0]) + 2) ] )

    return rocks, stops

rocks, stops = read_file()
shift_north_south(rocks, stops, north=True)
print("Advent of Code, Day 14, Part 1")
print(get_score(rocks, len(stops[0])))

rocks, stops = read_file()

seen_by_rocks = {}
seen_by_number = {}
cycle_length = None
for i in range(1, 100000):
    shift_north_south(rocks, stops, north=True)
    shift_east_west(rocks, stops, east=False)
    shift_north_south(rocks, stops, north=False)
    shift_east_west(rocks, stops, east=True)
    rock_tuple = rocks_to_tuples(rocks)
    if rock_tuple in seen_by_rocks:
        cycle_length = i - seen_by_rocks[rock_tuple]
        break
    else:
        seen_by_rocks[rock_tuple] = i
        seen_by_number[i] = rock_tuple

offset = (1000000000 - i) % cycle_length

print("Advent of Code, Day 14, Part 2")
print(get_score(seen_by_number[i - cycle_length + offset], len(stops[0])))

