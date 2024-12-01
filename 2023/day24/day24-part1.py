from pprint import pprint

points = []

if False:
    box_start = 7
    box_end = 27
    filename = "input-sample"
else:
    box_start = 200000000000000
    box_end = 400000000000000
    filename = "input"

lines = open(filename, 'r').readlines()
for line in lines:
    line = line.strip()
    location = line.split(" @ ")[0]
    velocity = line.split(" @ ")[1]

    points.append([ [ int(x.strip()) for x in location.split(", ") ],
                    [ int(x.strip()) for x in velocity.split(", ") ]
                   ])

matches = []
for first in range(len(points) - 1):
    for second in range(first+1, len(points)):
        # intersecting_x = ((y2i - yi)(xv*x2v)+(x2v*xi*yv)-(xv*x2i*y2v))/((x2v*yv)-(xv*y2v))
        xi = points[first][0][0]
        yi = points[first][0][1]
        xv = points[first][1][0]
        yv = points[first][1][1]
        x2i = points[second][0][0]
        y2i = points[second][0][1]
        x2v = points[second][1][0]
        y2v = points[second][1][1]

        if ( x2v * yv ) == (xv * y2v):
            # lines are parallel
            continue
        intersecting_x = ( ( (y2i - yi) * (xv * x2v) ) + (x2v * xi * yv) - (xv * x2i * y2v) ) / ( (x2v * yv) - ( xv *y2v ) )
        time_of_intersection_first = ( intersecting_x - xi ) / xv
        time_of_intersection_second = ( intersecting_x - x2i ) / x2v
        if ( time_of_intersection_first < 0 ) or ( time_of_intersection_second < 0 ):
            continue
        intersecting_y = yi + (time_of_intersection_first * yv)
        if ( intersecting_x >= box_start and intersecting_x <= box_end ) and (intersecting_y >= box_start and intersecting_y <= box_end):
            matches.append((first, second))

print("Advent of Code, Day 24, Part 1")
print(len(matches))
