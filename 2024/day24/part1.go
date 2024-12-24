package main

import (
	"bufio"
    "fmt"
	"math"
    "os"
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
	

		
func main() {

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
			rules[parts[4]] = Rule {
				first: parts[0],
					second: parts[2],
					operation: parts[1],
					result: parts[4],
				}
		}
    }

    readFile.Close()
	score := float64(0)
	for wire, _ := range rules {
		if wire[0:1] == "z" {
			wire_num := get_wire_number(wire)
			wire_val := get_wire_val(wire, wires, rules)
			score += float64(wire_val) * ( math.Pow(2, float64(wire_num) ))
		}
	}
	fmt.Printf("%.0f\n", score)
}
