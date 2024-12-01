import re
import sys

lines = open('input-5', 'r').readlines()

crates = {}

for line in lines:
    line = line.strip()
    if "[" in line:
        start = 0
        while True:
            location = line.find("[", start)
            if location == -1:
                break
            crate = (location // 4) + 1
            crates.setdefault(crate, [])
            crates[crate].insert(0, line[location+1:location+2])
            start = location + 1
    if line.startswith("move"):
        match = re.match("move (\d+) from (\d+) to (\d+)", line)
        assert match, line
        how_many = int(match.group(1))
        from_crate = int(match.group(2))
        to_crate = int(match.group(3))
        move = crates[from_crate][-how_many:]
        crates[from_crate] = crates[from_crate][0:-how_many]
        crates[to_crate] = crates[to_crate] + move
      
#        print(line, how_many, from_crate, to_crate, move, crates[from_crate])
#        count = 1
#        while count <= how_many:
#            count += 1
#            value = crates[from_crate].pop(len(crates[from_crate]) - 1)
#            crates[to_crate].append(value)


tops = ""
for crate_number in sorted(crates.keys()):
    tops += crates[crate_number][-1]

print(tops)
print(crates)
