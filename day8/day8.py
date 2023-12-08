import numpy

class node(object):
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

def get_distance(nodes, sequence, start, finish):
    seen = {}
    count = 0
    current_node = nodes[start]
    while current_node.name != finish:
        offset = count % len(sequence)
        seen.setdefault(offset, [])
        if current_node.name in seen[offset]:
            return -1
        else:
            seen[offset].append(current_node.name)
        direction = sequence[offset]
        if direction == "R":
            current_node = current_node.right
        else:
            current_node = current_node.left
        count += 1
    return count

def parse_file(filename):
    nodes = {}
    lines = open(filename, 'r').readlines()
    sequence = lines.pop(0).strip()
    lines.pop(0)
    for line in lines:
        line = line.strip().replace("(", "").replace(")", "").replace(",", "").replace("=", "")
        (name, left, right) = line.split()
        nodes[name] = node(name, left, right)
    for this_node in nodes.values():
        this_node.left = nodes[this_node.left]
        this_node.right = nodes[this_node.right]
    return sequence, nodes

sequence, nodes = parse_file("input")
print("Advent of Code, Day 8, Part 1")
print(get_distance(nodes, sequence, "AAA", "ZZZ"))

sequence, nodes = parse_file("input")
starting_nodes = [ this_node.name for this_node in nodes.values() if this_node.name[-1] == 'A' ]
ending_nodes = [ this_node.name for this_node in nodes.values() if this_node.name[-1] == 'Z' ]
steps = []
for start in starting_nodes:
    for end in ending_nodes:
        distance = get_distance(nodes, sequence, start, end)
        if distance >= 0:
            steps.append(distance)

print("Advent of Code, Day 8, Part 1")
print(numpy.lcm.reduce(steps))
