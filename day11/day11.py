def print_galaxies(galaxies):
    max_x = max([galaxy[0] for galaxy in galaxies])
    for y in range(max([galaxy[1] for galaxy in galaxies]) + 1):
        print("".join([ "#" if (x, y) in galaxies else "." for x in range(max_x + 1)]))

def get_galaxies():
    galaxies = []
    row = 0
    lines = open('input', 'r').readlines()
    for line in lines:
        line = line.strip()
        for x in range(len(line)):
            if line[x] == "#":
                galaxies.append((x, row))
        row += 1
    return galaxies

def get_blanks(galaxies):
    max_rows = max([ galaxy[1] for galaxy in galaxies ])
    max_columns = max([ galaxy[0] for galaxy in galaxies ])
    blank_rows = [ y for y in range(max_rows+1) if len([galaxy for galaxy in galaxies if galaxy[1] == y]) == 0 ]
    blank_columns = [ x for x in range(max_columns+1) if len([galaxy for galaxy in galaxies if galaxy[0] == x]) == 0 ]
    return blank_rows, blank_columns

def shift_galaxies(galaxies, blank_rows, blank_columns, multiplier):
    new_galaxies = []
    for galaxy in galaxies:
        shift = len([row for row in blank_rows if row < galaxy[1]])
        new_galaxies.append((galaxy[0], galaxy[1]+(shift*(multiplier-1))))
    galaxies = []
    for galaxy in new_galaxies:
        shift = len([column for column in blank_columns if column < galaxy[0]])
        galaxies.append((galaxy[0]+(shift*(multiplier-1)), galaxy[1]))
    return galaxies

def get_distance(galaxies):
    distances = []
    for a in range(len(galaxies)):
        for b in range(a, len(galaxies)):
            distances.append(abs(galaxies[a][0] - galaxies[b][0]) + abs(galaxies[a][1] - galaxies[b][1]))
    return sum(distances)

print("Advent of Code, Day 10, Part 1")
galaxies = get_galaxies()
blank_rows, blank_columns = get_blanks(galaxies)
galaxies = shift_galaxies(galaxies, blank_rows, blank_columns, 2)
print(get_distance(galaxies))

print("Advent of Code, Day 10, Part 2")
galaxies = get_galaxies()
blank_rows, blank_columns = get_blanks(galaxies)
galaxies = shift_galaxies(galaxies, blank_rows, blank_columns, 1000000)
print(get_distance(galaxies))

