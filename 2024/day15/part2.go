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

func move_box (board [][]rune, x int, y int, direction rune) {
	if board[y][x] == '.' {
		return
	}
	if board[y][x] == ']' {
		if direction == '^' {
			if ! ( board[y-1][x-1] == '.' && board[y-1][x] == '.' ) {
				move_box(board, x - 1, y - 1, direction)
				move_box(board, x, y - 1, direction)
			}
			board[y-1][x-1] = '['
			board[y-1][x] = ']'
			board[y][x-1] = '.'
			board[y][x] = '.'
			return
		} else {
			if ! ( board[y+1][x-1] == '.' && board[y+1][x] == '.' ) {
				move_box(board, x - 1, y + 1, direction)
				move_box(board, x, y + 1, direction)
			}
			board[y+1][x-1] = '['
			board[y+1][x] = ']'
			board[y][x-1] = '.'
			board[y][x] = '.'
			return
		}
	} else if board[y][x] == '[' {
		if direction == '^' {
			if ! ( board[y-1][x] == '.' && board[y-1][x+1] == '.' ) {
				move_box(board, x, y - 1, direction)
				move_box(board, x + 1, y - 1, direction)
			}
			board[y-1][x] = '['
			board[y-1][x+1] = ']'
			board[y][x] = '.'
			board[y][x+1] = '.'
			return
		} else {
			if ! ( board[y+1][x] == '.' && board[y+1][x+1] == '.' ) {
				move_box(board, x, y + 1, direction)
				move_box(board, x + 1, y + 1, direction)
			}
			board[y+1][x] = '['
			board[y+1][x+1] = ']'
			board[y][x] = '.'
			board[y][x+1] = '.'
			return
		}
	}
	return
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
		j := y - 1
		if board[j][x] == '#' {
			return -1
		}
		if board[j][x] == '.' {
			return j
		}
		if board[j][x] == ']' {
			push_left := find_first(board, x - 1, j, direction)
			push_right := find_first(board, x, j, direction)
			if push_left == -1 || push_right == -1 {
				return -1
			}
			return max(push_left, push_right)
		}
		if board[j][x] == '[' {
			push_left := find_first(board, x, j, direction)
			push_right := find_first(board, x + 1, j, direction)
			if push_left == -1 || push_right == -1 {
				return -1
			}
			return max(push_left, push_right)
		}
		return -1
	}
	if direction == 'v' {
		j := y + 1
		if board[j][x] == '#' {
			return -1
		}
		if board[j][x] == '.' {
			return j
		}
		if board[j][x] == ']' {
			push_left := find_first(board, x - 1, j, direction)
			push_right := find_first(board, x, j, direction)
			if push_left == -1 || push_right == -1 {
				return -1
			}
			return min(push_left, push_right)
		}
		if board[j][x] == '[' {
			push_left := find_first(board, x, j, direction)
			push_right := find_first(board, x + 1, j, direction)
			if push_left == -1 || push_right == -1 {
				return -1
			}
			return min(push_left, push_right)
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
			board = append(board, make([]rune, len(text_line) * 2))
			for index, char := range text_line {
				if char == 'O' {
					board[len(board) - 1][index*2] = '['
					board[len(board) - 1][index*2 + 1] = ']'
				} else if char == '#' || char == '.' {
					board[len(board) - 1][index*2] = char
					board[len(board) - 1][index*2 + 1] = char
				} else {
					board[len(board) - 1][index*2] = '@'
					board[len(board) - 1][index*2 + 1] = '.'
					robot_x = index * 2
					robot_y = len(board) - 1
				}
			}
		} else {
			for _, char := range text_line {
				first := find_first(board, robot_x, robot_y, char)
				board[robot_y][robot_x] = '.'
				if char == '<' {
					if first > -1 {
						for i := first; i < robot_x - 1; i += 2 {
							board[robot_y][i] = '['
							board[robot_y][i+1] = ']'
						}
						robot_x--
					}
				} else if char == '>' {
					if first > -1 {
						for i := first; i > robot_x + 1; i -= 2 {
							board[robot_y][i] = ']'
							board[robot_y][i-1] = '['
						}
						robot_x++
					}
				} else if char == 'v' {
					if first > -1 {
						move_box (board, robot_x, robot_y + 1, char)
						robot_y++
					}
				} else if char == '^' {
					if first > -1 {
						move_box (board, robot_x, robot_y - 1, char)
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
			if char == '[' {
				score += 100 * y + x
			}
		}
	}
	fmt.Println(score)

    readFile.Close()
}
