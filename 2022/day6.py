import re
import sys

lines = open('input-6', 'r').readlines()
for line in lines:
    last_four = [""] * 14
    count = 0
    characters = line.strip()
    while ("" in last_four) or (len(set(last_four)) < 14):
        next_char = characters[count:count+1]
        last_four.pop()
        last_four.insert(0, next_char)
        count += 1
    print(count, last_four)
