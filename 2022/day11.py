import time
import gmpy2
import pprint
import re
import sys

from gmpy2 import mpz

monkeys = []

lines = open('input-11', 'r').readlines()

this_monkey = False
for line in lines:
    line = line.strip()
    line = line.replace(",", "")
    pieces = line.split()
    if not len(pieces):
        monkeys.append(this_monkey)
        continue
    if pieces[0] == "Monkey":
        this_monkey = { "count": 0 }
    elif pieces[0] == "Starting":
        this_monkey["items"] = [ mpz(x) for x in pieces[2:] ]
    elif pieces[0] == "Operation:":
        this_monkey["operation"] = pieces[4:]
    elif pieces[0] == "Test:":
        this_monkey["test"] = int(pieces[3])
    elif pieces[1] == "true:":
        this_monkey["true"] = int(pieces[5])
    elif pieces[1] == "false:":
        this_monkey["false"] = int(pieces[5])
monkeys.append(this_monkey)

pprint.pprint(monkeys)
for round in range(300):
    print(round)
    for monkey in monkeys:
        start = time.time()
        for item in monkey["items"]:
            monkey["count"] += 1
            if monkey["operation"][0] == "+":
                if monkey["operation"][1] == "old":
                    worry = item + item
                else:
                    worry = item + int(monkey["operation"][1])
                #if round > 150:
                #    print(time.time() - start, "addition")
            if monkey["operation"][0] == "*":
                if monkey["operation"][1] == "old":
                    worry = item * item
                else:
                    worry = item * mpz(monkey["operation"][1])
            new_time = time.time()
            if round > 200:
                print(new_time - start, "operation", monkey["operation"])
            #worry = worry // 3
            test_is_true = False
            #if monkey["test"] == 2:
            #    if int(str(worry)[-1]) % 2 == 0:
            #        test_is_true = True
            #    else:
            #        pass
            #elif monkey["test"] == 3:
            #    if sum([ int(x) for x in str(worry) ]) % 3 == 0:
            #        test_is_true = True
            #    else:
            #        pass
            #elif monkey["test"] == 5:
            #    if int(str(worry)[-1]) % 5 == 0:
            #        test_is_true = True
            #    else:
            #        pass
            #elif worry % monkey["test"] == 0:
            #        test_is_true = True
            #if test_is_true:
            if worry % monkey["test"] == 0:
                monkeys[monkey["true"]]["items"].append(worry)
            else:
                monkeys[monkey["false"]]["items"].append(worry)
            if round > 200:
                print(time.time() - new_time, "test")
        if round > 200:
            print(time.time() - start, monkey["test"], len(monkey["items"]))
        monkey["items"] = []
    #print(round, time.time() - start)
#    pprint.pprint(monkeys)

counts = [ monkey["count"] for monkey in monkeys ]
counts.sort()
print(counts)
print(counts[-1] * counts[-2])
