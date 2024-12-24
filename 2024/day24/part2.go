package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
	"strconv"
	"strings"
)

type Rule struct {
	first string
	second string
	operation string
	result string
}

func get_wire_number (wire string) int {
	number, _ := strconv.Atoi(wire[1:])
	return number
}

func get_wire_val(wire string, wires map[string]int, rules map[string]Rule) int {
	wire_val, ok := wires[wire]
	if ok {
		return wire_val
	}
	first, ok := wires[rules[wire].first]
	if ! ok {
		first = get_wire_val(rules[wire].first, wires, rules)
	}
	second, ok := wires[rules[wire].second]
	if ! ok {
		second = get_wire_val(rules[wire].second, wires, rules)
	}
	if rules[wire].operation == "AND" {
		if ( first == 1 ) && ( second == 1 ) {
			wires[wire] = 1
		} else {
			wires[wire] = 0
		}
	} else if rules[wire].operation == "OR" {
		if ( first == 1 ) || ( second == 1 ) {
			wires[wire] = 1
		} else {
			wires[wire] = 0
		}
	} else if rules[wire].operation == "XOR" {
		if first != second {
			wires[wire] = 1
		} else {
			wires[wire] = 0
		}
	}
	return wires[wire]
}

func rule_string(rule Rule) string {
	return "( " + rule.first + " " + rule.operation + " " + rule.second + " )"
}

func wire_expansion (wire string, rules map[string]Rule) string {
	if wire[0:1] == "x" || wire[0:1] == "y" {
		return wire
	}
	first := wire_expansion(rules[wire].first, rules)
	second := wire_expansion(rules[wire].second, rules)
	if first > second {
		return "( " + first + " " + rules[wire].operation + " " + second + " )"
	} else {
		return "( " + second + " " + rules[wire].operation + " " + first + " )"
	}
}

func print_rules (rules map[string]Rule) {
	keys := make([]string, 0, len(rules))
    for k := range rules{
        keys = append(keys, k)
    }
    sort.Strings(keys)
	for _, wire := range keys {
		fmt.Println(wire, "<-", wire_expansion(wire, rules))
		fmt.Println(wire, "<-", rules[wire].first, rules[wire].operation, rules[wire].second)
	}
}
	


func build_up_rule(start int) string {
	// ( ( y01 AND x01 ) OR ( ( y01 XOR x01 ) AND ( y00 AND x00 ) ) )
	if start == 0 {
		return "( y00 AND x00 )"
	}
	i_str := strconv.Itoa(start)
	if start < 10 {
		i_str = "0" + i_str
	}
	return "( ( y" + i_str + " AND x" + i_str + " ) OR ( ( y" + i_str + " XOR x" + i_str + " ) AND " + build_up_rule(start - 1) + " ) )"
}

func find_rule(first string, second string, operation string, rules map[string]Rule) Rule {
	for _, rule := range rules {
		if rule.operation == operation {
			if ( rule.first == first && rule.second == second ) || ( rule.first == second && rule.second == first ) {
				return rule
			}
		}
	}
	return Rule{ first: "", second: "", operation: "", result: "XXX" }
}

func main() {

	results_by_expansion := make(map[string]string)
	rules_by_expansion := make(map[string]Rule)
	rules := make(map[string]Rule)
	wires := make(map[string]int)
	populating_wires := true

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		if text_line == "" {
			populating_wires = false
			continue
		} else if populating_wires {
			parts := strings.Split(text_line, ": ")
			if parts[1] == "0" {
				wires[parts[0]] = 0
			} else {
				wires[parts[0]] = 1
			}
		} else {
			parts := strings.Split(text_line, " ")
			if parts[0] < parts[2] {
				rules[parts[4]] = Rule {
					first: parts[0],
						second: parts[2],
						operation: parts[1],
						result: parts[4],
					}
			} else {
				rules[parts[4]] = Rule {
					first: parts[2],
						second: parts[0],
						operation: parts[1],
						result: parts[4],
					}
			}
		}
    }
	for result, rule := range rules {
		rules_by_expansion[wire_expansion(result, rules)] = rule
		results_by_expansion[wire_expansion(result, rules)] = rule.result
	}
	keys := make([]string, 0, len(rules_by_expansion))
    for k := range rules_by_expansion{
        keys = append(keys, k)
    }
    sort.Strings(keys)

    readFile.Close()

	swapped := make([]string, 0)
	for i := range 45 {
		if i == 0 {
			continue
		}
		i_str := strconv.Itoa(i)
		if i < 10 {
			i_str = "0" + i_str
		}
		wire := "z" + i_str
		if rules[wire].operation != "XOR" {
			// x06 XOR y06 -> jgw
			// z02 <- ( ( y02 XOR x02 ) XOR ( ( y01 AND x01 ) OR ( ( y01 XOR x01 ) AND ( y00 AND x00 ) ) ) )
			// z02 <- A XOR B
			first_part := rules_by_expansion["( y" + i_str + " XOR x" + i_str + " )"]
			second_part := rules_by_expansion[build_up_rule(i - 1)]
			swap_rule := find_rule(first_part.result, second_part.result, "XOR", rules)
			swap_result := swap_rule.result
			swapped = append(swapped, wire)
			swapped = append(swapped, swap_result)
			swap_rule.result = wire
			wire_rule := rules[wire]
			wire_rule.result = swap_result
			rules[wire] = swap_rule
			rules[swap_result] = wire_rule
			for result, rule := range rules {
				rules_by_expansion[wire_expansion(result, rules)] = rule
			}
		} else {
			first_part_str := "( y" + i_str + " XOR x" + i_str + " )"
			if wire_expansion(rules[wire].first, rules) == first_part_str {
				if wire_expansion(rules[wire].second, rules) == build_up_rule(i - 1) {
					continue
				}
			} else if wire_expansion(rules[wire].second, rules) == first_part_str {
				if wire_expansion(rules[wire].first, rules) == build_up_rule(i - 1) {
					continue
				}
			} else {
				// first_part_str doesn't match
				correct_first_part := rules_by_expansion[first_part_str]
				to_swap := rules[wire].first
				if wire_expansion(rules[wire].first, rules) == build_up_rule(i - 1) {
					to_swap = rules[wire].second
				}
				swapped = append(swapped, to_swap)
				swapped = append(swapped, correct_first_part.result)
				tmp_rule := rules[to_swap]
				tmp_result := correct_first_part.result
				correct_first_part.result = to_swap
				rules[to_swap] = correct_first_part

				tmp_rule.result = tmp_result
				rules[tmp_result] = tmp_rule

				for result, rule := range rules {
					rules_by_expansion[wire_expansion(result, rules)] = rule
				}
			}
		}
	}
	sort.Strings(swapped)
	fmt.Println(strings.Join(swapped, ","))
}
