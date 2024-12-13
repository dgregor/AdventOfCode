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

func calc(button_a Button, button_b Button, x int, y int) int{
	min_cost := -1
	var x_remaining int
	var y_remaining int
	for count := 100; count >= 0; count-- {
		if count == 0 {
			x_remaining = x
			y_remaining = y
		} else {
			x_remaining = x - (button_a.x * count)
			y_remaining = y - (button_a.y * count)
		}
		if x_remaining % button_b.x == 0 &&
			y_remaining % button_b.y == 0 &&
			x_remaining / button_b.x == y_remaining / button_b.y {
			b_count := x_remaining / button_b.x
			if b_count <= 100 {
				cost := ( 3 * count ) + b_count
				if min_cost == -1 || cost < min_cost {
					min_cost = cost
				}
			}
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

	total := 0
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
