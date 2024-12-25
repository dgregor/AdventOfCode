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
		new_rv := make([][]rune, 0)
		for _, path := range rv {
			dir_change := 0
			for i := range len(path) - 2 {
				if path[i] != path[i+1] {
					dir_change++
				}
			}
			if dir_change <= 1 {
				new_rv = append(new_rv, path)
			}
		}
		rv = new_rv
	}
	if len(rv) == 0 {
		fmt.Println("no move", string(first), string(second), buttons)
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

func expand(sequence []rune, cache map[string][]rune) []rune {
	rv := make([]rune, 0)
	for i := range len(sequence) - 1 {
		rv = append(rv, cache[string(sequence[i:i+2])]...)
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

	cache := make(map[string]string)
	cache["AA"] = "A"
	cache["A>"] = "vA"
	cache["A^"] = "<A"

	cache["^^"] = "A"
	cache["^A"] = ">A"
	cache["^<"] = "v<A"
	cache["^v"] = "vA"

	cache["<<"] = "A"
	cache["<v"] = ">A"
	cache["<^"] = ">^A"
	cache["<>"] = ">>A"

	cache["vv"] = "A"
	cache["v<"] = "<A"
	cache["v^"] = "^A"
	cache["v>"] = ">A"

	cache[">>"] = "A"
	cache[">A"] = "^A"
	cache[">v"] = "<A"
	cache["><"] = "<<A"

	cache_options := make(map[string][]string)
	cache_options["A<"] = make([]string, 0)
	cache_options["A<"] = append(cache_options["A<"], "v<<A" )
	cache_options["A<"] = append(cache_options["A<"], "<v<A" )

	cache_options["Av"] = make([]string, 0)
	cache_options["Av"] = append(cache_options["Av"], "v<A" )
	cache_options["Av"] = append(cache_options["Av"], "<vA" )

	cache_options["^>"] = make([]string, 0)
	cache_options["^>"] = append(cache_options["^>"], ">vA" )
	cache_options["^>"] = append(cache_options["^>"], "v>A" )
	
	cache_options[">^"] = make([]string, 0)
	cache_options[">^"] = append(cache_options[">^"], "<^A" )
	cache_options[">^"] = append(cache_options[">^"], "^<A" )
	
	cache_options["vA"] = make([]string, 0)
	cache_options["vA"] = append(cache_options["vA"], ">^A" )
	cache_options["vA"] = append(cache_options["vA"], "^>A" )
	
	cache_options["<A"] = make([]string, 0)
	cache_options["<A"] = append(cache_options["<A"], ">^>A" )
	cache_options["<A"] = append(cache_options["<A"], ">>^A" )
	
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
		total := 0
		for i := range len(text_line) - 1 {
			shortest := -1
			this_path := text_line[i:i+2]
			for _, first := range cache_options["A<"] {
				cache["A<"] = first
				for _, second := range cache_options["Av"] {
					cache["Av"] = second
					for _, third := range cache_options["^>"] {
						cache["^>"] = third
						for _, fourth := range cache_options[">^"] {
							cache[">^"] = fourth
							for _, fifth := range cache_options["vA"] {
								cache["vA"] = fifth
								for _, sixth := range cache_options["<A"] {
									cache["<A"] = sixth
									combos := get_combos([]rune(this_path), buttons)
									for _, combo := range combos {
										combo_string := "A" + string(combo)
										moves := make(map[string]int)
										for j := range len(combo_string) - 1 {
											this_move := combo_string[j:j+2]
											moves[cache[this_move]] += 1
										}
										for range 24 {
											new_moves := make(map[string]int)
											for key, value := range moves {
												move := "A" + key
												for k := range len(move) - 1 {
													this_move := move[k:k+2]
													new_moves[cache[this_move]] += value
												}
											}
											moves = new_moves
										}
										this_count := 0
										for k, v := range moves {
											this_count += v * len(k)
										}
										if shortest == -1 || shortest > this_count {
											shortest = this_count
										}
									}
								}
							}
						}
					}
				}
			}
			total += shortest
		}
		score += total * get_num([]rune(text_line))
	}
    readFile.Close()
	fmt.Println(score)

}
