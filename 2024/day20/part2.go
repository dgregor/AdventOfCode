package main

import (
	"bufio"
    "fmt"
	"math"
    "os"
)

type Cell struct {
	x int
	y int
}

type Skip struct {
	cell Cell
	distance int
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

func abs (num int) int {
	return int(math.Abs(float64(num)))
}

func get_skips (board [][]rune, x int, y int, max int) []Skip {
	skips := make([]Skip, 0)
	for delta_x := range max + 1 {
		if delta_x == 0 {
			continue
		}
		for delta_y := range max + 1 {
			if delta_y == 0 {
				continue
			}
			distance := delta_x + delta_y
			if distance <= max {
				if y >= delta_y && x >= delta_x && board[y - delta_y][x - delta_x] != '#' {
					skips = append(skips, Skip{cell: Cell{x: x - delta_x, y: y - delta_y}, distance: distance})
				}
				if y >= delta_y && x < len(board[0]) - delta_x && board[y - delta_y][x + delta_x] != '#' {
					skips = append(skips, Skip{cell: Cell{x: x + delta_x, y: y - delta_y}, distance: distance})
				}
				if y < len(board) - delta_y && x >= delta_x && board[y + delta_y][x - delta_x] != '#' {
					skips = append(skips, Skip{cell: Cell{x: x - delta_x, y: y + delta_y}, distance: distance})
				}
				if y < len(board) - delta_y && x < len(board) - delta_x && board[y + delta_y][x + delta_x] != '#' {
					skips = append(skips, Skip{cell: Cell{x: x + delta_x, y: y + delta_y}, distance: distance})
				}
			}
		}
	}
	for delta_x := range max + 1 {
		if delta_x == 0 {
			continue
		}
		delta_y := 0
		distance := delta_x + delta_y
		if x >= delta_x && board[y][x - delta_x] != '#' {
			skips = append(skips, Skip{cell: Cell{x: x - delta_x, y: y}, distance: distance})
		}
		if x < len(board[0]) - delta_x && board[y][x + delta_x] != '#' {
			skips = append(skips, Skip{cell: Cell{x: x + delta_x, y: y}, distance: distance})
		}
	}
	for delta_y := range max + 1 {
		if delta_y == 0 {
			continue
		}
		delta_x := 0
		distance := delta_x + delta_y
		if y >= delta_y && board[y - delta_y][x] != '#' {
			skips = append(skips, Skip{cell: Cell{x: x, y: y - delta_y}, distance: distance})
		}
		if y < len(board) - delta_y && board[y + delta_y][x] != '#' {
			skips = append(skips, Skip{cell: Cell{x: x, y: y + delta_y}, distance: distance})
		}
	}
	
	return skips
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
		for _, skip := range get_skips(board, this_cell.x, this_cell.y, 20) {
			if mins[this_cell] - ( mins[skip.cell] + skip.distance ) >= 100 {
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
