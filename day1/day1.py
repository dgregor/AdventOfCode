lines = open('input', 'r').readlines()

words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
def replace_first_word(line):
    for x in range(len(line)):
        for word_index in range(len(words)):
            try:
                if line[x:x+len(words[word_index])] == words[word_index]:
                    return line[0:x] + str(word_index + 1) + line[x+1:]
            except:
                pass
    return line

def execute(lines, day1):
    total = 0
    for line in lines:
        line = line.strip()
        orig_line = line
        if not day1:
            while True:
                new_line = replace_first_word(line)
                if line == new_line:
                    break
                line = new_line
        first = None
        second = None
        for x in range(len(line)):
            try:
                first = int(line[x])
                break
            except:
                pass
        for x in reversed(range(len(line))):
            try:
                second = int(line[x])
                break
            except:
                pass
        total += int(str(first) + str(second))
    return total

print("Advent of Code, Day 1, Part 1")
print(execute(lines, True))

print("Advent of Code, Day 1, Part 2")
print(execute(lines, False))


