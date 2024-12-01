import pprint
import re
import sys

trees = []
lines = open('input-8', 'r').readlines()
for line in lines:
    line = line.strip()
    trees.append([ int(x) for x in line ])

width = len(trees[0])
height = len(trees)

max_score = 0
for row in range(1, height - 1):
    for column in range(1, width - 1):
        this_tree = trees[row][column]
        score_up = 0
        score_right = 0
        score_down = 0
        score_left = 0
        # from top
        for x in range(row - 1, -1, -1):
            score_up += 1
            if trees[x][column] >= this_tree:
                break
        # from bottom
        for x in range(row + 1, height):
            score_down += 1
            if trees[x][column] >= this_tree:
                break
        # from left
        for x in range(column - 1, -1, -1):
            score_left += 1
            if trees[row][x] >= this_tree:
                break
        # from right
        for x in range(column + 1, width):
            score_right += 1
            if trees[row][x] >= this_tree:
                break
        score = score_up * score_right * score_left * score_down
        if score > max_score:
            max_score = score
#        print(column, row, score, score_up, score_right, score_down, score_left)

print(max_score)
