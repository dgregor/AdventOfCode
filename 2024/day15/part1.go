package main

import (
	"bufio"
    "fmt"
    "os"
)

func print_board (board [][]rune) {
	for _, row := range board {
		fmt.Println(string(row))
	}
}

func find_first (board [][]rune, x int, y int, direction rune) int {
	if direction == '<' {
		for j := x - 1; j > 0; j-- {
			if board[y][j] == '.' {
				return j
			} else if board[y][j] == '#' {
				return -1
			}
		}
		return -1
	}
	if direction == '>' {
		for j := x + 1; j < len(board[0]) - 1; j++ {
			if board[y][j] == '.' {
				return j
			} else if board[y][j] == '#' {
				return -1
			}
		}
		return -1
	}
	if direction == '^' {
		for j := y - 1; j > 0; j-- {
			if board[j][x] == '.' {
				return j
			} else if board[j][x] == '#' {
				return -1
			}
		}
		return -1
	}
	if direction == 'v' {
		for j := y + 1; j < len(board) - 1; j++ {
			if board[j][x] == '.' {
				return j
			} else if board[j][x] == '#' {
				return -1
			}
		}
		return -1
	}
	return -2
}

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	board := make([][]rune, 0)
	var robot_x int
	var robot_y int
	
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	on_board := true
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		if text_line == "" {
			on_board = false
		} else if on_board {
			board = append(board, make([]rune, len(text_line)))
			for index, char := range text_line {
				board[len(board) - 1][index] = char
				if char == '@' {
					robot_x = index
					robot_y = len(board) - 1
				}
			}
		} else {
			for _, char := range text_line {
				first := find_first(board, robot_x, robot_y, char)
				board[robot_y][robot_x] = '.'
				if char == '<' {
					if first > -1 {
						if robot_x - first > 1 {
							board[robot_y][first] = 'O'
						}
						robot_x--
					}
				} else if char == '>' {
					if first > -1 {
						if first - robot_x > 1 {
							board[robot_y][first] = 'O'
						}
						robot_x++
					}
				} else if char == 'v' {
					if first > -1 {
						if first - robot_y > 1 {
							board[first][robot_x] = 'O'
						}
						robot_y++
					}
				} else if char == '^' {
					if first > -1 {
						if robot_y - first > 1 {
							board[first][robot_x] = 'O'
						}
						robot_y--
					}
				}
				board[robot_y][robot_x] = '@'
			}
		}
	}

	score := 0

	for y, row := range board {
		for x, char := range row {
			if char == 'O' {
				score += 100 * y + x
			}
		}
	}
	fmt.Println(score)

    readFile.Close()
}
