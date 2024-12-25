package main

import (
	"bufio"
    "fmt"
	"math"
    "os"
	"slices"
	"strconv"
)

type Button struct {
	letter rune
	x int
	y int
	neighbors []rune
}

func is_closer(first rune, neighbor rune, target rune, buttons map[rune]Button) bool {
	if ( math.Abs(float64(buttons[first].x) - float64(buttons[target].x)) + math.Abs(float64(buttons[first].y) - float64(buttons[target].y)) ) >
		( math.Abs(float64(buttons[neighbor].x) - float64(buttons[target].x)) + math.Abs(float64(buttons[neighbor].y) - float64(buttons[target].y)) ) {
		return true
	}
	return false
}

func get_direction(first rune, second rune, buttons map[rune]Button) rune {
	if buttons[first].x == buttons[second].x {
		if buttons[first].y < buttons[second].y {
			return('v')
		} else {
			return('^')
		}
	} else if buttons[first].x < buttons[second].x {
		return('>')
	} else {
		return ('<')
	}
}
	

func get_strings(runes [][]rune) [][]string {
	rv := make([][]string, len(runes))
	for i, c := range runes {
		rv[i] = make([]string, len(c))
		for j, d := range runes[i] {
			rv[i][j] = string(d)
		}
	}
	return rv
}

func get_move(first rune, second rune, buttons map[rune]Button) [][]rune {
	rv := make([][]rune, 0)
	if first == second {
		rv = append(rv, make([]rune, 1))
		rv[0][0] = 'A'
	} else if slices.Contains(buttons[first].neighbors, second) {
		rv = append(rv, make([]rune, 2))
		rv[0][0] = get_direction(first, second, buttons)
		rv[0][1] = 'A'
	} else {
		for _, neighbor := range buttons[first].neighbors {
			if is_closer(first, neighbor, second, buttons) {
				for _, path := range get_move(neighbor, second, buttons) {
					rv = append(rv, make([]rune, 0))
					rv[len(rv)-1] = append(rv[len(rv)-1], get_direction(first, neighbor, buttons))
					for _, letter := range path {
						rv[len(rv)-1] = append(rv[len(rv)-1], letter)
					}
				}
			}
		}
	}
	if len(rv) == 0 {
		fmt.Println("no move", first, second, buttons)
	}
	return rv
}
			
			
func get_combos(sequence []rune, buttons map[rune]Button) [][]rune {
	rv := make([][]rune, 0)
	if len(sequence) < 2 {
		return rv
	}
	if len(sequence) == 2 {
		return get_move(sequence[0], sequence[1], buttons)
	} else {
		for _, path := range get_move(sequence[0], sequence[1], buttons) {
			for _, rest := range get_combos(sequence[1:], buttons) {
				rv = append(rv, make([]rune, 0))
				for _, letter := range path {
					rv[len(rv)-1] = append(rv[len(rv)-1], letter)
				}
				for _, letter := range rest {
					rv[len(rv)-1] = append(rv[len(rv)-1], letter)
				}
			}
		}
	}
	return rv
}

func get_num(sequence []rune) int {
	number := ""
	for _, letter := range sequence {
		if number == "" && letter == '0' {
			continue
		}
		if letter == 'A' {
			continue
		}
		number += string(letter)
	}
	rv, _ := strconv.Atoi(number)
	return rv
}
	
func main() {

	buttons := make(map[rune]Button)
	buttons['A'] = Button{letter: 'A', x: 2, y: 3, neighbors: []rune{'0', '3'}}
	buttons['0'] = Button{letter: '0', x: 1, y: 3, neighbors: []rune{'A', '2'}}
	buttons['1'] = Button{letter: '1', x: 0, y: 2, neighbors: []rune{'2', '4'}}
	buttons['2'] = Button{letter: '2', x: 1, y: 2, neighbors: []rune{'0', '1', '3', '5'}}
	buttons['3'] = Button{letter: '3', x: 2, y: 2, neighbors: []rune{'A', '2', '6'}}
	buttons['4'] = Button{letter: '4', x: 0, y: 1, neighbors: []rune{'1', '5', '7'}}
	buttons['5'] = Button{letter: '5', x: 1, y: 1, neighbors: []rune{'2', '4', '6', '8'}}
	buttons['6'] = Button{letter: '6', x: 2, y: 1, neighbors: []rune{'3', '5', '9'}}
	buttons['7'] = Button{letter: '7', x: 0, y: 0, neighbors: []rune{'4', '8'}}
	buttons['8'] = Button{letter: '8', x: 1, y: 0, neighbors: []rune{'5', '7', '9'}}
	buttons['9'] = Button{letter: '9', x: 2, y: 0, neighbors: []rune{'6', '8'}}

	dir_buttons := make(map[rune]Button)
	dir_buttons['A'] = Button{letter: 'A', x: 2, y: 0, neighbors: []rune{'^', '>'}}
	dir_buttons['<'] = Button{letter: '<', x: 0, y: 1, neighbors: []rune{'v'}}
	dir_buttons['>'] = Button{letter: '>', x: 2, y: 1, neighbors: []rune{'v', 'A'}}
	dir_buttons['^'] = Button{letter: '^', x: 1, y: 0, neighbors: []rune{'v', 'A'}}
	dir_buttons['v'] = Button{letter: 'v', x: 1, y: 1, neighbors: []rune{'<', '^', '>'}}

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	score := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		text_line = "A" + text_line
		overall_shortest := ""
		for i := range len(text_line) - 1 {
			shortest := -1
			shortest_string := ""
			this_path := text_line[i:i+2]
			combos := get_combos([]rune(this_path), buttons)
			for _, combo := range combos {
				new_path := append([]rune{'A'}, combo...)
				new_combos := get_combos(new_path, dir_buttons)
				shortest_first := -1
				for _, new_combo := range new_combos {
					if shortest_first == -1 || len(new_combo) <= shortest {
						shortest_first = len(new_combo)
					}
					new_path_2 := append([]rune{'A'}, new_combo...)
					new_combos_2 := get_combos(new_path_2, dir_buttons)
					for _, this_combo := range new_combos_2 {
						if shortest == -1 || shortest > len(this_combo) {
							shortest = len(this_combo)
							shortest_string = string(this_combo)
						}
					}
				}
			}
			overall_shortest += shortest_string
		}
		score += len(overall_shortest) * get_num([]rune(text_line))
	}
    readFile.Close()
	fmt.Println(score)

}
