workflows = {}
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if not line:
        break
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
good = []
tests = [ { "workflow_name": "in", "workflow_index": 0, "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000) } ]

while tests:
    test = tests.pop()
    workflow_name = test["workflow_name"]
    for workflow_index in range(len(workflows[workflow_name])):
        if workflow_index < test["workflow_index"]:
            continue
        workflow = workflows[workflow_name][workflow_index]
        if workflow["comparison"] is None:
            if workflow["target"] == "A":
                good.append(test)
                continue
            elif workflow["target"] == "R":
                continue
            tests.append( { "workflow_name": workflow["target"],
                            "workflow_index": 0,
                            "x": test["x"],
                            "m": test["m"],
                            "a": test["a"],
                            "s": test["s"],
                            })
        elif workflow["comparison"] == ">":
            if test[workflow["letter"]][1] > workflow["value"]:
                if workflow["target"] == "R":
                    pass
                elif workflow["target"] == "A":
                    good.append({ "workflow_name": test["workflow_name"],
                                  "workflow_index": test["workflow_index"],
                                  "x": test["x"] if "x" != workflow["letter"] else (max(workflow["value"]+1, test["x"][0]), test["x"][1]),
                                  "m": test["m"] if "m" != workflow["letter"] else (max(workflow["value"]+1, test["m"][0]), test["m"][1]),
                                  "a": test["a"] if "a" != workflow["letter"] else (max(workflow["value"]+1, test["a"][0]), test["a"][1]),
                                  "s": test["s"] if "s" != workflow["letter"] else (max(workflow["value"]+1, test["s"][0]), test["s"][1]),
                                 })
                else:
                    tests.append({ "workflow_name": workflow["target"],
                                   "workflow_index": 0,
                                   "x": test["x"] if "x" != workflow["letter"] else (max(workflow["value"]+1, test["x"][0]), test["x"][1]),
                                   "m": test["m"] if "m" != workflow["letter"] else (max(workflow["value"]+1, test["m"][0]), test["m"][1]),
                                   "a": test["a"] if "a" != workflow["letter"] else (max(workflow["value"]+1, test["a"][0]), test["a"][1]),
                                   "s": test["s"] if "s" != workflow["letter"] else (max(workflow["value"]+1, test["s"][0]), test["s"][1]),
                                  })
            if test[workflow["letter"]][0] <= workflow["value"]:
                tests.append({ "workflow_name": test["workflow_name"],
                               "workflow_index": test["workflow_index"] + 1,
                               "x": test["x"] if "x" != workflow["letter"] else (test["x"][0], min(workflow["value"], test["x"][1])),
                               "m": test["m"] if "m" != workflow["letter"] else (test["m"][0], min(workflow["value"], test["m"][1])),
                               "a": test["a"] if "a" != workflow["letter"] else (test["a"][0], min(workflow["value"], test["a"][1])),
                               "s": test["s"] if "s" != workflow["letter"] else (test["s"][0], min(workflow["value"], test["s"][1])),
                              })
        else:
            if test[workflow["letter"]][0] < workflow["value"]:
                if workflow["target"] == "R":
                    pass
                elif workflow["target"] == "A":
                    good.append({ "workflow_name": test["workflow_name"],
                                  "workflow_index": test["workflow_index"],
                                  "x": test["x"] if "x" != workflow["letter"] else (test["x"][0], min(workflow["value"]-1, test["x"][1])),
                                  "m": test["m"] if "m" != workflow["letter"] else (test["m"][0], min(workflow["value"]-1, test["m"][1])),
                                  "a": test["a"] if "a" != workflow["letter"] else (test["a"][0], min(workflow["value"]-1, test["a"][1])),
                                  "s": test["s"] if "s" != workflow["letter"] else (test["s"][0], min(workflow["value"]-1, test["s"][1])),
                                 })
                else:
                    tests.append({ "workflow_name": workflow["target"],
                                   "workflow_index": 0,
                                   "x": test["x"] if "x" != workflow["letter"] else (test["x"][0], min(workflow["value"]-1, test["x"][1])),
                                   "m": test["m"] if "m" != workflow["letter"] else (test["m"][0], min(workflow["value"]-1, test["m"][1])),
                                   "a": test["a"] if "a" != workflow["letter"] else (test["a"][0], min(workflow["value"]-1, test["a"][1])),
                                   "s": test["s"] if "s" != workflow["letter"] else (test["s"][0], min(workflow["value"]-1, test["s"][1])),
                                  })
            if test[workflow["letter"]][1] >= workflow["value"]:
                tests.append({ "workflow_name": test["workflow_name"],
                               "workflow_index": test["workflow_index"] + 1,
                               "x": test["x"] if "x" != workflow["letter"] else (max(workflow["value"], test["x"][0]), test["x"][1]),
                               "m": test["m"] if "m" != workflow["letter"] else (max(workflow["value"], test["m"][0]), test["m"][1]),
                               "a": test["a"] if "a" != workflow["letter"] else (max(workflow["value"], test["a"][0]), test["a"][1]),
                               "s": test["s"] if "s" != workflow["letter"] else (max(workflow["value"], test["s"][0]), test["s"][1]),
                              })
        break

total = 0
for x in good:
    total += (x["x"][1] + 1 - x["x"][0]) * (x["m"][1] + 1 - x["m"][0]) * (x["a"][1] + 1 - x["a"][0]) * (x["s"][1] + 1 - x["s"][0])
print("Advent of Code, Day 19, Part 2")
print(total)
