package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
)

type Move struct {
	x int
	y int
	in_direction int
}

func print_board (board [][]rune) {
	for _, row := range board {
		fmt.Println(string(row))
	}
}

func print_mins (mins map[Move]int) {
	for key, value := range mins {
		if value != MAX {
			fmt.Println(key.x, key.y, key.in_direction, value)
		}
	}
}

func get_neighbors (board [][]rune, x int, y int) []Move {
	neighbors := make([]Move, 0)
	if board[y-1][x] != '#' {
		neighbors = append(neighbors, Move{x: x, y: y-1, in_direction: 0})
	}
	if board[y+1][x] != '#' {
		neighbors = append(neighbors, Move{x: x, y: y+1, in_direction: 2})
	}
	if board[y][x-1] != '#' {
		neighbors = append(neighbors, Move{x: x-1, y: y, in_direction: 3})
	}
	if board[y][x+1] != '#' {
		neighbors = append(neighbors, Move{x: x+1, y: y, in_direction: 1})
	}
	return neighbors
}

func score (direction_a int, direction_b int) int {
	if direction_a == direction_b {
		return 0
	} else {
		return 1
	}
}

func opposite (direction int) int {
	if direction == 0 {
		return 2
	} else if direction == 1 {
		return 3
	} else if direction == 2 {
		return 0
	} else {
		return 1
	}
}

var MAX int = 1000000000

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	board := make([][]rune, 0)
	var start_x int
	var start_y int
	var end_x int
	var end_y int

	mins := make(map[Move]int)
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	to_check := make(map[int]map[Move]bool)

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		board = append(board, make([]rune, len(text_line)))
		y := len(board) - 1
		for x, char := range text_line {
			board[y][x] = char
		}
	}
    readFile.Close()

	for y, row := range board {
		for x, char := range row {
			if char == '#' {
				continue
			} else {
				for _, move := range get_neighbors (board, x, y) {
					mins[move] = MAX
				}
				if char == 'S' {
					start_x = x
					start_y = y
					//				mins[Move{x: start_x, y: start_y, in_direction: 0}] = 1000
					mins[Move{x: start_x, y: start_y, in_direction: 1}] = 0
					//				mins[Move{x: start_x, y: start_y, in_direction: 2}] = 1000
					//				mins[Move{x: start_x, y: start_y, in_direction: 3}] = 2000
					to_check[0] = make(map[Move]bool)
					to_check[0][Move{x: start_x, y: start_y, in_direction: 1}] = true
					//				to_check[1000] = make(map[Move]bool)
					//				to_check[1000][Move{x: start_x, y: start_y, in_direction: 0}] = true
					//				to_check[1000][Move{x: start_x, y: start_y, in_direction: 2}] = true
					//				to_check[2000] = make(map[Move]bool)
					//				to_check[2000][Move{x: start_x, y: start_y, in_direction: 3}] = true
				} else if char == 'E' {
					end_x = x
					end_y = y
				}
			}
		}
	}

	count := 0
	for len(to_check) > 0 && count < 10 {
		count--
		keys := make([]int, 0, len(to_check))
		for k := range to_check {
			keys = append(keys, k)
		}
		sort.Ints(keys)
		for _, k := range keys {
			for this_check := range to_check[k] {
				delete(to_check[k], this_check)
				for _, move := range get_neighbors(board, this_check.x, this_check.y) {
					if opposite(move.in_direction) != this_check.in_direction {
						new_score := k + 1 + score(move.in_direction, this_check.in_direction) * 1000
						if mins[move] > new_score {
							mins[move] = new_score
							_, ok := to_check[new_score]
							if ! ok {
								to_check[new_score] = make(map[Move]bool)
							}
							to_check[new_score][move] = true
						}
					}
				}
			}
			delete(to_check, k)
		}
	}
	best := -1
	for direction := range 4 {
		this_one := mins[Move{x: end_x, y: end_y, in_direction: direction}]
		if this_one > 0 {
			if best == -1 || this_one < best {
				best = this_one
			}
		}
	}
	fmt.Println(best)
}
