import functools
import time
import pprint
import re
import sys

lines = open('input-15', 'r').readlines()

sensors = []

ROW = 2000000
MAX = 4000000
for line in lines:
    line = line.strip()
    parts = line.replace(",", "").replace(":", "").split()
    sensor = {
        "x": int(parts[2].split("=")[1]),
        "y": int(parts[3].split("=")[1]),
        "beacon_x": int(parts[8].split("=")[1]),
        "beacon_y": int(parts[9].split("=")[1]),
        }
    sensor["beacon_distance"] = abs(sensor["x"] - sensor["beacon_x"]) + abs(sensor["y"] - sensor["beacon_y"])
    sensors.append(sensor)

def check_row(row):
    global sensors
    no_beacon_ranges = []
    for sensor in sensors:
        y_distance = abs(row - sensor["y"])
        x_distance = sensor["beacon_distance"] - y_distance
        if x_distance >= 0:
            no_beacon = [max(0, sensor["x"] - x_distance), min(MAX, sensor["x"] + x_distance)]
            no_beacon_ranges.append(no_beacon)
    no_beacon_ranges.sort()
    if no_beacon_ranges[0][0] != 0:
        print("XXX", no_beacon_ranges)
        sys.exit(0)
    covered_start = no_beacon_ranges[0][0]
    covered_end = no_beacon_ranges[0][1]
    if len(no_beacon_ranges) > 1:
        for beacon_range in no_beacon_ranges[1:]:
            if beacon_range[0] > covered_end:
                print((covered_end + 1) * MAX + row)
                print(row, "ZZZ", covered_start, covered_end, no_beacon_ranges)
                sys.exit()
            else:
                covered_end = max(beacon_range[1], covered_end)
    if covered_end != MAX:
        print("YYY", no_beacon_ranges)
        sys.exit(0)

for row in range(0, MAX + 1):
    check_row(row)

