package main

import (
	"bufio"
    "fmt"
    "os"
)

func is_match_letter(x int, y int, letter string, lines []string) bool {
	if x >= 0 && x < len(lines[0]) {
		if y >= 0 && y < len(lines) {
			if lines[y][x:x+1] == letter {
				return true
			}
		}
	}
	return false
}

func is_match_word(coords [][]int, lines []string) bool {
	if ! is_match_letter(coords[0][0], coords[0][1], "X", lines) {
		return false
	}
	if ! is_match_letter(coords[1][0], coords[1][1], "M", lines) {
		return false
	}
	if ! is_match_letter(coords[2][0], coords[2][1], "A", lines) {
		return false
	}
	if ! is_match_letter(coords[3][0], coords[3][1], "S", lines) {
		return false
	}
	return true
}

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	var lines []string

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		lines = append(lines, text_line)
    }

    readFile.Close()

	var count int
	var coords [][]int

	for y, _ := range lines {
		for x, _ := range lines[y] {
			// right
			coords = [][]int{
				{x, y},
				{x + 1, y},
				{x + 2, y},
				{x + 3, y},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// down-right
			coords = [][]int{
				{x, y},
				{x + 1, y + 1},
				{x + 2, y + 2},
				{x + 3, y + 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// down
			coords = [][]int{
				{x, y},
				{x, y + 1},
				{x, y + 2},
				{x, y + 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// down-left
			coords = [][]int{
				{x, y},
				{x - 1, y + 1},
				{x - 2, y + 2},
				{x - 3, y + 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// left
			coords = [][]int{
				{x, y},
				{x - 1, y},
				{x - 2, y},
				{x - 3, y},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// up-left
			coords = [][]int{
				{x, y},
				{x - 1, y - 1},
				{x - 2, y - 2},
				{x - 3, y - 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// up
			coords = [][]int{
				{x, y},
				{x, y - 1},
				{x, y - 2},
				{x, y - 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
			// up-right
			coords = [][]int{
				{x, y},
				{x + 1, y - 1},
				{x + 2, y - 2},
				{x + 3, y - 3},
			}
			if is_match_word(coords, lines) {
				count = count + 1
			}
		}
	}
	fmt.Println(count)
	
}
