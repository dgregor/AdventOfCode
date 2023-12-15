def hash(code):
    current = 0
    for letter in code:
        current += ord(letter)
        current = (current * 17) % 256
    return current

total = 0

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    for part in line.split(","):
        count = hash(part)
        total += count

print("Advent of Code, Day 15, Part 1")
print(total)

boxes = []
for i in range(256):
    boxes.append([])

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    for part in line.split(","):
        if part.endswith("-"):
            key = part[:-1]
            hash_value = hash(key)
            for i in range(len(boxes[hash_value])):
                if boxes[hash_value][i][0] == key:
                    boxes[hash_value].pop(i)
                    break
        else:
            value = int(part[-1])
            key = part[:-2]
            hash_value = hash(key)
            found = False
            for i in range(len(boxes[hash_value])):
                if boxes[hash_value][i][0] == key:
                    boxes[hash_value][i] = (key, value)
                    found = True
                    break
            if not found:
                boxes[hash_value].append((key, value))

power = 0
for box_num in range(len(boxes)):
    for lens_num in range(len(boxes[box_num])):
        power += (box_num + 1) * (lens_num + 1) * boxes[box_num][lens_num][1]

print("Advent of Code, Day 15, Part 2")

