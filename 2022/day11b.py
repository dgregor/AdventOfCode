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
        this_monkey["items"] = [ { "original": int(x), "current": int(x), "item_history": [], "remainders": [] } for x in pieces[2:] ]
    elif pieces[0] == "Operation:":
        this_monkey["operation"] = pieces[4:]
    elif pieces[0] == "Test:":
        this_monkey["test"] = int(pieces[3])
    elif pieces[1] == "true:":
        this_monkey["true"] = int(pieces[5])
    elif pieces[1] == "false:":
        this_monkey["false"] = int(pieces[5])
monkeys.append(this_monkey)

for monkey in monkeys:
    for item in monkey["items"]:
        for i in range(len(monkeys)):
            item["remainders"].append(item["current"] % monkeys[i]["test"])

pprint.pprint(monkeys)
for round in range(10000):
    print("ROUND", round)
    for monkey_num in range(len(monkeys)):
        monkey = monkeys[monkey_num]
        for item in monkey["items"]:
            monkey["count"] += 1
            item["item_history"].append(monkey_num)
#            print(item)
#            print("".join([ str(x) for x in item["item_history"] ]))
            #if round > 150:
            #    assert monkey_num in (0, 3, 5, 2), monkey_num
            #    if monkey_num == 0:
            #        monkeys[3]["items"].append(item)
            #    elif monkey_num == 3:
            #        monkeys[5]["items"].append(item)
            #    elif monkey_num == 5:
            #        monkeys[2]["items"].append(item)
            #    elif monkey_num == 2:
            #        monkeys[0]["items"].append(item)
            #    continue

            if monkey["operation"][0] == "+":
                addend = int(monkey["operation"][1])
                #item['current'] = item['current'] + addend)
                for test_monkey_num in range(len(monkeys)):
                    item["remainders"][test_monkey_num] = (item["remainders"][test_monkey_num] + addend) % monkeys[test_monkey_num]["test"]
            if monkey["operation"][0] == "*":
                if monkey["operation"][1] == "old":
                    for test_monkey_num in range(len(monkeys)):
                        item["remainders"][test_monkey_num] = (item["remainders"][test_monkey_num] * item["remainders"][test_monkey_num]) % monkeys[test_monkey_num]["test"]
                    #item['current'] = item['current'] * item['current']
                else:
                    for test_monkey_num in range(len(monkeys)):
                        item["remainders"][test_monkey_num] = (item["remainders"][test_monkey_num] * int(monkey["operation"][1])) % monkeys[test_monkey_num]["test"]
                    #item['current'] = item['current'] * int(monkey["operation"][1])
            #item['current'] = item['current'] // 3
            # if item['current'] % monkey["test"] == 0:
            #     monkeys[monkey["true"]]["items"].append(item)
            # else:
            #     monkeys[monkey["false"]]["items"].append(item)
            if item['remainders'][monkey_num] == 0:
                monkeys[monkey["true"]]["items"].append(item)
            else:
                monkeys[monkey["false"]]["items"].append(item)
        monkey["items"] = []

counts = [ monkey["count"] for monkey in monkeys ]
counts.sort()
print(counts)
print(counts[-1] * counts[-2])
#pprint.pprint([ [ str(item["item_history"]) for item in monkey["items"] ] for monkey in monkeys])
max_values = []
for i in range(8):
    max_values.append(0)
for monkey_num in range(len(monkeys)):
    monkey = monkeys[monkey_num]
#    print("monkey", monkey_num)
    for item in monkey["items"]:
#        print("".join([ str(x) for x in item["item_history"] ]))
#        print(len(item["item_history"]), item["item_history"])
        for i in range(8):
#            print(i, len(item["item_history"]))
            for j in range(len(item["item_history"]) -1, 0, -1):
                if item["item_history"][j] == i:
                    max_values[i] = j
                    break
                    #if i not in (0, 2, 3, 5):
                        #print(i, j, max_values[i])
                    #if j > max_values[i]:
                    #    print(i, j, max_values[i])
print(max_values)
