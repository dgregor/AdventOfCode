import sys

lines = open('input-4', 'r').readlines()

total = 0

for line in lines:
    elfA, elfB = line.strip().split(',')
    aMin, aMax = elfA.split('-')
    bMin, bMax = elfB.split('-')
    aMin = int(aMin)
    aMax = int(aMax)
    bMin = int(bMin)
    bMax = int(bMax)
    if (aMin >= bMin and aMin <= bMax) or \
       (aMax >= bMin and aMax <= bMax) or \
       (bMin >= aMin and bMin <= aMax) or \
       (bMax >= aMin and bMax <= aMax):
        total += 1
    
print(total)
