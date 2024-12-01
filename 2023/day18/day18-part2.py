import sys

# 0 - Right
# 1 - Down
# 2 - Left
# 3 - Up

import pprint
print("Advent of Code, Day 18, Part 2")

current_coords = (0, 0)
dug_coords = { 'left': {},
               'right': {},
               'right-special': {},
               'vertical': []
               }

# vert coords are top to bottom
# left/right coords are left to right

border_total = 0
turns = []
edges = 0
lines = open("input", 'r').readlines()
for line in lines:
    line = line.strip()
    direction, count, color = line.split()
    count = int(color[2:-2], 16)
    direction = int(color[-2])
    turns.append((direction, count, color))
for turn_index in range(len(turns)):
    direction, count, color = turns[turn_index]
    border_total += count
    if direction in (3, "U"):
        new_coords = (current_coords[0], current_coords[1]+count)
        dug_coords['vertical'].append((current_coords[0], (new_coords[1], current_coords[1])))
    elif direction in (1, "D"):
        new_coords = (current_coords[0], current_coords[1]-count)
        dug_coords['vertical'].append((current_coords[0], (current_coords[1], new_coords[1])))
    elif direction in (0, "R"):
        new_coords = (current_coords[0]+count, current_coords[1])
        left = current_coords[0]
        right = new_coords[0]
        if turns[turn_index - 1][0] == 3:
            left += 1
        if turns[turn_index + 1][0] == 1:
            right -= 1
        dug_coords['right'].setdefault(current_coords[1], [])
        dug_coords['right'][current_coords[1]].append((left, right))
    elif direction in (2, "L"):
        new_coords = (current_coords[0]-count, current_coords[1])
        left = new_coords[0]
        right = current_coords[0]
        if turns[turn_index - 1][0] == 1:
            right -= 1
        if turns[turn_index + 1][0] == 3:
            left += 1
        dug_coords['left'].setdefault(current_coords[1], [])
        dug_coords['left'][current_coords[1]].append((left, right))
    edges += (new_coords[0] - current_coords[0]) * (new_coords[1] + current_coords[1])
    current_coords = new_coords

def get_ranges(baseline, against, start, end):
    ranges = []
    for segment_vert, segments in sorted(against.items(), reverse=True):
        if segment_vert >= baseline:
            # above, so skip
            continue
        for segment in sorted(segments):
            if len(ranges) > 0 and ranges[0][1][0] == start and ranges[-1][1][1] == end:
                all_contiguous = True
                for i in range(len(ranges) - 1):
                    assert ranges[i+1][1][0] - ranges[i][1][1] >= 1
                    if ranges[i+1][1][0] - ranges[i][1][1] != 1:
                        all_contiguous = False
                        break
                if all_contiguous:
                    return ranges
            segment_start = max(segment[0], start)
            segment_end = min(segment[1], end)
            if segment_end < start or segment_start > end:
                # segment doesn't overlap with overall
                continue
            if not ranges:
                ranges.append( (segment_vert, ( segment_start, segment_end) ) )
                continue
            # look for overlap
            # ranges are in order and contiguous.  this range must start at or to the left of segment.  and it must end at or after the beginning of the segment
            for range_index in range(len(ranges)):
                this_range = ranges[range_index]
                this_range_vert = this_range[0]
                this_range_start = this_range[1][0]
                this_range_end = this_range[1][1]
                # We are going top-down.  so, this range is "above" the segment.  We are looking down, so the range takes precedence
                if segment_start >= this_range_start and segment_end <= this_range_end:
                    # segment is "hidden"
                    break
                if segment_start < this_range_start:
                    ranges.insert(range_index, ( segment_vert, ( segment_start, min(segment_end, this_range_start - 1 ) ) ) )
                    break
                else:
                    # this segment ends to the right of the range.
                    segment_start = max(this_range_end + 1, segment_start)
                    if range_index < len(ranges) - 1:
                        next_start = ranges[range_index+1][1][0]
                        if next_start - this_range_end > 1 and next_start > segment_start:
                            ranges.insert(range_index + 1, ( segment_vert, ( segment_start, min(segment_end,  next_start - 1) ) ) )
                            break
                        else:
                            segment_start = max(this_range_end + 1, segment_start)
                    else:
                        ranges.insert(range_index + 1, ( segment_vert, ( segment_start, segment_end ) ) )
                        break
    return ranges

extra = 0
grand_total = 0
clockwise = True
if clockwise:
    top = dug_coords['right']
    bottom = dug_coords['left']
    all_bottom = dug_coords['left']
else:
    top = dug_coords['left']
    bottom = dug_coords['right']
for baseline, segments in sorted(top.items()):
    for segment in sorted(segments):
        total = 0
        ranges = get_ranges(baseline, all_bottom, start=segment[0], end=segment[1])
        for this_range in ranges:
            total += ( baseline - ( this_range[0] + 1 ) ) * ( this_range[1][1] - this_range[1][0] + 1 )
        grand_total += total

print(grand_total + border_total)
