grid = None
mins = None
paths = None
overall_min = None
count = None
skipped = None
width = None
height = None

def get_direction(pointA, pointB):
    return (pointA[0] - pointB[0]) + ( 10 * ( pointA[1] - pointB[1] ) )

def init(partA=True):
    global grid, mins, paths, overall_min, count, skipped, width, height
    grid = []
    mins = {}
    lines = open('input-sample', 'r').readlines()
    for line in lines:
        line = line.strip()
        grid.append([ int(x) for x in line ])
    width = len(grid[0])
    height = len(grid)

    for init_dir in [ -1, 1, -10, 10 ]:
        if partA:
            this_range = range(4)
        else:
            this_range = range(4, 11)
        for count in this_range:
            mins[(init_dir, count)] = []
            for y in range(height):
                mins[(init_dir, count)].append( [ ((width + height) * 9, None) for i in range(width) ] )

    overall_min = (width + height) * 9
    count = 0
    skipped = 0


if True:
    init()
    paths = [ ( grid[height-1][width-1], ( 1, get_direction((width - 1, height - 1), (width - 1, height - 2)) ), ( (width - 1, height - 1), (width - 1, height - 2)) ),
              ( grid[height-1][width-1], ( 1, get_direction((width - 1, height - 1), (width - 2, height - 1)) ), ( (width - 1, height - 1), (width - 2, height - 1)) ),
              ]

    while paths:
        count += 1
        path_tuple = paths.pop()
        score = path_tuple[0]
        direction_count = path_tuple[1][0]
        if direction_count >= 4:
            continue
        direction = path_tuple[1][1]
        path = path_tuple[2]
        current = path[-1]
        this_x = current[0]
        this_y = current[1]

        if ( this_x != 0 or this_y != 0 ):
            if score + this_x + this_y >= overall_min:
                continue
        if score < mins[(direction, direction_count)][this_y][this_x][0]:
            mins[(direction, direction_count)][this_y][this_x] = (score, path)
            if ( this_x == 0 and this_y == 0 ):
                overall_min = min([overall_min, score ])
        else:
            skipped += 1
            continue
        if path[-1] == (0, 0):
            continue
        for x, y in ( (1, 0), (0, 1), (-1, 0), (0, -1) ):
            if this_x + x < 0 or this_x + x >= width:
                continue
            if this_y + y < 0 or this_y + y >= height:
                continue
            if ( (this_x + x, this_y + y) == path[-2] ):
                # cannot "turn back"
                continue
            new_direction = get_direction( (this_x, this_y), (this_x + x, this_y + y) )
            if new_direction == direction:
                new_direction_count = direction_count + 1
                if new_direction_count >= 4:
                    continue
            else:
                new_direction_count = 1

            paths.append((( score + grid[this_y][this_x] ), (new_direction_count, new_direction), path + ((this_x + x, this_y + y),)))

    print("Advent of Code, Day 17, Part 1")
    print(min([ x[0][0][0] for x in mins.values() ]))

init(partA=False)
paths = [ ( sum([ grid[height-1][width-i] for i in range(1, 4)]), ( 4, get_direction((width - 1, height - 1), (width - 1, height - 2)) ), ( (width - 1, height - 1), (width - 1, height - 2), (width - 1, height - 3), (width - 1, height - 4)) ),
          ( sum([ grid[height-i][width-1] for i in range(1, 4)]), ( 4, get_direction((width - 1, height - 1), (width - 2, height - 1)) ), ( (width - 1, height - 1), (width - 2, height - 1), (width - 3, height - 1), (width - 4, height - 1)) ),
         ]

while paths:
    count += 1
    path_tuple = paths.pop()
    score = path_tuple[0]
    direction_count = path_tuple[1][0]
    if direction_count > 10:
        continue
    direction = path_tuple[1][1]
    path = path_tuple[2]
    current = path[-1]
    this_x = current[0]
    this_y = current[1]

    if score + this_x + this_y >= overall_min:
        skipped += 1
        continue
    if direction_count >= 4:
        if score < mins[(direction, direction_count)][this_y][this_x][0]:
            mins[(direction, direction_count)][this_y][this_x] = (score, path)
            if ( this_x == 0 and this_y == 0 ):
                overall_min = min([overall_min, score ])
        else:
            skipped += 1
            continue
    if path[-1] == (0, 0):
        continue
    for x, y in ( (1, 0), (0, 1), (-1, 0), (0, -1) ):
        if this_x + x < 0 or this_x + x >= width:
            continue
        if this_y + y < 0 or this_y + y >= height:
            continue
        if ( (this_x + x, this_y + y) == path[-2] ):
            # cannot "turn back"
            continue
        new_direction = get_direction( (this_x, this_y), (this_x + x, this_y + y) )
        if new_direction == direction:
            new_direction_count = direction_count + 1
            if new_direction_count > 10:
                continue
        else:
            if direction_count < 4:
                continue
            new_direction_count = 1

        paths.append((( score + grid[this_y][this_x] ), (new_direction_count, new_direction), path + ((this_x + x, this_y + y),)))

print("Advent of Code, Day 17, Part 2")
print(overall_min)

