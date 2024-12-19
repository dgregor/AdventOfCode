package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
	"strconv"
	"strings"
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

//var WIDTH int = 9
//var HEIGHT int = 9
var WIDTH int = 73
var HEIGHT int = 73
var MAX int = 1000000000

func can_solve(bad []Cell, bytes int) bool {
	board := make([][]rune, 0)
	var start_x int = 1
	var start_y int = 1
	var end_x int = WIDTH - 2
	var end_y int = HEIGHT - 2
	to_check := make(map[int]map[Cell]bool)

	mins := make(map[Cell]int)
	
	board = append(board, make([]rune, WIDTH))
	for x := 0; x < WIDTH; x++ {
		board[0][x] = '#'
	}
	for y := 1; y < HEIGHT - 1; y++ {
		board = append(board, make([]rune, WIDTH))
		board[y][0] = '#'
		for x := range WIDTH - 2 {
			board[y][x+1] = '.'
			mins[Cell{x: x+1, y: y}] = MAX
		}
		board[y][WIDTH-1] = '#'
	}
	board = append(board, make([]rune, WIDTH))
	for x := 0; x < WIDTH; x++ {
		board[HEIGHT-1][x] = '#'
	}
	mins[Cell{x: start_x, y: start_y}] = 0
	to_check[0] = make(map[Cell]bool)
	to_check[0][Cell{x: start_x, y: start_y}] = true

	for i, cell := range bad {
		if i == bytes {
			break
		}
		board[cell.y+1][cell.x+1] = '#'
	}

	for len(to_check) > 0 {
		keys := make([]int, 0, len(to_check))
		for k := range to_check {
			keys = append(keys, k)
		}
		sort.Ints(keys)
		for _, k := range keys {
			for this_check := range to_check[k] {
				delete(to_check[k], this_check)
				for _, cell := range get_neighbors(board, this_check.x, this_check.y) {
					new_score := k + 1
					if mins[cell] > new_score {
						mins[cell] = new_score
						_, ok := to_check[new_score]
						if ! ok {
							to_check[new_score] = make(map[Cell]bool)
						}
						to_check[new_score][cell] = true
					}
				}
			}
			delete(to_check, k)
		}
	}
	if mins[Cell{x: end_x, y: end_y}] < MAX {
		return true
	}
	return false
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

	bad := make([]Cell, 0)
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		x, _ := strconv.Atoi(strings.Split(text_line, ",")[0])
		y, _ := strconv.Atoi(strings.Split(text_line, ",")[1])
		bad = append(bad, Cell{x: x, y: y})
	}
    readFile.Close()

	bad_count := 1024
	for true {
		if ! can_solve(bad, bad_count) {
			fmt.Println(bad_count, bad[bad_count-1])
			break
		}
		bad_count++
	}
}
