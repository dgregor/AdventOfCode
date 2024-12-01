import sys

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lines = open('input-day1', 'r').readlines()

most = [0,0,0]
max = 0

total = 0

for line in lines:
    line = line.strip()
    if line == "":
        if total > most[0]:
            most[0] = total
            most.sort()
        total = 0
        continue
    total += int(line)
if total > most[0]:
    most[0] = total
    most.sort()

print(sum(most))
