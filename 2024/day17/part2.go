package main

import (
	"bufio"
    "fmt"
	"math"
    "os"
	"strconv"
	"strings"
)

func calc(instructions []int, register_a int, register_b int, register_c int) []int {
	instruction_pointer := 0
	output := make([]int, 0)
	for instruction_pointer < len(instructions) - 1 {
		operation := instructions[instruction_pointer]
		operand := instructions[instruction_pointer + 1]
		jumped := false
		combo := operand
		if operand == 4 {
			combo = register_a
		} else if operand == 5 {
			combo = register_b
		} else if operand == 6 {
			combo = register_c
		}
		if operation == 0 {
			register_a = register_a / int(math.Pow(2, float64(combo)))
		} else if operation == 1 {
			register_b = register_b ^ operand
		} else if operation == 2 {
			register_b = combo % 8
		} else if operation == 3 {
			if register_a != 0 {
				instruction_pointer = operand
				jumped = true
			}
		} else if operation == 4 {
			register_b = register_b ^ register_c
		} else if operation == 5 {
			output = append(output, combo % 8)
		} else if operation == 6 {
			register_b = register_a / int(math.Pow(2, float64(combo)))
		} else if operation == 7 {
			register_c = register_a / int(math.Pow(2, float64(combo)))
		}
		if ! jumped {
			instruction_pointer += 2
		}
		jumped = false
	}
	return output
}

func matches(instructions []int, match []int, starting int) []int {
	good := make([]int, 0)
	for i := range 8 {
		rv := calc(instructions, starting + i, 0, 0)
		is_good := true
		if len(rv) == len(match) {
			for j := range rv {
				if rv[j] != match[j] {
					is_good = false
					break
				}
			}
		} else {
			is_good = false
		}
		if is_good {
			good = append(good, starting + i)
		}
	}
	return good
}

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	var text_line string
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	
    fileScanner.Scan()
    fileScanner.Scan()
    fileScanner.Scan()
    fileScanner.Scan()
    fileScanner.Scan()
	text_line = fileScanner.Text()
	instructions := make([]int, 0)
	parts := strings.Split(strings.Fields(text_line)[1], ",")
	for _, part := range parts {
		instruction, _ := strconv.Atoi(part)
		instructions = append(instructions, instruction)
	}
    readFile.Close()

	to_check := make([]map[int]bool, len(instructions))
	for i := range len(instructions) {
		to_check[i] = make(map[int]bool)
	}
	for i := range 8 {
		rv := calc(instructions, i, 0, 0)
		if rv[0] == instructions[len(instructions) - 1] {
			to_check[len(instructions) - 1][i] = true
		}
	}
	for i := len(instructions)-2; i >= 0; i-- {
		for k, _ := range to_check[i+1] {
			for _, x := range matches(instructions, instructions[i:], k << 3) {
				to_check[i][x] = true
			}
		}
	}
	m := -1
	for k, _ := range to_check[0] {
		if m == -1 || m > k {
			m = k
		}
	}
	fmt.Println(m)
}
