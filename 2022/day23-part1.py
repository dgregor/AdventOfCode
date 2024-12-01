import copy
import pprint
import sys

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

elf_locations = {}
elf_proposals = {}

def elf_at_location(x, y):
    return (x, y) in elf_locations

class Elf():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        elf_locations[(self.x, self.y)] = self

    def propose(self, elves, directions):
        self.propose_x = None
        self.propose_y = None
        has_elf = False
        for location in [ (self.x, self.y - 1),
                          (self.x + 1, self.y - 1),
                          (self.x + 1, self.y),
                          (self.x + 1, self.y + 1),
                          (self.x, self.y + 1),
                          (self.x - 1, self.y + 1),
                          (self.x - 1, self.y),
                          (self.x - 1, self.y - 1) ]:
            has_elf = elf_at_location(location[0], location[1])
            if has_elf:
                break
        if not has_elf:
            return
        for direction in directions:
            if direction == NORTH:
                empty = True
#                print("checking NORTH", self.x, self.y)
                for location in [ (self.x, self.y - 1),
                                  (self.x - 1, self.y - 1),
                                  (self.x + 1, self.y - 1)]:
                    if elf_at_location(location[0], location[1]):
                        empty = False
                        break
                if empty:
                    self.propose_x = self.x
                    self.propose_y = self.y - 1
#                    print("Moving to", self.propose_x, self.propose_y)
                    elf_proposals.setdefault((self.propose_x, self.propose_y), []).append(self)
                    return
            if direction == SOUTH:
                empty = True
#                print("checking SOUTH", self.x, self.y)
                for location in [ (self.x, self.y + 1),
                                  (self.x - 1, self.y + 1),
                                  (self.x + 1, self.y + 1)]:
                    if elf_at_location(location[0], location[1]):
                        empty = False
                        break
                if empty:
                    self.propose_x = self.x
                    self.propose_y = self.y + 1
#                    print("Moving to", self.propose_x, self.propose_y)
                    elf_proposals.setdefault((self.propose_x, self.propose_y), []).append(self)
                    return
            if direction == WEST:
                empty = True
#                print("checking WEST", self.x, self.y)
                for location in [ (self.x - 1, self.y),
                                  (self.x - 1, self.y + 1),
                                  (self.x - 1, self.y - 1)]:
                    if elf_at_location(location[0], location[1]):
                        empty = False
                        break
                if empty:
                    self.propose_x = self.x - 1
                    self.propose_y = self.y
#                    print("Moving to", self.propose_x, self.propose_y)
                    elf_proposals.setdefault((self.propose_x, self.propose_y), []).append(self)
                    return
            if direction == EAST:
                empty = True
#                print("checking EAST", self.x, self.y)
                for location in [ (self.x + 1, self.y),
                                  (self.x + 1, self.y + 1),
                                  (self.x + 1, self.y - 1)]:
                    if elf_at_location(location[0], location[1]):
                        empty = False
                        break
                if empty:
                    self.propose_x = self.x + 1
                    self.propose_y = self.y
#                    print("Moving to", self.propose_x, self.propose_y)
                    elf_proposals.setdefault((self.propose_x, self.propose_y), []).append(self)
                    return

    def move(self, elves):
        if self.propose_x is not None and self.propose_x is not None:
#            print("Looking to move ", self.x, self.y, "to", self.propose_x, self.propose_y)
            if len(elf_proposals[(self.propose_x, self.propose_y)]) > 1:
                if False:
                    print("Collision")
            else:
                if False:
                    print("Moving")
                del elf_locations[(self.x, self.y)]
                self.x = self.propose_x
                self.y = self.propose_y
                elf_locations[(self.x, self.y)] = self
                return True
        else:
            if False:
                print("No Proposal")

def print_map(elves):
    min_x = min([ elf.x for elf in elves ])
    max_x = max([ elf.x for elf in elves ])
    min_y = min([ elf.y for elf in elves ])
    max_y = max([ elf.y for elf in elves ])

    print()
    for y in range(min_y, max_y + 1):
        line = "".join( [ "#" if elf_at_location(x, y) else "." for x in range(min_x, max_x + 1) ] )
        print(line)
    print()

elves = []
lines = open('input-23', 'r').readlines()
y = 0
for line in lines:
    for x in range(len(line.strip())):
        if line[x] == "#":
            elves.append(Elf(x, y))
            print(x, y)
    y += 1

first = [NORTH, SOUTH, WEST, EAST]

print(first)
print_map(elves)
round = 1
while True:
    print("ROUND", round)
    for elf in elves:
        elf.propose(elves, first)
    any_move = False
    for elf in elves:
        if elf.move(elves):
            any_move = True
    elf_proposals = {}
    a = first.pop(0)
    first.append(a)
    if not any_move:
        break
    round += 1

print_map(elves)

min_x = min([ elf.x for elf in elves ])
max_x = max([ elf.x for elf in elves ])
min_y = min([ elf.y for elf in elves ])
max_y = max([ elf.y for elf in elves ])

print( ( (max_x - min_x + 1) * (max_y - min_y + 1) ) - len(elves) )
