package main

import (
	"bufio"
    "fmt"
    "os"
	"regexp"
	"strconv"
)

type Button struct {
	x int
	y int
}

type Prize struct {
	x int
	y int
}

func calc(button_a Button, button_b Button, x int, y int) int64{
	min_cost := int64(-1)
	a_delta := button_a.x - button_a.y
	b_delta := button_b.x - button_b.y
	if a_delta == 0 {
		// to check later
		return min_cost
	} else if b_delta == 0 {
		// to check later
		return min_cost
	}
	b_coeff := int64((b_delta * button_a.x) - (a_delta * button_b.x))
	target := int64(( (x - y) * button_a.x ) - ( x * a_delta ))
	if target % b_coeff == 0 {
		num_b := target / b_coeff
		num_a := ( int64(x) - (int64(num_b) * int64(button_b.x)) ) / int64(button_a.x)
		min_cost = (3 * num_a) + num_b
		if int64(button_a.x)*num_a + int64(button_b.x)*num_b != int64(x) {
			fmt.Println("THIS SHOULDN'T HAPPEN", a_delta, b_delta, b_coeff, target)
		}
		if int64(button_a.y)*num_a + int64(button_b.y)*num_b != int64(y) {
			fmt.Println("THIS SHOULDN'T HAPPEN")
		}
	}
	return min_cost
}
		
func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string
	re_button := regexp.MustCompile(`X\+([0-9]+), Y\+([0-9]+)`)
	re_prize := regexp.MustCompile(`Prize: X=([0-9]+), Y=([0-9]+)`)

	total := int64(0)
	state := 0
	var button_a Button
	var button_b Button
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		if state % 4 == 0 {
			match := re_button.FindStringSubmatch(text_line)
			x, _ := strconv.Atoi(match[1])
			y, _ := strconv.Atoi(match[2])
			button_a = Button { x: x, y: y }
		} else if state % 4 == 1 {
			match := re_button.FindStringSubmatch(text_line)
			x, _ := strconv.Atoi(match[1])
			y, _ := strconv.Atoi(match[2])
			button_b = Button { x: x, y: y }
		} else if state % 4 == 2 {
			match := re_prize.FindStringSubmatch(text_line)
			x, _ := strconv.Atoi(match[1])
			y, _ := strconv.Atoi(match[2])
			if true {
				x += 10000000000000
				y += 10000000000000
			}
			cost := calc(button_a, button_b, x, y)
			if cost > -1 {
				total += cost
			}
		}

		state++
	}

    readFile.Close()
	fmt.Println(total)
}
