import pprint
import sys


#lines = open('input-17', 'r').readlines()
#for line in lines:
#    line = line.strip()

#air = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
air = open('input-17', 'r').readlines()[0].strip()

air_index = -1

chamber = [ [False] * 7 for x in range(100000) ]
max_height = -1

def print_chamber(first_row=None, num_rows=-1, coords=None):
    if coords:
        return
    global chamber
    global max_height
    if not first_row:
        first_row = max_height + 7
    if num_rows < 0:
        num_rows = 7
    for index in range(first_row, first_row - num_rows, -1):
        this_row = [ x if x else "." for x in chamber[index] ]
        if coords:
            for coord in coords:
                if coord[1] == index:
                    this_row[coord[0]] = "@"
        if this_row == ".......":
            continue
        print(str(index).rjust(5) + " " + "".join(this_row))
    print()


foo = 0
for rock_num in range(10092):

    height = max_height + 4
    if height > len(chamber) - 4:
        for i in range(1000):
            chamber.append([False] * 7)
    if rock_num % 5 == 0:
        left_side = 2
        right_side = 5
        falling = True
        while falling:
            air_index = (air_index + 1) % len(air)
            if air_index % len(air) == 0:
                print(rock_num, "".join([ x if x else "." for x in chamber[max_height] ]))
            print_chamber(coords=[(left_side, height),
                                  (left_side + 1, height),
                                  (left_side + 2, height),
                                  (left_side + 3, height)])
            if air[air_index] == ">":
                if right_side < 6 and not chamber[height][right_side + 1]:
                    right_side += 1
                    left_side += 1
            elif air[air_index] == "<":
                if left_side > 0 and not chamber[height][left_side - 1]:
                    right_side -= 1
                    left_side -= 1
            if height == 0:
                falling = False
            elif ( chamber[height-1][left_side] or
                   chamber[height-1][left_side+1] or
                   chamber[height-1][left_side+2] or
                   chamber[height-1][left_side+3] ):
                falling = False
            if not falling:
                for i in range(left_side, right_side + 1):
                    chamber[height][i] = "A"
                max_height = max(max_height, height)
            height -= 1
    if rock_num % 5 == 1:
        left_side = 2
        right_side = 4
        falling = True
        while falling:
            air_index = (air_index + 1) % len(air)
            if air_index % len(air) == 0:
                print(rock_num, "".join([ x if x else "." for x in chamber[max_height] ]))
            print_chamber(coords=[(left_side + 1, height),
                                  (left_side, height + 1),
                                  (left_side + 1, height + 1),
                                  (left_side + 2, height + 1),
                                  (left_side + 1, height + 2)])
            if air[air_index] == ">":
                if right_side < 6:
                    if not ( chamber[height][right_side] or
                             chamber[height+1][right_side+1] or
                             chamber[height+2][right_side] ):
                        right_side += 1
                        left_side += 1
            elif air[air_index] == "<":
                if left_side > 0:
                    if not ( chamber[height][left_side] or
                             chamber[height+1][left_side-1] or
                             chamber[height+2][left_side] ):
                        right_side -= 1
                        left_side -= 1
            if height == 0:
                falling = False
            elif ( chamber[height-1][left_side + 1] or
                   chamber[height][left_side] or
                   chamber[height][left_side + 2] ):
                falling = False
            if not falling:
                chamber[height][left_side + 1] = "B"
                chamber[height+1][left_side] = "B"
                chamber[height+1][left_side + 1] = "B"
                chamber[height+1][left_side + 2] = "B"
                chamber[height+2][left_side + 1] = "B"
                max_height = max(max_height, height + 2)
            height -= 1
    if rock_num % 5 == 2:
        left_side = 2
        right_side = 4
        falling = True
        while falling:
            air_index = (air_index + 1) % len(air)
            if air_index % len(air) == 0:
                print(rock_num, max_height)
#                print_chamber(num_rows=20)
            print_chamber(coords=[(left_side, height),
                                  (left_side + 1, height),
                                  (left_side + 2, height),
                                  (left_side + 2, height + 1),
                                  (left_side + 2, height + 2)])
            if air[air_index] == ">":
                if right_side < 6:
                    if not ( chamber[height][right_side+1] or
                             chamber[height+1][right_side+1] or
                             chamber[height+2][right_side+1] ):
                        right_side += 1
                        left_side += 1
            elif air[air_index] == "<":
                if left_side > 0:
                    if not ( chamber[height][left_side-1] or
                             chamber[height+1][left_side+1] or
                             chamber[height+2][left_side+1] ):
                        right_side -= 1
                        left_side -= 1
            if height == 0:
                falling = False
            elif ( chamber[height-1][left_side] or
                   chamber[height-1][left_side+1] or
                   chamber[height-1][left_side+2] ):
                falling = False
            if not falling:
                chamber[height][left_side] = "C"
                chamber[height][left_side + 1] = "C"
                chamber[height][left_side + 2] = "C"
                chamber[height+1][left_side + 2] = "C"
                chamber[height+2][left_side + 2] = "C"
                max_height = max(max_height, height + 2)
            height -= 1
    if rock_num % 5 == 3:
        left_side = 2
        right_side = 2
        falling = True
        while falling:
            air_index = (air_index + 1) % len(air)
            if air_index % len(air) == 0:
                print(rock_num, "".join([ x if x else "." for x in chamber[max_height] ]))
            print_chamber(coords=[(left_side, height),
                                  (left_side, height + 1),
                                  (left_side, height + 2),
                                  (left_side, height + 3)])
            if air[air_index] == ">":
                if right_side < 6:
                    if not ( chamber[height][right_side+1] or
                             chamber[height+1][right_side+1] or
                             chamber[height+2][right_side+1] or
                             chamber[height+3][right_side+1] ):
                        right_side += 1
                        left_side += 1
            elif air[air_index] == "<":
                if left_side > 0:
                    if not ( chamber[height][left_side-1] or
                             chamber[height+1][left_side-1] or
                             chamber[height+2][left_side-1] or
                             chamber[height+3][left_side-1] ):
                        right_side -= 1
                        left_side -= 1
            if height == 0:
                falling = False
            elif ( chamber[height-1][left_side] ):
                falling = False
            if not falling:
                chamber[height][left_side] = "D"
                chamber[height+1][left_side] = "D"
                chamber[height+2][left_side] = "D"
                chamber[height+3][left_side] = "D"
                max_height = max(max_height, height + 3)
            height -= 1
    if rock_num % 5 == 4:
        left_side = 2
        right_side = 3
        falling = True
        while falling:
            air_index = (air_index + 1) % len(air)
            if air_index % len(air) == 0:
                print(rock_num, "".join([ x if x else "." for x in chamber[max_height] ]))
            print_chamber(coords=[(left_side, height),
                                  (left_side, height + 1),
                                  (left_side + 1, height),
                                  (left_side + 1, height + 1)])
            if air[air_index] == ">":
                if right_side < 6:
                    if not ( chamber[height][right_side+1] or
                             chamber[height+1][right_side+1] ):
                        right_side += 1
                        left_side += 1
            elif air[air_index] == "<":
                if left_side > 0:
                    if not ( chamber[height][left_side-1] or
                             chamber[height+1][left_side-1] ):
                        right_side -= 1
                        left_side -= 1
            if height == 0:
                falling = False
            elif ( chamber[height-1][left_side] or
                  chamber[height-1][right_side]):
                falling = False
            if not falling:
                chamber[height][left_side] = "E"
                chamber[height+1][left_side] = "E"
                chamber[height][right_side] = "E"
                chamber[height+1][right_side] = "E"
                max_height = max(max_height, height + 1)
            height -= 1

    rock_count = rock_num + 1

    if (rock_count - 1722) % 1725 == 1604:
        print("xx", rock_count, max_height, max_height - foo)
    if (rock_count - 1722) % 1725 == 0:
        print("yy", rock_count, max_height, max_height - foo)
        foo = max_height


