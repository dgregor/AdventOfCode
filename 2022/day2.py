import sys

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lines = open('input-day2', 'r').readlines()

total = 0

for line in lines:
    line = line.strip()
    first = line.split()[0]
    second = line.split()[1]
    assert first in ("A", "B", "C")
    assert second in ("X", "Y", "Z")
    if second == "X":
        total += 0
        if first == "A":
            total += 3
        elif first == "B":
            total += 1
        elif first == "C":
            total += 2
    elif second == "Y":
        total += 3
        if first == "A":
            total += 1
        elif first == "B":
            total += 2
        elif first == "C":
            total += 3
    elif second == "Z":
        total += 6
        if first == "A":
            total += 2
        elif first == "B":
            total += 3
        elif first == "C":
            total += 1
    else:
        sys.exit(1)
print(total)
