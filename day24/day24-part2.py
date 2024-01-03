import math
import sys
from pprint import pprint

points = []

filename = "input"

def get_for_dimension(dimension):
    points_by_velocity = {}
    lines = open(filename, 'r').readlines()
    for line in lines:
        line = line.strip()
        location = line.split(" @ ")[0]
        velocity = line.split(" @ ")[1]
        point = [ [ int(x.strip()) for x in location.split(", ") ],
                  [ int(x.strip()) for x in velocity.split(", ") ]
                 ]
        points.append(point)
        points_by_velocity.setdefault(point[1][dimension], []).append(point)
    matches = {}
    all_matches = None
    for velocity, velocity_points in sorted(points_by_velocity.items()):
        if len(velocity_points) > 1:
            matches = None
            for first in range(len(velocity_points) - 1):
                for second in range(first + 1, len(velocity_points)):
                    these_matches = set()
                    diff = velocity_points[first][0][dimension] - velocity_points[second][0][dimension]
                    for i in range(1, round(abs(diff)**.5)):
                        if diff % i == 0:
                            these_matches.add(i)
                if matches is None:
                    matches = these_matches
                else:
                    matches = matches.intersection(these_matches)
            if all_matches is None:
                all_matches = set([ x + velocity for x in matches ]) | set([ velocity - x for x in matches ])
            else:
                all_matches = all_matches.intersection(set([ x + velocity for x in matches ]) | set([ velocity - x for x in matches ]))
            if len(all_matches) == 1:
                hail_velocity = all_matches.pop()
                break
    starting_point_index = [ i for i in range(len(points)) if points[i][1][dimension] == hail_velocity ][0]
    starting_dimension = points[starting_point_index][0][dimension]
    points_by_time = {}
    for point in points:
        if hail_velocity != point[1][dimension]:
            points_by_time[(point[0][dimension] - starting_dimension) // (hail_velocity - point[1][dimension])] = point
    timings = sorted(points_by_time.keys())
    return points[starting_point_index][0][dimension]

total = 0
for dimension in (0, 1, 2):
    total += get_for_dimension(dimension)

print("Advent of Code, Day 24, Part 1")
print(total)

