package main

import (
	"bufio"
    "fmt"
    "os"
)

var OBSTACLE byte = '#'
var EMPTY byte = '.'
var GUARD_START_X int
var GUARD_START_Y int

func solve_board (board [][]byte, x int, y int, direction int) (bool, map[int]map[int][]bool) {
	steps := make(map[int]map[int][]bool)
	for true {
		_, ok := steps[x]
		if ! ok {
			steps[x] = make(map[int][]bool)
		}
		_, ok = steps[x][y]
		if ! ok {
			steps[x][y] = make([]bool, 4)
		}
		if steps[x][y][direction] {
			// already been here.  it's a loop
			return false, steps
		} else {
			steps[x][y][direction] = true
		}
		if direction == 0 {
			tmp_y := y - 1
			if tmp_y < 0 {
				return true, steps
			}
			if board[tmp_y][x] == OBSTACLE {
				direction = 1
			} else {
				y = tmp_y
			}
		} else if direction == 1 {
			tmp_x := x + 1
			if tmp_x >= len(board[0]) {
				return true, steps
			}
			if board[y][tmp_x] == OBSTACLE {
				direction = 2
			} else {
				x = tmp_x
			}
		} else if direction == 2 {
			tmp_y := y + 1
			if tmp_y >= len(board) {
				return true, steps
			}
			if board[tmp_y][x] == OBSTACLE {
				direction = 3
			} else {
				y = tmp_y
			}
		}  else if direction == 3 {
			tmp_x := x - 1
			if tmp_x < 0 {
				return true, steps
			}
			if board[y][tmp_x] == OBSTACLE {
				direction = 0
			} else {
				x = tmp_x
			}
		}
	}
	return false, steps
}

func main() {

	var board [][]byte

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	row_num := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		board = append(board, []byte(text_line))
		for index, v := range []byte(text_line) {
			if v == '^' {
				GUARD_START_X = index
				GUARD_START_Y = row_num
			}
		}
		row_num = row_num + 1
    }

    readFile.Close()

	no_loop, steps := solve_board (board, GUARD_START_X, GUARD_START_Y, 0)

	var test_x int
	var test_y int
	var obstruction_count int = 0

	checked := make(map[int]map[int]bool)

	for x, _ := range steps {
		for y, _ := range steps[x] {
			for direction, _ := range steps[x][y] {
				if steps[x][y][direction] {
					if direction == 0 {
						test_x = x
						test_y = y - 1
					} else if direction == 1 {
						test_x = x + 1
						test_y = y
					} else if direction == 2 {
						test_x = x
						test_y = y + 1
					} else if direction == 3 {
						test_x = x - 1
						test_y = y
					}
					if ( test_x >= 0 && test_x < len(board[0]) && test_y >= 0 && test_y < len(board) ) {
						if board[test_y][test_x] != OBSTACLE {
							if ! ( test_x == GUARD_START_X && test_y == GUARD_START_Y ) {
								_, ok := checked[test_x]
								if ! ok {
									checked[test_x] = make(map[int]bool)
								}
								if checked[test_x][test_y] {
									continue
								} else {
									board[test_y][test_x] = OBSTACLE
									no_loop, _ = solve_board (board, GUARD_START_X, GUARD_START_Y, 0)
									if ! no_loop {
										obstruction_count = obstruction_count + 1
									}
									board[test_y][test_x] = EMPTY
									checked[test_x][test_y] = true
								}
							}
						}
					}
				}
			}
		}
	}
	fmt.Println(obstruction_count)
}
