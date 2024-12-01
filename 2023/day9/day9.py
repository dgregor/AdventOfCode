def get_diffs(numbers):
    diffs = []
    for i in range(len(numbers) - 1):
        diffs.append(numbers[i+1] - numbers[i])
    return diffs

def get_next_value(numbers):
    if len(set(numbers)) == 1 and numbers[0] == 0:
        return 0
    else:
        return numbers[-1] + get_next_value(get_diffs(numbers))

def get_prev_value(numbers):
    if len(set(numbers)) == 1 and numbers[0] == 0:
        return 0
    else:
        return numbers[0] - get_prev_value(get_diffs(numbers))

total = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    total += get_next_value([ int(x) for x in line.split()])

print("Advent of Code, Day 9, Part 1")
print(total)

total = 0
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    total += get_prev_value([ int(x) for x in line.split()])
print("Advent of Code, Day 9, Part 2")
print(total)

