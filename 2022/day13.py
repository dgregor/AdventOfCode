import functools
import time
import pprint
import re
import sys

lines = open('input-13', 'r').readlines()

in_order = []
pairs = [ eval(line.strip()) for line in lines if line.strip() ]
marker_a = eval("[[2]]")
marker_b = eval("[[6]]")
pairs.append(marker_a)
pairs.append(marker_b)

def compare(first, second):
    if type(first) == int:
        if type(second) == int:
            if first < second:
                return 1
            elif first > second:
                return -1
            else:
                return 0
        else:
            return compare([first], second)
    elif type(first) == list:
        if type(second) == int:
            return compare(first, [second])
        else:
            for i in range(len(first)):
                if i > len(second) - 1:
                    return -1
                x = compare(first[i], second[i])
                if x != 0:
                    return x
            if len(first) < len(second):
                return 1
            return 0

#for i in range(0, len(pairs), 2):
#    first = pairs[i]
#    second = pairs[i+1]
#    if compare(first, second) == 1:
#        in_order.append((i // 2) + 1)
#
#print(sum(in_order))

pairs.sort(key=functools.cmp_to_key(compare), reverse=True)
first = pairs.index(marker_a) + 1
second = pairs.index(marker_b) + 1
print(first, second, first * second)

