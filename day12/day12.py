seen_permutations = {}
def _permutations(line, damaged_counts):
    if (line, damaged_counts) in seen_permutations:
        return seen_permutations[(line, damaged_counts)]
    assert damaged_counts
    total = 0
    first = damaged_counts[0]
    for index in range(len(line)):
        if index + first > len(line):
            break
        if line[index:index+first].find(".") > -1:
            if line[index] == "#":
                break
            continue
        if len(damaged_counts) == 1:
            if "#" not in line[index+first:]:
                total += 1
            else:
                pass
        else:
            if index+first >= len(line) - 1:
                break
            if line[index+first] != "#":
                subtotal = _permutations(line[index + first + 1:], damaged_counts[1:])
                total += subtotal
            else:
                pass
        if line[index] == "#":
            break
    seen_permutations[(line, damaged_counts)] = total
    return seen_permutations[(line, damaged_counts)]

grand_total = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    damage_counts = [ int(x) for x in line.split()[1].split(",")]
    text = line.split()[0]
    perms = _permutations(text, tuple(damage_counts))
    grand_total += perms

print("Advent of Code, Day 19, Part 1")
print(grand_total)

grand_total = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    damage_counts = [ int(x) for x in line.split()[1].split(",")]
    text = line.split()[0]
    damage_counts = damage_counts * 5
    text = text + "?" + text + "?" + text + "?" + text + "?" + text
    perms = _permutations(text, tuple(damage_counts))
    grand_total += perms

print("Advent of Code, Day 19, Part 2")
print(grand_total)

