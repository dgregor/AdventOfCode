import sys

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lines = open('input', 'r').readlines()

total = 0

#for line in lines:
#    line = line.strip()
#    half = len(line) // 2
#    setA = set(line[:half])
#    setB = set(line[half:])
#    priority = characters.index(setA.intersection(setB).pop()) + 1
#    total += priority

count = 0
setA = set()
setB = set()
setC = set()
for line in lines:
    line = line.strip()
    count += 1
    if count == 1:
        setA = set(line)
    elif count == 2:
        setB = set(line)
    elif count == 3:
        setC = set(line)
        common = setA.intersection(setB).intersection(setC)
        priority = characters.index(common.pop()) + 1
        total += priority
        count = 0
    
print(total)
