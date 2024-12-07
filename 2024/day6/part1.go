package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
	"strings"
)

func main() {

	var board []string
	seen := make(map[string]bool)

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	var guard_x int
	var guard_y int
	guard_direction := 0 // north

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	row_num := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		board = append(board, text_line)
		index := strings.Index(text_line, "^")
		if index > -1 {
			guard_x = index
			guard_y = row_num
		}
		row_num = row_num + 1
    }

    readFile.Close()

	for true {
		seen[strconv.Itoa(guard_x)  + "," + strconv.Itoa(guard_y)] = true
		if guard_direction == 0 {
			if guard_y == 0 {
				break
			}
			if board[guard_y - 1][guard_x:guard_x + 1] == "#" {
				guard_direction = 1
			} else {
				guard_y = guard_y - 1
			}
		} else if guard_direction == 1 {
			if guard_x == len(board[0]) - 1 {
				break
			}
			if board[guard_y][guard_x + 1:guard_x + 2] == "#" {
				guard_direction = 2
			} else {
				guard_x = guard_x + 1
			}
		} else if guard_direction == 2 {
			if guard_y == len(board) - 1 {
				break
			}
			if board[guard_y + 1][guard_x:guard_x + 1] == "#" {
				guard_direction = 3
			} else {
				guard_y = guard_y + 1
			}
		} else if guard_direction == 3 {
			if guard_x == 0 {
				break
			}
			if board[guard_y][guard_x - 1:guard_x] == "#" {
				guard_direction = 0
			} else {
				guard_x = guard_x - 1
			}
		}
	}
	fmt.Println(len(seen))
}
