workflows = {}
parts = []

do_workflows = True
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if not line:
        do_workflows = False
        continue
    if do_workflows:
        workflow_name = line.split("{")[0]
        workflows[workflow_name] = []
        tests = line[:-1].split("{")[1].split(",")
        for test in tests:
            if test.find(":") > -1:
                workflows[workflow_name].append( { "letter": test[0],
                                                   "comparison": test[1],
                                                   "value": int(test[2:].split(":")[0]),
                                                   "target": test[2:].split(":")[1] } )
            else:
                workflows[workflow_name].append( { "letter": None,
                                                   "comparison": None,
                                                   "value": None,
                                                   "target": test } )
    else:
        items = line[1:-1].split(",")
        parts.append( { "x": int(items[0].split("=")[1]),
                        "m": int(items[1].split("=")[1]),
                        "a": int(items[2].split("=")[1]),
                        "s": int(items[3].split("=")[1]),
                       })

def get_target(workflow_name, item):
    for workflow in workflows[workflow_name]:
        if workflow["comparison"] is None:
            if workflow["target"] in ( "A", "R" ):
                return workflow["target"]
            return get_target(workflow["target"], item)
        elif workflow["comparison"] == ">":
            if item[workflow["letter"]] > workflow["value"]:
                if workflow["target"] in ( "A", "R" ):
                    return workflow["target"]
                else:
                    return get_target(workflow["target"], item)
        else:
            if item[workflow["letter"]] < workflow["value"]:
                if workflow["target"] in ( "A", "R" ):
                    return workflow["target"]
                else:
                    return get_target(workflow["target"], item)

def accept_part(part):
    return get_target("in", item)

total = 0
for part in parts:
    foo = get_target("in", part)
    if foo == "A":
        total += part["x"] + part["m"] + part["a"] + part["s"]

print("Advent of Code, Day 19, Part 1")
print(total)

