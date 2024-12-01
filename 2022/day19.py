import copy
import pprint
import sys


minutes_total = 32
blueprints = {}
lines = open('input-19', 'r').readlines()
for line in lines:
    line = line.strip().replace(":", "")
    parts = line.split()
    blueprints[int(parts[1])] = {
        "ore": int(parts[6]),
        "clay": int(parts[12]),
        "obsidian": {
            "ore": int(parts[18]),
            "clay": int(parts[21]),
            },
        "geode": {
            "ore": int(parts[27]),
            "obsidian": int(parts[30])
            },
        "score": 0
        }

def print_score(score, blueprint):
    parts = score.split(",")
    ore_collected = 0
    clay_collected = 0
    obsidian_collected = 0
    geodes_collected = 0
    ore_robots = 1
    clay_robots = 0
    obsidian_robots = 0
    geode_robots = 0
    for i in range(1, len(parts)):
        ore_collected += ore_robots
        clay_collected += clay_robots
        obsidian_collected += obsidian_robots
        geodes_collected += geode_robots
        for action in parts[i].split("|"):
            if action == "ore":
                ore_robots += 1
                ore_collected -= blueprint["ore"]
            elif action == "clay":
                clay_robots += 1
                ore_collected -= blueprint["clay"]
            elif action == "obsidian":
                obsidian_robots += 1
                ore_collected -= blueprint["obsidian"]["ore"]
                clay_collected -= blueprint["obsidian"]["clay"]
            elif action == "geode":
                geode_robots += 1
                ore_collected -= blueprint["geode"]["ore"]
                obsidian_collected -= blueprint["geode"]["obsidian"]
        print("After {} rounds passed".format(i))
        print("Ore: {}".format(ore_collected))
        print("Clay: {}".format(clay_collected))
        print("Obsidian: {}".format(obsidian_collected))
        print("Geodes: {}".format(geodes_collected))
        print("Ore Robots: {}".format(ore_robots))
        print("Clay Robots: {}".format(clay_robots))
        print("Obsidian Robots: {}".format(obsidian_robots))
        print("Geode Robots: {}".format(geode_robots))

def calculate_score(blueprint, state):
    global minutes_total
    rv = []

    minutes_passed, ore_collected, ore_robots, clay_collected, clay_robots, obsidian_collected, obsidian_robots, geode_collected, geode_robots, rounds = state

    def round_string(action):
        return "," + action

    minutes_left = minutes_total - minutes_passed

    # figure out max potential geodes from robots we don't have yet
    obsidian_gap = blueprint["geode"]["obsidian"] - obsidian_collected
    closest_next_geode_robot = minutes_left - 0
    if closest_next_geode_robot % 2 == 1:
        max_additional_geodes = (closest_next_geode_robot + 2) * (closest_next_geode_robot // 2) + 1
    else:
        max_additional_geodes = (closest_next_geode_robot + 1) * (closest_next_geode_robot // 2)

    if not ( geode_collected + (geode_robots * minutes_left ) + max_additional_geodes > blueprint["score"] ):
        return rv
    can_skip_ore = True #ore_robots >= max(blueprint["clay"], blueprint["obsidian"]["ore"], blueprint["geode"]["ore"]) or ore_collected < blueprint["ore"]
    if obsidian_collected >= blueprint["geode"]["obsidian"] and ore_collected >= blueprint["geode"]["ore"] and can_skip_ore:
        rv.append((minutes_passed + 1,
                   ore_collected + ore_robots - blueprint["geode"]["ore"],
                   ore_robots,
                   clay_collected + clay_robots,
                   clay_robots,
                   obsidian_collected + obsidian_robots - blueprint["geode"]["obsidian"],
                   obsidian_robots,
                   geode_collected + geode_robots,
                   geode_robots + 1,
                   rounds + round_string("geode")))
    if can_skip_ore:
        rv.append((minutes_passed + 1,
                   ore_collected + ore_robots,
                   ore_robots,
                   clay_collected + clay_robots,
                   clay_robots,
                   obsidian_collected + obsidian_robots,
                   obsidian_robots,
                   geode_collected + geode_robots,
                   geode_robots,
                   rounds + round_string("")))
    if clay_collected >= blueprint["obsidian"]["clay"] and ore_collected >= blueprint["obsidian"]["ore"] and (
            clay_collected <= blueprint["obsidian"]["clay"] + clay_robots or ore_collected <= blueprint["obsidian"]["ore"] + ore_robots) and obsidian_robots < blueprint["geode"]["obsidian"] and can_skip_ore:
        rv.append((minutes_passed + 1,
                   ore_collected + ore_robots - blueprint["obsidian"]["ore"],
                   ore_robots,
                   clay_collected + clay_robots - blueprint["obsidian"]["clay"],
                   clay_robots,
                   obsidian_collected + obsidian_robots,
                   obsidian_robots + 1,
                   geode_collected + geode_robots,
                   geode_robots,
                   rounds + round_string("obsidian")))
    if ore_collected >= blueprint["clay"] and ore_collected < blueprint["clay"] + ore_robots and clay_robots <= blueprint["obsidian"]["clay"] and can_skip_ore:
        rv.append((minutes_passed + 1,
                   ore_collected + ore_robots - blueprint["clay"],
                   ore_robots,
                   clay_collected + clay_robots,
                   clay_robots + 1,
                   obsidian_collected + obsidian_robots,
                   obsidian_robots,
                   geode_collected + geode_robots,
                   geode_robots,
                   rounds + round_string("clay")))
    # and ore_collected < blueprint["ore"] + ore_robots 
    if ore_collected >= blueprint["ore"] and ore_robots < max(blueprint["geode"]["ore"],
                                                              blueprint["obsidian"]["ore"],
                                                              blueprint["clay"],
                                                              0 if clay_robots == blueprint["obsidian"]["clay"] else blueprint["ore"]):
        rv.append((minutes_passed + 1,
                   ore_collected + ore_robots - blueprint["ore"],
                   ore_robots + 1,
                   clay_collected + clay_robots,
                   clay_robots,
                   obsidian_collected + obsidian_robots,
                   obsidian_robots,
                   geode_collected + geode_robots,
                   geode_robots,
                   rounds + round_string("ore")))
    return rv

quality = 0
for blueprint_number, blueprint in blueprints.items():
    if blueprint_number >= 4:
        continue
    print("blueprint", blueprint_number, blueprint)
    to_check = set()
    to_check.add(( 0, # 0 minutes_passed
                   0, # 1 ore_collected
                   1, # 2 ore_robots
                   0, # 3 clay_collected
                   0, # 4 clay_robots
                   0, # 5 obsidian_collected
                   0, # 6 obsidian_robots
                   0, # 7 geode_collected
                   0, # 8 geode_robots
                   "" # 9 rounds w/ geode robots
                  ))
    while to_check:
        args = to_check.pop()
#        print(len(to_check), blueprint["score"], args)
        if args[0] == minutes_total:
            #print(blueprint["score"], args["ore_collected"], args["clay_collected"], args["obsidian_collected"], args["geode_collected"])
            if args[7] > blueprint["score"]:
                print(args[7], args)
#                print_score(args[9], blueprint)
            blueprint["score"] = max(blueprint["score"], args[7])
        else:
            for item in calculate_score(blueprint, args):
                #print(item)
                to_check.add(item)
    print(blueprint["score"])
    quality += blueprint_number * blueprint["score"]

print(quality)
