import scipy
import functools
import time
import pprint
import re
import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

lines = open('input-16', 'r').readlines()

valves = {}
for line in lines:
    line = line.strip()
    parts = line.replace(",", "").replace(";", "").split()
    name = parts[1]
    valves[name] = { "name": name,
                     "rate": 0,
                     "outgoing": parts[9:],
                     "closed_name": "",
                     "open_name": "",
                     "is_open": False
                    }
    if int(parts[4].split("=")[1]) > 0:
        open_name = "X{}".format(name)
        valves[open_name] = { "name": open_name,
                              "rate": int(parts[4].split("=")[1]),
                              "outgoing": parts[9:],
                              "is_open": True,
                              "open_name": open_name
                             }
        valves[name]["outgoing"].append(open_name)
        valves[name]["open_name"] = open_name
        valves[open_name]["closed_name"] = name

names = sorted(valves.keys())
to_consider = [ name for name in names if valves[name]["open_name"] != "" and valves[name]["is_open"]]
print(to_consider)

grid = [ [0] * len(names) for i in range(len(names)) ]
for first in range(len(names)):
    for second in range(len(names)):
        if names[second] in valves[names[first]]["outgoing"]:
            grid[first][second] = 1

#for row in grid:
#    print(",".join([ str(x) for x in row ]))

dist_matrix = shortest_path(np.array(grid), directed=True, return_predecessors=False)

#print(dist_matrix)

## total_minutes = 30
## minutes_passed = 0
## 
## max_score = 0
## max_path = None
## 
## # 0 - minutes passed
## # 1 - score
## # 2 - path - me
## 
## to_check = set()
## to_check.add((0, 0, "AA"))
## count = 0
## 
## while to_check:
##     count += 1
##     if count % 10000 == 0:
##         print(count, max_score, max_path)
##     state = to_check.pop()
##     minutes_passed = state[0]
##     score = state[1]
##     my_path = state[2].split("|")
##     minutes_left = total_minutes - minutes_passed
##     if score > max_score:
##         max_score = score
##         max_path = my_path
##     for valve in to_consider:
##         if valve in my_path:
##             continue
##         distance = dist_matrix[names.index(my_path[-1])][names.index(valve)]
##         if minutes_left < distance + 1:
##             continue
##         new_score = score + ( minutes_left - distance ) * valves[valve]["rate"]
##         to_check.add((minutes_passed + distance,
##                       new_score,
##                       state[2] + "|" + valve))
## print(max_score)
## print(max_path)

total_minutes = 26
minutes_passed = 0

max_score = 0
max_path = None
max_path_elephant = None

# 0 - my minutes passed
# 1 - elephant minutes passed
# 2 - score
# 3 - path - me
# 4 - path - elephant

to_check = set()
to_check.add((0, 0, 0, "AA", "AA"))
count = 0

while to_check:
    count += 1
    if count % 10000 == 0:
        print(count, max_score, max_path, max_path_elephant)
        distance = 0
        for i in range(len(max_path) - 1):
            d = dist_matrix[names.index(max_path[i])][names.index(max_path[i+1])]
            distance += d
            print(max_path[i], max_path[i+1], d, distance, valves[max_path[i+1]]["rate"])
    state = to_check.pop()
    minutes_passed = state[0]
    elephant_minutes_passed = state[1]
    score = state[2]
    my_path = state[3].split("|")
    my_minutes_left = total_minutes - minutes_passed
    elephant_path = state[4].split("|")
    elephant_minutes_left = total_minutes - elephant_minutes_passed
    if score > max_score:
        max_score = score
        max_path = my_path
        max_path_elephant = elephant_path
    for my_valve in to_consider:
        if my_valve in my_path or my_valve in elephant_path:
            continue
        my_distance = dist_matrix[names.index(my_path[-1])][names.index(my_valve)]
        if my_minutes_left < my_distance + 1:
            continue
        # check with elephant not moving
        new_score = score + ( my_minutes_left - my_distance ) * valves[my_valve]["rate"]
        to_check.add((minutes_passed + my_distance,
                      elephant_minutes_passed,
                      new_score,
                      state[3] + "|" + my_valve,
                      state[4]))
        for elephant_valve in to_consider:
            if elephant_valve in my_path or elephant_valve in elephant_path:
                continue
            if my_valve == elephant_valve:
                continue
            elephant_distance = dist_matrix[names.index(elephant_path[-1])][names.index(elephant_valve)]
            if elephant_minutes_left < elephant_distance + 1:
                continue
            new_score = score + ( my_minutes_left - my_distance ) * valves[my_valve]["rate"] + ( elephant_minutes_left - elephant_distance ) * valves[elephant_valve]["rate"]
            to_check.add((minutes_passed + my_distance,
                          elephant_minutes_passed + elephant_distance,
                          new_score,
                          state[3] + "|" + my_valve,
                          state[4] + "|" + elephant_valve))
            # check with me not moving
            new_score = score + ( elephant_minutes_left - elephant_distance ) * valves[elephant_valve]["rate"]
            to_check.add((minutes_passed,
                          elephant_minutes_passed + elephant_distance,
                          new_score,
                          state[3],
                          state[4] + "|" + elephant_valve))
print(max_score)
print(max_path)
            #  
#  minutes_left = 30
#  path = ["AA"]
#  while minutes_left > 0:
#      current_index = names.index(path[-1])
#      max_potential = 0
#      max_potential_target = None
#      for target in range(i, len(names)):
#          if not names[target].startswith("X"):
#              continue
#          potential = ((minutes_left - 1) - dist_matrix[current_index][target]) * valves[names[target]]["rate"]
#          if potential > max_potential:
#              max_potential 
#  potentials = []
#  
#  sys.exit()
#  
#  def all_open(paths):
#      global opened_names
#      if opened_names.difference(set(paths)):
#          # one or more valves with positive flow haven't been opened
#          return False
#      return True
#  
#  # 0 - minutes passed
#  # 1 - score
#  # 2 - path - me
#  # 3 - path - elephant
#  
#  to_check = set()
#  to_check.add((0, 0, "AA", "AA"))
#  count = 1
#  while to_check:
#  #    if count % 100 == 0:
#  #        sys.exit()
#      count += 1
#      if count % 100000 == 0:
#          print(count, max_score)
#          paths = max_path.split("_")
#          paths[0] = paths[0].split("|")
#          paths[1] = paths[1].split("|")
#          for i in range(len(paths[0])):
#              print("After minute", i, paths[0][i], paths[1][i])
#      state = to_check.pop()
#  #    print(state)
#      my_path = state[2].split("|")
#      elephant_path = state[3].split("|")
#      combined_path = my_path + elephant_path
#      if state[0] == total_minutes or all_open(combined_path):
#          if state[1] > max_score:
#              max_score = state[1]
#              max_path = state[2] + "_" + state[3]
#      else:
#          # find out the most recent valve opening per path
#          my_most_recent_opened = None
#          for i in range(1, len(my_path) - 1):
#              if "X" + my_path[i-1] == my_path[i]:
#                  my_most_recent_opened = my_path[i]
#          elephant_most_recent_opened = None
#          for i in range(1, len(elephant_path) - 1):
#              if "X" + elephant_path[i-1] == elephant_path[i]:
#                  elephant_most_recent_opened = elephant_path[i]
#  
#          for my_outgoing in valves[my_path[-1]]["outgoing"]:
#              for elephant_outgoing in valves[elephant_path[-1]]["outgoing"]:
#                  # "convert" already opened valves
#                  if valves[my_outgoing]["open_name"] and valves[my_outgoing]["open_name"] in combined_path:
#                      my_outgoing = valves[my_outgoing]["open_name"]
#                  if valves[elephant_outgoing]["open_name"] and valves[elephant_outgoing]["open_name"] in combined_path:
#                      elephant_outgoing = valves[elephant_outgoing]["open_name"]
#  
#                  # if elephant and person are at the same valve, let's divide up the work
#                  if my_path[-1] == elephant_path[-1]:
#                      if elephant_outgoing > my_outgoing:
#                          continue
#                      if elephant_outgoing == my_outgoing and "X" + elephant_path[-1] == elephant_outgoing:
#                          # no need for both to open the same valve at the same time
#                          continue
#  
#                  # if one is going to a valve being opened by the other...
#                  if my_outgoing == "X" + elephant_outgoing:
#                      # I am opening the valve that elephant is going to
#                      elephant_outgoing = my_outgoing
#                  elif "X" + my_outgoing == elephant_outgoing:
#                      # I am going to the valve that elephant is opening
#                      my_outgoing = elephant_outgoing
#  
#                  if my_most_recent_opened and my_outgoing.startswith("X") and my_outgoing == my_most_recent_opened:
#                      # don't go to an already opened valve unless we have opened up something else in the meantime
#                      continue
#                  if elephant_most_recent_opened and elephant_outgoing.startswith("X") and elephant_outgoing == elephant_most_recent_opened:
#                      # don't go to an already opened valve unless we have opened up something else in the meantime
#                      continue
#  
#                  # Avoid loops for me
#                  last_visit = -1
#                  for i in range(len(my_path) - 1, -1, -1):
#                      if my_path[i] == my_outgoing:
#                          last_visit = i
#                          break
#                  if last_visit >= 0:
#                      # we already visited this valve.  Let's make sure that we have opened something before going back
#                      found_open = False
#                      for j in range(last_visit + 1, len(my_path)):
#                          if my_path[j].startswith("X") and not [ y for y in range(last_visit) if my_path[y] == my_path[j] ]:
#                              found_open = True
#                      if not found_open:
#                          continue
#  
#                  # Avoid loops for elephant
#                  last_visit = -1
#                  for i in range(len(elephant_path) - 1, -1, -1):
#                      if elephant_path[i] == elephant_outgoing:
#                          last_visit = i
#                          break
#                  if last_visit >= 0:
#                      # we already visited this valve.  Let's make sure that we have opened something before going back
#                      found_open = False
#                      for j in range(last_visit, len(elephant_path) - 1):
#                          if "X" + elephant_path[j] == elephant_path[j+1]:
#                              found_open = True
#                      if not found_open:
#                          continue
#  
#                  new_flow = state[1]
#                  if my_path[-1] == valves[my_outgoing]["closed_name"]:
#                      new_flow += (total_minutes - (state[0]+1)) * valves[my_outgoing]["rate"]
#                  if elephant_path[-1] == valves[elephant_outgoing]["closed_name"]:
#                      new_flow += (total_minutes - (state[0]+1)) * valves[elephant_outgoing]["rate"]
#  
#                  to_check.add((state[0] + 1,                 # add one minute
#                                new_flow,                     # additional flow from the current valve
#                                state[2] + "|" + my_outgoing, # my path
#                                state[3] + "|" + elephant_outgoing)) # elephant path
#  
#  print(max_score)
#  print(max_path)
#  
