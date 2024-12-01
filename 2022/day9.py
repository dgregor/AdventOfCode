import pprint
import re
import sys

visited = { (0,0): 1 }
knots = [(0,0)] * 10

def print_grid():
    global knots
    min_x = min([ knot[0] for knot in knots ])
    max_x = max([ knot[0] for knot in knots ])
    min_y = min([ knot[1] for knot in knots ])
    max_y = max([ knot[1] for knot in knots ])
    width = 1 + (max_x - min_x)
    height = 1 + (max_y - min_y)
    grid = [ ["x"] * width for i in range(height) ]
    for knot in range(9, -1, -1):
#        print(knot, knots[knot], min_x, max_x, min_y, max_y, width, height)
        grid[max_y - knots[knot][1]][knots[knot][0] - min_x] = str(knot)
#        print(grid)
    for row in range(0, height):
        print("".join(grid[row]))

def move(knot_number):
    global knots
    global visited
    head_x = knots[knot_number][0]
    head_y = knots[knot_number][1]
    tail_x = knots[knot_number+1][0]
    tail_y = knots[knot_number+1][1]
    if head_y == tail_y:
        if abs(head_x - tail_x) <= 1:
            return
        if head_x > tail_x:
            assert tail_x == head_x - 2
            tail_x = head_x - 1
        else:
            assert tail_x == head_x + 2
            tail_x = head_x + 1
    elif head_x == tail_x:
        if abs(head_y - tail_y) <= 1:
            return
        if head_y > tail_y:
            assert tail_y == head_y - 2
            tail_y = head_y - 1
        else:
            assert tail_y == head_y + 2
            tail_y = head_y + 1
    else:
        if abs(head_x - tail_x) == 1 and abs(head_y - tail_y) == 1:
            return
        if abs(head_y - tail_y) == 2 and abs(head_x - tail_x) == 2:
            tail_x += (head_x - tail_x) // 2
            tail_y += (head_y - tail_y) // 2
        elif abs(head_y - tail_y) == 2:
            tail_x = head_x
            tail_y += (head_y - tail_y) // 2
        elif abs(head_x - tail_x) == 2:
            tail_y = head_y
            tail_x += (head_x - tail_x) // 2
    knots[knot_number+1] = (tail_x, tail_y)
    if knot_number == 8:
        print("visited", (tail_x, tail_y))
        visited[(tail_x, tail_y)] = 1

lines = open('input-9', 'r').readlines()
for line in lines:
    line = line.strip()
    direction, distance = line.split()
    distance = int(distance)
    print(line)
    if direction == 'R':
        for i in range(distance):
            knots[0] = (knots[0][0] + 1, knots[0][1])
            for j in range(0, 9):
                move(j)
#                print_grid()
    elif direction == 'D':
        for i in range(distance):
            knots[0] = (knots[0][0], knots[0][1] - 1)
            for j in range(0, 9):
                move(j)
#                print_grid()
    elif direction == 'L':
        for i in range(distance):
            knots[0] = (knots[0][0] - 1, knots[0][1])
            for j in range(0, 9):
                move(j)
#                print_grid()
    elif direction == 'U':
        for i in range(distance):
            knots[0] = (knots[0][0], knots[0][1] + 1)
            for j in range(0, 9):
                move(j)
#                print_grid()
    print(knots)

print(len(visited.keys()))
