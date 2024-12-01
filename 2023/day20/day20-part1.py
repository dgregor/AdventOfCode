modules = {}
broadcaster = None
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    parts = [ x.strip() for x in line.split("->") ]
    if parts[0] == "broadcaster":
        broadcaster = [ x.strip() for x in parts[1].split(",") ]
        continue
    modules[parts[0][1:]] = { "type": parts[0][0],
                              "dest": [ x.strip() for x in parts[1].split(",") ],
                              "inputs": {},
                             }
    if parts[0][0] == "%":
        modules[parts[0][1:]]["state"] = "off"

module_names = [ x for x in modules.keys() ]
for name in module_names:
    module = modules[name]
    for dest in module["dest"]:
        if dest not in modules:
            modules[dest] = { "type": "@",
                              "dest": [],
                              "inputs": {} }
        modules[dest]["inputs"][name] = "low"

done = { "high": 0,
         "low": 0 }
for count in range(1000):
    to_process = [ (None, "low", "broadcaster" ) ]
    while to_process:
        signal = to_process.pop(0)
        from_module = signal[0]
        strength = signal[1]
        destination = signal[2]
        if strength == "low":
            done["low"] += 1
        else:
            done["high"] += 1
        if destination == "broadcaster":
            for target in broadcaster:
                to_process.append(("broadcaster", strength, target))
        elif modules[destination]["type"] == "%":
            if strength == "low":
                if modules[destination]["state"] == "off":
                    modules[destination]["state"] = "on"
                    for x in modules[destination]["dest"]:
                        to_process.append((destination, "high", x))
                else:
                    modules[destination]["state"] = "off"
                    for x in modules[destination]["dest"]:
                        to_process.append((destination, "low", x))
        elif modules[destination]["type"] == "&":
            modules[destination]["inputs"][from_module] = strength
            if "low" in modules[destination]["inputs"].values():
                for x in modules[destination]["dest"]:
                    to_process.append((destination, "high", x))
            else:
                for x in modules[destination]["dest"]:
                    to_process.append((destination, "low", x))
print("Advent of Code, Day 19, Part 1")
print(done["high"] * done["low"])

