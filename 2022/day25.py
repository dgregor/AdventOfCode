import math
import copy
import pprint
import sys

lines = open('input-25', 'r').readlines()
total = 0
for line in lines:
    line = line.strip()
    if line:
        this_total = 0
        for i in range(len(line)):
            if line[-1 - i] == "=":
                this_total = this_total - (5**i) * 2
            elif line[-1 - i] == "-":
                this_total = this_total - (5**i)
            elif line[-1 - i] in ("1", "2"):
                this_total = this_total + ( (5**i) * int(line[-1 - i]) )
        print(line, this_total)
        total += this_total
print(total)

max_per_spot = [ 2 * 5**i for i in range(21) ]
max_total_per_spot = [ sum([ max_per_spot[i] for i in range(0, j+1)]) for j in range(21) ]
print(max_per_spot)
print(max_total_per_spot)

left = total
start = 0
while max_total_per_spot[start] < left:
    start += 1

print(start)
answer = ""


for i in range(start, -1, -1):
    x = 5**i
    print(i, left, answer)
    y = abs(left)
    if i == 0:
        if left == 2:
            answer += "2"
        if left == 1:
            answer += "1"
        if left == 0:
            answer += "0"
        if left == -1:
            answer += "-"
        if left == -2:
            answer += "="
        continue
    if max_total_per_spot[i-1] > y:
        answer += "0"
    elif x + max_total_per_spot[i-1] > y:
        if left > 0:
            answer += "1"
            left -= x
        else:
            answer += "-"
            left += x
    else:
        if left > 0:
            answer += "2"
            left -= x * 2
        else:
            answer += "="
            left += x * 2
print()
print(answer, left)
