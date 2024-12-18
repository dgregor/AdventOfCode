package main

import (
	"bufio"
    "fmt"
	"math"
    "os"
	"strconv"
	"strings"
)

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
	text_line = fileScanner.Text()
	register_a, _ := strconv.Atoi(strings.Fields(text_line)[2])

    fileScanner.Scan()
	text_line = fileScanner.Text()
	register_b, _ := strconv.Atoi(strings.Fields(text_line)[2])

    fileScanner.Scan()
	text_line = fileScanner.Text()
	register_c, _ := strconv.Atoi(strings.Fields(text_line)[2])

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

	instruction_pointer := 0
	output := ""
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
			if output == "" {
				output = strconv.Itoa(combo % 8)
			} else {
				output += ","
				output += strconv.Itoa(combo % 8)
			}
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
	fmt.Println(output)
}
