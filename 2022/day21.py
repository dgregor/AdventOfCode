import copy
import pprint
import sys

class Human:
    def __init__(self):
        self.value = self

    def reduce(self):
        return self

    def __repr__(self):
        return "H"

class Monkey:
    def __init__(self, operation=None, first=None, second=None, value=None, name="tmp"):
        assert (value is not None) or (operation is not None and first is not None and second is not None)
        self.operation = operation
        self.first = first
        self.second = second
        self.value = value
        self.name = name
        self.reduced = False

        self._first_name = None
        self._second_name = None

        if self.value is not None:
            self.reduced = True
        else:
            try:
                self.first = int(self.first)
            except:
                self.first_name = self.first
                pass
            try:
                self.second = int(self.second)
            except:
                self.second_name = self.second
                pass

    def __repr__(self):
        if self.value:
            return "{} [{}]".format(self.value, self.name)
        else:
            #if self.is_number(self.first):
            #    if self._first_name:
            #        first = "{} ({})".format(self.first, self._first_name)
            #    else:
            #        first = "{}".format(self.first)
            #else:
            #    first = self.first.__repr__()
            #if self.is_number(self.second):
            #    second = "{} ({})".format(self.second, self._second_name)
            #else:
            #    second = self.second.__repr__()
            #return "( {} {} {} {} )".format(self.name, self.operation, first, second)
            return "( {} {} {} )".format(self.first, self.operation, self.second)

    def is_number(self, x):
        return isinstance(x, int) or isinstance(x, float)

    def reduce(self):
        if self.value:
            return
        if self.reduced:
            return

        self.first.reduce()
        if self.first.value is not None:
            self.first = self.first.value

        self.second.reduce()
        if self.second.value is not None:
            self.second = self.second.value

        # swap to keep numbers in the front
        if self.operation in ("+", "*"):
            if self.is_number(self.second):
                if not self.is_number(self.first):
                    temp = self.first
                    self.first = self.second
                    self.second = temp
                    temp = self._first_name
                    self._first_name = self._second_name
                    self._second_name = temp

        if self.is_number(self.first):
            if isinstance(self.second, Human):
                pass
            if self.is_number(self.second):
                if self.operation == "+":
                    self.value = self.first + self.second
                elif self.operation == "-":
                    self.value = self.first - self.second
                if self.operation == "*":
                    self.value = self.first * self.second
                if self.operation == "/":
                    self.value = self.first / self.second
            elif isinstance(self.second, Monkey):
                if self.operation == "+":
                    if self.second.operation == "+":
                        if self.is_number(self.second.first):
                            # A + (B + X) -> (A + B) + X
                            self.first = self.first + self.second.first
                            self.second = self.second.second
                            self.operation = "+"
                        elif self.is_number(self.second.second):
                            # A + (X + B) -> (A + B) + X
                            self.first = self.first + self.second.second
                            self.second = self.second.first
                            self.operation = "+"
                    elif self.second.operation == "-":
                        if self.is_number(self.second.first):
                            # A + (B - X) -> (A + B) - X
                            self.first = self.first + self.second.first
                            self.second = self.second.second
                            self.operation = "-"
                        elif self.is_number(self.second.second):
                            # A + (X - B) -> (A - B) + X
                            self.first = self.first - self.second.second
                            self.second = self.second.first
                            self.operation = "+"
                elif self.operation == "-":
                    if self.second.operation == "+":
                        if self.is_number(self.second.first):
                            # A - (B + X) -> (A - B) - X
                            self.first = self.first - self.second.first
                            self.second = self.second.second
                            self.operation = "-"
                        elif self.is_number(self.second.second):
                            # A - (X + B) -> (A - B) - X
                            self.first = self.first - self.second.second
                            self.second = self.second.first
                            self.operation = "-"
                    elif self.second.operation == "-":
                        if self.is_number(self.second.first):
                            # A - (B - X) -> (A - B) + X
                            self.first = self.first - self.second.first
                            self.second = self.second.second
                            self.operation = "+"
                        elif self.is_number(self.second.second):
                            # A - (X - B) -> (A + B) - X
                            self.first = self.first + self.second.first
                            self.second = self.second.first
                            self.operation = "-"
                elif self.operation == "*":
                    if self.second.operation == "+":
                        if self.is_number(self.second.first):
                            # A * (B + X) -> (A * B) + (A * X)
                            temp_value = self.first * self.second.first
                            self.second = Monkey(operation="*", first=self.first, second=self.second.second)
                            self.first = temp_value
                            self.operation = "+"
                        elif self.is_number(self.second.second):
                            # A * (X + B) -> (A * B) + (A * X)
                            temp_value = self.first * self.second.second
                            self.second = Monkey(operation="*", first=self.first, second=self.second.first)
                            self.first = temp_value
                            self.operation = "+"
                    elif self.second.operation == "-":
                        if self.is_number(self.second.first):
                            # A * (B - X) -> (A * B) - (A * X)
                            temp_value = self.first * self.second.first
                            self.second = Monkey(operation="*", first=self.first, second=self.second.second)
                            self.first = temp_value
                            self.operation = "-"
                        elif self.is_number(self.second.second):
                            # A * (X - B) -> (A * X) - (A * B)
                            temp_value = self.first * self.second.second
                            self.first = Monkey(operation="*", first=self.first, second=self.second.first)
                            self.second = temp_value
                            self.operation = "-"
                    elif self.second.operation == "*":
                        if self.is_number(self.second.first):
                            # A * (B * X) -> (A * B) * X
                            self.first = self.first * self.second.first
                            self.second = self.second.second
                            self.operation = "*"
                        elif self.is_number(self.second.second):
                            # A * (X * B) -> (A * B) * X
                            self.first = self.first * self.second.second
                            self.second = self.second.first
                            self.operation = "*"
                    elif self.second.operation == "/":
                        if self.is_number(self.second.first):
                            # A * (B / X) -> (A * B) / X
                            self.first = self.first * self.second.first
                            self.second = self.second.second
                            self.operation = "/"
                        elif self.is_number(self.second.second):
                            # A * (X / B) -> (A / B) * X
                            self.first = self.first / self.second.second
                            self.second = self.second.first
                            self.operation = "*"
                elif self.operation == "/":
                    if self.second.operation == "*":
                        if self.is_number(self.second.first):
                            # A / (B * X) -> (A / B) / X
                            self.first = self.first / self.second.first
                            self.second = self.second.second
                            self.operation = "/"
                        elif self.is_number(self.second.second):
                            # A / (X * B) -> (A / B) / X
                            self.first = self.first / self.second.second
                            self.second = self.second.first
                            self.operation = "/"
                    elif self.second.operation == "/":
                        if self.is_number(self.second.first):
                            # A / (B / X) -> (A / B) * X
                            self.first = self.first / self.second.first
                            self.second = self.second.second
                            self.operation = "*"
                        elif self.is_number(self.second.second):
                            # A / (X / B) -> (A * B) / X
                            self.first = self.first * self.second.second
                            self.second = self.second.first
                            self.operation = "/"
        elif self.is_number(self.second):
            if isinstance(self.first, Human):
                pass
            elif isinstance(self.first, Monkey):
                if self.operation == "-":
                    if self.first.operation == "+":
                        if self.is_number(self.first.first):
                            # (B + X) - A -> (B - A) + X
                            temp = self.first.first - self.second
                            self.second = self.first.second
                            self.first = temp
                            self.operation = "+"
                        elif self.is_number(self.first.second):
                            # (X + B) - A -> (B - A) + X
                            temp = self.first.second - self.second
                            self.second = self.first.first
                            self.first = temp
                            self.operation = "+"
                    elif self.first.operation == "-":
                        if self.is_number(self.first.first):
                            # (B - X) - A -> (B - A) - X
                            temp = self.first.first - self.second
                            self.second = self.first.second
                            self.first = temp
                            self.operation = "-"
                        elif self.is_number(self.first.second):
                            # (X - B) - A -> X - (A + B)
                            temp = self.first.second + self.second
                            self.first = self.first.first
                            self.second = temp
                            self.operation = "-"
                elif self.operation == "/":
                    #if self.first.operation == "+":
                    #    if self.is_number(self.first.first):
                    #        # (B + X) / A -> (B / A) + ( X / A )
                    #        temp = self.first.first / self.second
                    #        self.second = Monkey(operation="/", first=self.first.second, second=self.second)
                    #        self.first = temp
                    #        self.operation = "+"
                    #    elif self.is_number(self.first.second):
                    #        # (X + B) / A -> (B / A) + ( X / A )
                    #        temp = self.first.second / self.second
                    #        self.second = Monkey(operation="/", first=self.first.first, second=self.second)
                    #        self.first = temp
                    #        self.operation = "+"
                    #elif self.first.operation == "-":
                    #    if self.is_number(self.first.first):
                    #        # (B - X) / A -> (B / A) - ( X / A )
                    #        temp = self.first.first / self.second
                    #        self.second = Monkey(operation="/", first=self.first.second, second=self.second)
                    #        self.first = temp
                    #        self.operation = "-"
                    #    elif self.is_number(self.first.second):
                    #        # (X - B) / A -> (B / A) - ( X / A )
                    #        temp = self.first.second / self.second
                    #        self.second = Monkey(operation="/", first=self.first.first, second=self.second)
                    #        self.first = temp
                    #        self.operation = "-"
                    if self.first.operation == "*":
                        if self.is_number(self.first.first):
                            # (B * X) / A -> (B / A) * X
                            temp = self.first.first / self.second
                            self.second = self.first.second
                            self.first = temp
                            self.operation = "*"
                        elif self.is_number(self.first.second):
                            # (X * B) / A -> (B / A) * X
                            temp = self.first.second / self.second
                            self.second = self.first.first
                            self.first = temp
                            self.operation = "*"
                    elif self.first.operation == "/":
                        if self.is_number(self.first.first):
                            # (B / X) / A -> (B / A) / X
                            temp = self.first.first / self.second
                            self.second = self.first.second
                            self.first = temp
                            self.operation = "/"
                        elif self.is_number(self.first.second):
                            # (X / B) / A -> X / (A * B)
                            temp = self.first.second * self.second
                            self.first = self.first.first
                            self.second = temp
                            self.operation = "/"
            else:
                print("unknown", self.second)
        self.reduced = True

monkeys = {}
monkeys2 = {}

lines = open('input-21', 'r').readlines()
for line in lines:
    parts = line.strip().replace(":", "").split()
    if parts[0] == "humn":
        monkeys[parts[0]] = Human()
        monkeys2[parts[0]] = Human()
    elif len(parts) == 2:
        monkeys[parts[0]] = Monkey(value=int(parts[1]), name=parts[0])
        monkeys2[parts[0]] = Monkey(value=int(parts[1]), name=parts[0])
    else:
        monkeys[parts[0]] = Monkey(operation=parts[2], first=parts[1], second=parts[3], name=parts[0])
        monkeys2[parts[0]] = Monkey(operation=parts[2], first=parts[1], second=parts[3], name=parts[0])
for monkey_name, monkey in monkeys.items():
    if isinstance(monkey, Human):
        continue
    if isinstance(monkey.first, str):
        monkey.first = monkeys[monkey.first]
    if isinstance(monkey.second, str):
        monkey.second = monkeys[monkey.second]

#print(monkeys["lgvd"].__repr__())
#print(monkeys["lgvd"].reduce())
#print(monkeys["sjmn"].reduce())
monkeys["root"].first.reduce()
monkeys["root"].second.reduce()

def is_number(x):
    return isinstance(x, int) or isinstance(x, float)

if is_number(monkeys["root"].first):
    target = monkeys["root"].first.value
    source = monkeys["root"].second
else:
    target = monkeys["root"].second.value
    source = monkeys["root"].first

orig_target = target

def print_monkey2(monkey_name, monkeys, monkeys2, indent=0):
    if monkeys2[monkey_name].value is not None:
        print("{}{} {}".format(" " * indent, monkey_name, monkeys2[monkey_name].value))
    elif monkeys[monkey_name].value is not None:
        print("{}{} {} ( {} {} {} ) ( {} {} {} )".format(" " * indent, monkey_name, monkeys[monkey_name].value, monkeys[monkey_name].first, monkeys[monkey_name].operation, monkeys[monkey_name].second, monkeys2[monkey_name].first, monkeys2[monkey_name].operation, monkeys2[monkey_name].second))
        print_monkey2(monkeys2[monkey_name].first, monkeys, monkeys2, indent+2)
        print_monkey2(monkeys2[monkey_name].second, monkeys, monkeys2, indent+2)
    else:
        print("{}{} ( {} {} {} ) ( {} {} {} )".format(" " * indent, monkey_name, monkeys[monkey_name].first, monkeys[monkey_name].operation, monkeys[monkey_name].second, monkeys2[monkey_name].first, monkeys2[monkey_name].operation, monkeys2[monkey_name].second))
        print_monkey2(monkeys2[monkey_name].first, monkeys, monkeys2, indent+2)
        print_monkey2(monkeys2[monkey_name].second, monkeys, monkeys2, indent+2)

#print_monkey2("root", monkeys, monkeys2, indent=0)

while True:
    if isinstance(source, Human):
        break
    value = None
    next_monkey = None
    print()
    print(target, source)
    if is_number(source.first):
        value = source.first
        next_monkey = source.second
        if source.operation == "+":
            # T = V + H -> H = T - V
            target = target - value
        elif source.operation == "-":
            # T = V - H -> H = V - T
            target = value - target
        elif source.operation == "*":
            # T = V * H -> H = T / V
            target = target / value
        elif source.operation == "/":
            # T = V / H -> H = V / T
            target = value / target
        else:
            print("??", source)
    elif is_number(source.second):
        value = source.second
        next_monkey = source.first
        if source.operation == "+":
            # T = H + V -> H = T - V
            target = target - value
        elif source.operation == "-":
            # T = H - V -> H = T + V
            target = target + value
        elif source.operation == "*":
            # T = H * V -> H = T / V
            target = target / value
        elif source.operation == "/":
            # T = H / V -> H = T * V
            target = target * value
        else:
            print("??", source)
    else:
        print("???", source)
        sys.exit()
    source = next_monkey
print()
print(source, target)

#lgvd: * ljgn ptdq
#lgvd: * 2 ptdq
#lgvd: * 2 (- humn dvpt)
#lgvd: * 2 (- humn 3)
#lgvd: - (* 2 humn) 6
