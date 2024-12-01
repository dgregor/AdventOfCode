from itertools import chain
import math

min_distances = {}

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    first = line.split(":")[0]
    rest = line.split(":")[1].split()
    for second in rest:
        min_distances.setdefault(first, {})
        min_distances[first].setdefault("by_distance", {})
        min_distances[first].setdefault("by_name", {})
        min_distances[first].setdefault("by_path", {})
        min_distances[first]["by_name"][first] = 0
        min_distances[first]["by_name"][second] = 1
        min_distances[first]["by_distance"].setdefault(1, set()).add(second)
        min_distances[first]["by_path"][second] = []

        min_distances.setdefault(second, {})
        min_distances[second].setdefault("by_distance", {})
        min_distances[second].setdefault("by_name", {})
        min_distances[second].setdefault("by_path", {})
        min_distances[second]["by_name"][second] = 0
        min_distances[second]["by_name"][first] = 1
        min_distances[second]["by_distance"].setdefault(1, set()).add(first)
        min_distances[second]["by_path"][first] = []

distance = 2
while True:
    changed = False
    for first_node in min_distances.keys():
        if distance - 1 not in min_distances[first_node]["by_distance"]:
            continue
        for second_node in min_distances[first_node]["by_distance"][distance - 1]:
            for third_node in min_distances[second_node]["by_distance"][1]:
                if third_node not in min_distances[first_node]["by_name"]:
                    min_distances[first_node]["by_name"][third_node] = distance
                    min_distances[first_node]["by_distance"].setdefault(distance, set()).add(third_node)
                    min_distances[first_node]["by_path"][third_node] = [second_node]
                    changed = True
                elif min_distances[first_node]["by_name"][third_node] == distance:
                    min_distances[first_node]["by_path"][third_node].append(second_node)
    if not changed:
        distance -= 1
        break
    distance += 1

def get_set(node_a, node_b):
    x = set()
    if node_a < node_b:
        x.add((node_a, node_b))
    else:
        x.add((node_b, node_a))
    return x

def get_path_sets(source_node, dest_node, current, results):
    if not min_distances[source_node]["by_path"][dest_node]:
        current.append(frozenset(get_set(source_node, dest_node)))
        results.append(set(current))
    else:
        for node in min_distances[source_node]["by_path"][dest_node]:
            new_current = current.copy()
            new_current.append(frozenset(get_set(node, dest_node)))
            get_path_sets(source_node, node, new_current, results)

good_counts = {}
for node in min_distances.keys():
    if distance in min_distances[node]["by_distance"]:
        max_distance_for_this_node = max(min_distances[node]["by_distance"].keys())
        for last_node in min_distances[node]["by_distance"][max_distance_for_this_node]:
            path_sets = []
            current = []
            get_path_sets(node, last_node, current, path_sets)
            contenders = set()
            for path in path_sets:
                for this_node in path:
                    contenders.add(this_node)
            contenders = list(contenders)
            for first in range(len(contenders)):
                for second in range(first+1, len(contenders)):
                    for third in range(second+1, len(contenders)):
                        good = True
                        test_set = set([contenders[first], contenders[second], contenders[third]])
                        for path_set_index in range(len(path_sets)):
                            if not path_sets[path_set_index].intersection(test_set):
                                good = False
                                break
                        if good:
                            key = (contenders[first], contenders[second], contenders[third])
                            good_counts.setdefault(key, 0)
                            good_counts[key] += 1
                            break
best = [ x for x in good_counts.keys() if good_counts[x] == max(good_counts.values()) ][0]
best = best[0] | best[1] | best[2]

min_distances = {}

lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    first = line.split(":")[0]
    rest = line.split(":")[1].split()
    for second in rest:
        if (first, second) in best or (second, first) in best:
            continue
        min_distances.setdefault(first, {})
        min_distances[first].setdefault("by_distance", {})
        min_distances[first].setdefault("by_name", {})
        min_distances[first].setdefault("by_path", {})
        min_distances[first]["by_name"][first] = 0
        min_distances[first]["by_name"][second] = 1
        min_distances[first]["by_distance"].setdefault(1, set()).add(second)
        min_distances[first]["by_path"][second] = []

        min_distances.setdefault(second, {})
        min_distances[second].setdefault("by_distance", {})
        min_distances[second].setdefault("by_name", {})
        min_distances[second].setdefault("by_path", {})
        min_distances[second]["by_name"][second] = 0
        min_distances[second]["by_name"][first] = 1
        min_distances[second]["by_distance"].setdefault(1, set()).add(first)
        min_distances[second]["by_path"][first] = []

distance = 2
while True:
    changed = False
    for first_node in min_distances.keys():
        if distance - 1 not in min_distances[first_node]["by_distance"]:
            continue
        for second_node in min_distances[first_node]["by_distance"][distance - 1]:
            for third_node in min_distances[second_node]["by_distance"][1]:
                if third_node not in min_distances[first_node]["by_name"]:
                    min_distances[first_node]["by_name"][third_node] = distance
                    min_distances[first_node]["by_distance"].setdefault(distance, set()).add(third_node)
                    min_distances[first_node]["by_path"][third_node] = [second_node]
                    changed = True
                elif min_distances[first_node]["by_name"][third_node] == distance:
                    min_distances[first_node]["by_path"][third_node].append(second_node)
    if not changed:
        distance -= 1
        break
    distance += 1

group_a = len(min_distances['kdc']['by_name'])
print("Advent of Code, Day 25, Part 1")
print(( len(min_distances) - group_a ) * group_a)


