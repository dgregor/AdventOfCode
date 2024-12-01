lines = open("input-1", "r").readlines()
windows = []

count = 0

for line in lines:
    value = int(line.strip())
    while len(windows) <= (count + 2):
        windows.append([])
    windows[count].append(value)
    windows[count+1].append(value)
    windows[count+2].append(value)
    count += 1

increase_count = 0
prev_window = None
print(len(lines))
print(len(windows))
for window in windows:
    if len(window) == 3:
        this_window = sum(window) / 3
        if prev_window is not None and this_window > prev_window:
            increase_count += 1
        prev_window = this_window
        print(window, this_window)
print(increase_count)
