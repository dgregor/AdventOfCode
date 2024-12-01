import copy
import pprint
import sys


def print_item(item):
    print(item["value"], item["incoming"]["value"], item["outgoing"]["value"])

def print_items(item):
    if True:
        orig_item = item
        next_item = item["outgoing"]
        values = [item["value"]]
        while next_item != orig_item:
            values.append(next_item["value"])
            next_item = next_item["outgoing"]
        print(item["value"], ",".join([ str(x) for x in values ]))
    else:
        print(item["value"])

orig_list = []
key = 811589153
lines = open('input-20', 'r').readlines()
for line in lines:
    number = int(line.strip())
    orig_list.append( { "value": number * key,
                        "incoming": None,
                        "outgoing": None
                       } )
line_length = len(lines)
print(len(orig_list), line_length)

for i in range(line_length):
    if i == 0:
        orig_list[i]["incoming"] = orig_list[-1]
    else:
        orig_list[i]["incoming"] = orig_list[i - 1]
    if i == line_length - 1:
        orig_list[i]["outgoing"] = orig_list[0]
    else:
        orig_list[i]["outgoing"] = orig_list[i + 1]

for k in range(10):
    for i in range(line_length):
        value = orig_list[i]["value"]
        if value % (line_length - 1) != 0:
            this_item = orig_list[i]
            this_item["incoming"]["outgoing"] = this_item["outgoing"]
            this_item["outgoing"]["incoming"] = this_item["incoming"]
            target_item = this_item
            if value > 0:
                for j in range(0, value % (line_length - 1)):
                    target_item = target_item["outgoing"]
                this_item["outgoing"] = target_item["outgoing"]
                this_item["outgoing"]["incoming"] = this_item
                this_item["incoming"] = target_item
                this_item["incoming"]["outgoing"] = this_item
            else:
                for j in range(0, abs(value) % (line_length - 1)):
                    target_item = target_item["incoming"]
                this_item["incoming"] = target_item["incoming"]
                this_item["incoming"]["outgoing"] = this_item
                this_item["outgoing"] = target_item
                this_item["outgoing"]["incoming"] = this_item
        #print_items(orig_list[i])

item = orig_list[0]
while item["value"] != 0:
    item = item["outgoing"]
print_item(item)
values = []
for i in range(1, 3001):
    item = item["outgoing"]
    if i % 1000 == 0:
        values.append(item["value"])
        print_item(item)
print(sum(values))

