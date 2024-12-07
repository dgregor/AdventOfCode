package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
	"strings"
)

type Equation struct {
	total int
	inputs []int
}

func test_equation(equation Equation) bool {
	num_inputs := len(equation.inputs)
	if num_inputs == 1 {
		return equation.total == equation.inputs[0]
	}
	add_inputs := make([]int, len(equation.inputs) - 1)
	add_inputs[0] = equation.inputs[0] + equation.inputs[1]
	if len(equation.inputs) > 2 {
		for i, v := range equation.inputs[2:] {
			add_inputs[i + 1] = v
		}
	}
	if test_equation(Equation { total: equation.total, inputs: add_inputs }) {
		return true
	}
	mul_inputs := make([]int, len(equation.inputs) - 1)
	mul_inputs[0] = equation.inputs[0] * equation.inputs[1]
	if len(equation.inputs) > 2 {
		for i, v := range equation.inputs[2:] {
			mul_inputs[i + 1] = v
		}
	}
	if test_equation(Equation { total: equation.total, inputs: mul_inputs }) {
		return true
	}
	concat_inputs := make([]int, len(equation.inputs) - 1)
	first := strconv.Itoa(equation.inputs[0])
	second := strconv.Itoa(equation.inputs[1])
	concat_inputs[0], _ = strconv.Atoi(first + second)
	if len(equation.inputs) > 2 {
		for i, v := range equation.inputs[2:] {
			concat_inputs[i + 1] = v
		}
	}
	return test_equation(Equation { total: equation.total, inputs: concat_inputs })
}

func main() {

	var equations []Equation

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
		parts := strings.Split(text_line, ":")
		text_inputs := strings.Split(parts[1], " ")
		num_inputs := make([]int, 0)
		for _, v := range text_inputs {
			num, _ := strconv.Atoi(v)
			if num > 0 {
				num_inputs = append(num_inputs, num)
			}
		}
		total, _ := strconv.Atoi(parts[0])
		equations = append(equations, Equation { total: total, inputs: num_inputs })
    }

    readFile.Close()

	var total int = 0
	for _, equation := range equations {
		if test_equation(equation) {
			total = total + equation.total
		}
	}
	fmt.Println(total)
}
