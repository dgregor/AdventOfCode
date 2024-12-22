package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

func get_score(start int64, iterations int) int64 {
	for range iterations {
		start = ( start ^ ( start * 64 ) ) % 16777216
		start = ( ( start / 32 ) ^ start ) % 16777216
		start = ( ( start * 2048 ) ^ start ) % 16777216
	}
	return start
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

	score := int64(0)
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		number, _ := strconv.Atoi(text_line)
		score += get_score(int64(number), 2000)
	}
    readFile.Close()
	fmt.Println(score)
}
