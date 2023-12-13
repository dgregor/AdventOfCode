def find_points_of_reflection(strings, with_smudge=False):
    found = []
    for index in range(len(strings) - 1):
        error_count = 0
        for offset in range(len(strings) - 1):
            if index - offset < 0 or index + offset + 1 >= len(strings):
                continue
            if strings[index-offset] != strings[index+offset+1]:
                error_count += len( [ x for x in range(len(strings[index-offset])) if strings[index-offset][x] != strings[index+offset+1][x] ] )
            if error_count > 1:
                break
            elif error_count == 1 and not with_smudge:
                break
        if with_smudge:
            if error_count == 1:
                found.append(index+1)
        else:
            if error_count == 0:
                found.append(index+1)
    return found

grids = []
rows = []

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if line == "":
        columns = []
        for i in range(len(rows[0])):
            columns.append("".join([ rows[x][i] for x in range(len(rows)) ]))
        grids.append({ 'rows': rows,
                       'columns': columns })
        rows = []
    else:
        rows.append(line)


print("Advent of Code, Day 13, Part 1")
score = 0
for grid in grids:
    for column in find_points_of_reflection(grid['columns']):
        score += column
    for row in find_points_of_reflection(grid['rows']):
        score += 100 * row
print(score)

print("Advent of Code, Day 13, Part 2")
score = 0
for grid in grids:
    for column in find_points_of_reflection(grid['columns'], True):
        score += column
    for row in find_points_of_reflection(grid['rows'], True):
        score += 100 * row
print(score)

