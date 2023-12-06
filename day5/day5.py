import pprint
import re

seeds = []
maps = {
    "soil": [],
    "fertilizer": [],
    "water": [],
    "light": [],
    "temperature": [],
    "humidity": [],
    "location": []
    }

def get_value(starting, map_name):
    global maps
    for mapping in maps[map_name]:
        if starting >= mapping[1] and starting < mapping[1] + mapping[2]:
            return mapping[0] + (starting - mapping[1])
    return starting

def get_value_reverse(ending, map_name):
    global maps
    for mapping in maps[map_name]:
        if ending >= mapping[0] and ending < mapping[0] + mapping[2]:
            return mapping[1] + (ending - mapping[0])
    return ending

current_map = None
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    if line == "":
        continue
    elif line.startswith("seeds"):
        seeds = [ int(x) for x in line.split(":")[1].split() ]
    elif line.startswith("seed-to-soil"):
        current_map = "soil"
    elif line.startswith("soil-to-fertilizer"):
        current_map = "fertilizer"
    elif line.startswith("fertilizer-to-water"):
        current_map = "water"
    elif line.startswith("water-to-light"):
        current_map = "light"
    elif line.startswith("light-to-temperature"):
        current_map = "temperature"
    elif line.startswith("temperature-to-humidity"):
        current_map = "humidity"
    elif line.startswith("humidity-to-location"):
        current_map = "location"
    else:
        maps[current_map].append([ int(x) for x in line.split() ])

locations = []
for seed in seeds:
    soil = get_value(seed, "soil")
    fertilizer = get_value(soil, "fertilizer")
    water = get_value(fertilizer, "water")
    light = get_value(water, "light")
    temperature = get_value(light, "temperature")
    humidity = get_value(temperature, "humidity")
    location = get_value(humidity, "location")
    locations.append(location)

print("Advent of Code, Day 5, Part 1")
print(min(locations))

seed_pairs = []
locations = []

for x in range(0, len(seeds), 2):
    seed_pairs.append([seeds[x], seeds[x+1]])

location = 0
while True:
    humidity = get_value_reverse(location, "location")
    temperature = get_value_reverse(humidity, "humidity")
    light = get_value_reverse(temperature, "temperature")
    water = get_value_reverse(light, "light")
    fertilizer = get_value_reverse(water, "water")
    soil = get_value_reverse(fertilizer, "fertilizer")
    seed = get_value_reverse(soil, "soil")
    found = False
    for x in seed_pairs:
        if seed >= x[0] and seed < x[0] + x[1]:
            found = True
            break
    if found:
        print("Advent of Code, Day 5, Part 2")
        print(location)
        break
    location += 1

# To be continued... without brute force
#mappings = []
#for mapping in maps["soil"]:
#    mappings.append(mapping)
#new_mappings = []
#for orig_mapping in mappings:
#    for mapping in maps["fertilizer"]:

