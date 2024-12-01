lines = open("input-1", "r").readlines()
count = 0
prev_line = None
for line in lines:
    if prev_line is not None and int(line.strip()) > prev_line:
        count += 1
    prev_line = int(line.strip())
print(count)
