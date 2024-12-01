lines = open('input-2', 'r').readlines()
horizontal = 0
depth = 0
aim = 0

for line in lines:
    if line.startswith("forward"):
        horizontal += int(line.strip().split()[1])
        depth += int(line.strip().split()[1]) * aim
    elif line.startswith("down"):
        aim += int(line.strip().split()[1])
    elif line.startswith("up"):
        aim -= int(line.strip().split()[1])
print(horizontal, depth, horizontal * depth)
