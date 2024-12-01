import pprint
import re

lines = open('input', 'r').readlines()

games = {}

for line in lines:
    line = line.strip()
    game_number = int(line.split(":")[0].split()[1])
    games[game_number] = []
    turns = line.split(":")[1].split(";")
    for turn in turns:
        match = re.search("([0-9]+) red", turn)
        if match:
            red = int(match.group(1))
        else:
            red = 0
        match = re.search("([0-9]+) green", turn)
        if match:
            green = int(match.group(1))
        else:
            green = 0
        match = re.search("([0-9]+) blue", turn)
        if match:
            blue = int(match.group(1))
        else:
            blue = 0
        games[game_number].append({
            "red": red,
            "green": green,
            "blue": blue
            })

total = 0
for game_num, turns in games.items():
    bad = [ turn for turn in turns if (turn["red"] > 12 or turn["green"] > 13 or turn["blue"] > 14) ]
    if not bad:
        total += game_num

print("Advent of Code, Day 2, Part 1")
print(total)

total = 0
for game_num, turns in games.items():
    red = max( [ turn["red"] for turn in turns ] )
    blue = max( [ turn["blue"] for turn in turns ] )
    green = max( [ turn["green"] for turn in turns ] )
    total += red * blue * green
print("Advent of Code, Day 2, Part 2")
print(total)
