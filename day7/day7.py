from functools import total_ordering

ORDERING = "AKQJT98765432"

def is_five_of_a_kind(hand, jokers=False):
    if len(set(hand.cards)) == 1:
        return True
    if jokers:
        non_jokers = set(hand.cards).difference(set(["J"]))
        if len(non_jokers) == 1:
            return True
    return False

def is_four_of_a_kind(hand, jokers=False):
    seen = {}
    for card in hand.cards:
        seen.setdefault(card, 0)
        seen[card] += 1
    for value in seen.values():
        if value == 4:
            return True
    if jokers:
        num_jokers = hand.cards.count("J")
        non_jokers = [ card for card in hand.cards if card != "J" ]
        seen = {}
        for card in non_jokers:
            seen.setdefault(card, 0)
            seen[card] += 1
        for value in seen.values():
            if value + num_jokers == 4:
                return True
    return False

def is_full_house(hand, jokers=False):
    seen = {}
    for card in hand.cards:
        seen.setdefault(card, 0)
        seen[card] += 1
    if len(seen) == 2:
        if is_four_of_a_kind(hand):
            return False
        return True
    if jokers:
        num_jokers = hand.cards.count("J")
        if num_jokers != 1:
            return False
        non_jokers = [ card for card in hand.cards if card != "J" ]
        seen = {}
        for card in non_jokers:
            seen.setdefault(card, 0)
            seen[card] += 1
        for value in seen.values():
            if value != 2:
                return False
        return True
    return False

def is_three_of_a_kind(hand, jokers=False):
    seen = {}
    for card in hand.cards:
        seen.setdefault(card, 0)
        seen[card] += 1
    for value in seen.values():
        if value == 3:
            return True
    if jokers:
        num_jokers = hand.cards.count("J")
        non_jokers = [ card for card in hand.cards if card != "J" ]
        seen = {}
        for card in non_jokers:
            seen.setdefault(card, 0)
            seen[card] += 1
        for value in seen.values():
            if value + num_jokers == 3:
                return True
    return False

def is_two_pair(hand, jokers=False):
    seen = {}
    for card in hand.cards:
        seen.setdefault(card, 0)
        seen[card] += 1
    count = 0
    for value in seen.values():
        if value == 2:
            count += 1
    if count == 2:
        return True
    return False

def is_one_pair(hand, jokers=False):
    seen = {}
    for card in hand.cards:
        seen.setdefault(card, 0)
        seen[card] += 1
    for value in seen.values():
        if value == 2:
            return True
    if jokers:
        num_jokers = hand.cards.count("J")
        non_jokers = [ card for card in hand.cards if card != "J" ]
        seen = {}
        for card in non_jokers:
            seen.setdefault(card, 0)
            seen[card] += 1
        for value in seen.values():
            if value + num_jokers == 2:
                return True
    return False

@total_ordering
class hand(object):
    def __init__(self, cards, bid, jokers=False):
        assert(len(cards) == 5)
        self.cards = cards
        self.bid = int(bid)

        self.rank = None
        if is_five_of_a_kind(self, jokers):
            self.rank = 100000
        elif is_four_of_a_kind(self, jokers):
            self.rank = 10000
        elif is_full_house(self, jokers):
            self.rank = 1000
        elif is_three_of_a_kind(self, jokers):
            self.rank = 100
        elif is_two_pair(self, jokers):
            self.rank = 10
        elif is_one_pair(self, jokers):
            self.rank = 1
        else:
            self.rank = 0

    def __eq__(self, other):
        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return(False)
        return(True)

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        elif self.rank < other.rank:
            return False
        else:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return ( ORDERING.index(self.cards[i]) < ORDERING.index(other.cards[i]) )
        return(False)

hands = []
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    hands.append(hand(line.split()[0], line.split()[1]))

hands.sort()

score = 0
for i in range(len(hands)):
    score += (i + 1) * hands[i].bid

print("Advent of Code, Day 6, Part 1")
print(score)

ORDERING = "AKQT98765432J"

hands = []
lines = open('input', 'r').readlines()
for line in lines:
    line = line.strip()
    hands.append(hand(line.split()[0], line.split()[1], jokers=True))

hands.sort()

score = 0
for i in range(len(hands)):
    score += (i + 1) * hands[i].bid

print("Advent of Code, Day 6, Part 2")
print(score)
