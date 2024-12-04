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

func is_match_word(x int, y int, word string, lines []string) bool {
	if ! is_match_letter(x, y, word[0:1], lines) {
		return false
	}
	if ! is_match_letter(x + 2, y, word[1:2], lines) {
		return false
	}
	if ! is_match_letter(x + 2, y + 2, word[2:3], lines) {
		return false
	}
	if ! is_match_letter(x, y + 2, word[3:4], lines) {
		return false
	}
	if ! is_match_letter(x + 1, y + 1, "A", lines) {
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

	for y, _ := range lines {
		for x, _ := range lines[y] {
			if is_match_word(x, y, "MMSS", lines) {
				count = count + 1
			}
			if is_match_word(x, y, "SMMS", lines) {
				count = count + 1
			}
			if is_match_word(x, y, "SSMM", lines) {
				count = count + 1
			}
			if is_match_word(x, y, "MSSM", lines) {
				count = count + 1
			}
		}
	}
	fmt.Println(count)
	
}
