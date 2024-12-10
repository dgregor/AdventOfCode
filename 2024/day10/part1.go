package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

type Cell struct {
	x int
	y int
	value int
}

func get_neighbors(board [][]Cell, cell Cell) []Cell {
	neighbors := make([]Cell, 0)
	if cell.x > 0 {
		neighbors = append(neighbors, Cell{ x: cell.x - 1, y: cell.y, value: board[cell.y][cell.x - 1].value } )
	}
	if cell.x < len(board[0]) - 1 {
		neighbors = append(neighbors, Cell{ x: cell.x + 1, y: cell.y, value: board[cell.y][cell.x + 1].value } )
	}
	if cell.y > 0 {
		neighbors = append(neighbors, Cell{ x: cell.x, y: cell.y - 1, value: board[cell.y - 1][cell.x].value } )
	}
	if cell.y < len(board) - 1 {
		neighbors = append(neighbors, Cell{ x: cell.x, y: cell.y + 1, value: board[cell.y + 1][cell.x].value } )
	}
	return neighbors
}
		
func main() {

	trails := make([][]Cell, 0)
	board := make([][]Cell, 0)

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
		this_line := []byte(text_line)
		row_num := len(board)
		board = append(board, make([]Cell, 0))
		for i, v := range this_line {
			int_v, _ := strconv.Atoi(string(v))
			this_cell := Cell{ x: i, y: row_num, value: int_v }
			board[row_num] = append(board[row_num], this_cell)
			if int_v == 0 {
				trails = append(trails, make([]Cell, 1))
				trails[len(trails) - 1][0] = this_cell
			}
		}
    }

    readFile.Close()

	changed := true
	for changed {
		changed = false
		tmp_trails := make([][]Cell, 0)
		for _, trail := range trails {
			for _, neighbor := range get_neighbors(board, trail[len(trail) - 1]) {
				if board[neighbor.y][neighbor.x].value == len(trail) {
					new_trail := make([]Cell, len(trail) + 1)
					for i, v := range trail {
						new_trail[i] = v
					}
					new_trail[len(trail)] = neighbor
					tmp_trails = append(tmp_trails, new_trail)
					changed = true
				}
			}
		}
		if changed {
			trails = tmp_trails
		}
	}
	unique := make(map[Cell]map[Cell]bool)
	for _, trail := range trails {
		_, ok := unique[trail[0]]
		if ! ok {
			unique[trail[0]] = make(map[Cell]bool)
		}
		unique[trail[0]][trail[len(trail) - 1]] = true
	}
	count := 0
	for _, v := range unique {
		count += len(v)
	}
	fmt.Println(count)
	
}
