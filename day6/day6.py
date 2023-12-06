import pprint

times = []
distances = []

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if line.startswith("Time"):
        times = [ int(x) for x in line.split(":")[1].split() ]
    else:
        distances = [ int(x) for x in line.split(":")[1].split() ]

winners = []
for race in range(len(times)):
    winning = [ x for x in range(times[race]) if (x * (times[race] - x)) > distances[race] ]
    winners.append(len(winning))

print("Advent of Code, Day 5, Part 1")
total = 1
for x in range(len(winners)):
    total *= winners[x]
print(total)

race_time = int("".join([ str(x) for x in times]))
race_distance = int("".join([ str(x) for x in distances]))
first = None
last = None
for x in range(race_time):
    if x * (race_time - x) > race_distance:
        first = x
        break
for x in range(race_time, 0, -1):
    if x * (race_time - x) > race_distance:
        last = x
        break

print("Advent of Code, Day 5, Part 2")
print(last - first + 1)
