package main

import (
	"bufio"
    "fmt"
    "os"
)

type Cell struct {
	x int
	y int
}

func print_board (board [][]rune) {
	for _, row := range board {
		fmt.Println(string(row))
	}
}

func print_mins (mins map[Cell]int) {
	for key, value := range mins {
		if value != MAX {
			fmt.Println(key.x, key.y, value)
		}
	}
}

func get_neighbors (board [][]rune, x int, y int) []Cell {
	neighbors := make([]Cell, 0)
	if board[y-1][x] != '#' {
		neighbors = append(neighbors, Cell{x: x, y: y-1})
	}
	if board[y+1][x] != '#' {
		neighbors = append(neighbors, Cell{x: x, y: y+1})
	}
	if board[y][x-1] != '#' {
		neighbors = append(neighbors, Cell{x: x-1, y: y})
	}
	if board[y][x+1] != '#' {
		neighbors = append(neighbors, Cell{x: x+1, y: y})
	}
	return neighbors
}

func get_skips (board [][]rune, x int, y int) []Cell {
	neighbors := make([]Cell, 0)
	if y >= 2 && board[y-1][x] == '#' && board[y-2][x] != '#' {
		neighbors = append(neighbors, Cell{x: x, y: y-2})
	}
	if y < len(board) - 2 && board[y+1][x] == '#' && board[y+2][x] != '#' {
		neighbors = append(neighbors, Cell{x: x, y: y+2})
	}
	if x >= 2 && board[y][x-1] == '#' && board[y][x-2] != '#' {
		neighbors = append(neighbors, Cell{x: x-2, y: y})
	}
	if x < len(board[0]) - 2 && board[y][x+1] == '#' && board[y][x+2] != '#' {
		neighbors = append(neighbors, Cell{x: x+2, y: y})
	}
	return neighbors
}

var MAX int = 1000000000

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	board := make([][]rune, 0)
	var end_x int
	var end_y int

	mins := make(map[Cell]int)
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	to_check := make(map[Cell]bool)

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
				for _, cell := range get_neighbors (board, x, y) {
					mins[cell] = MAX
				}
				if char == 'E' {
					end_x = x
					end_y = y
					mins[Cell{x: end_x, y: end_y}] = 0
					to_check = make(map[Cell]bool)
					to_check[Cell{x: end_x, y: end_y}] = true
				}
			}
		}
	}

	for len(to_check) > 0 {
		for this_check := range to_check {
			delete(to_check, this_check)
			for _, cell := range get_neighbors(board, this_check.x, this_check.y) {
				new_score := mins[this_check] + 1
				if mins[cell] > new_score {
					mins[cell] = new_score
					to_check[cell] = true
				}
			}
		}
	}
	this_cell := Cell{x: end_x, y: end_y}
	prev_cell := this_cell
	count := 0
	for true {
		for _, skip := range get_skips(board, this_cell.x, this_cell.y) {
			if mins[this_cell] - ( mins[skip] + 2 ) >= 100 {
				count++
			}
		}
		for _, cell := range get_neighbors(board, this_cell.x, this_cell.y) {
			if mins[cell] == mins[this_cell] + 1 {
				this_cell = cell
				break
			}
		}
		if this_cell == prev_cell {
			break
		} else {
			prev_cell = this_cell
		}
	}
	fmt.Println(count)
}
