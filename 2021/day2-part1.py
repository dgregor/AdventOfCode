lines = open('input-2', 'r').readlines()
horizontal = 0
depth = 0

for line in lines:
    if line.startswith("forward"):
        horizontal += int(line.strip().split()[1])
    elif line.startswith("down"):
        depth += int(line.strip().split()[1])
    elif line.startswith("up"):
        depth -= int(line.strip().split()[1])
print(horizontal, depth, horizontal * depth)
