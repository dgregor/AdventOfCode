import pprint
import re

total = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    winning = set([ int(x) for x in line.split(":")[1].split("|")[0].split() ])
    mine = set([ int(x) for x in line.split(":")[1].split("|")[1].split() ])
    count = len(winning & mine)
    if count > 0:
        total += 2**(count-1)

print("Advent of Code, Day 4, Part 1")
print(total)

cards = {}
lines = open('input', 'r').readlines()
current = 0
for line in lines:
    current += 1
    cards.setdefault(current, 0)
    cards[current] += 1
    line = line.strip()
    winning = set([ int(x) for x in line.split(":")[1].split("|")[0].split() ])
    mine = set([ int(x) for x in line.split(":")[1].split("|")[1].split() ])
    count = len(winning & mine)
    for j in range(1, count+1):
        cards.setdefault(current+j, 0)
        cards[current+j] += cards[current]

print("Advent of Code, Day 4, Part 2")
print(sum(cards.values()))
