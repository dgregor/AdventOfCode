package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

func process_prices(prices []int, mappings map[int]map[int]map[int]map[int]int) {
	these_mappings := make(map[int]map[int]map[int]map[int]int)
	for i := range len(prices) {
		if i > 4 {
			a := prices[i-3] - prices[i-4]
			b := prices[i-2] - prices[i-3]
			c := prices[i-1] - prices[i-2]
			d := prices[i] - prices[i-1]
			_, ok := these_mappings[a]
			if ! ok {
				these_mappings[a] = make(map[int]map[int]map[int]int)
			}
			_, ok = these_mappings[a][b]
			if ! ok {
				these_mappings[a][b] = make(map[int]map[int]int)
			}
			_, ok = these_mappings[a][b][c]
			if ! ok {
				these_mappings[a][b][c] = make(map[int]int)
			}
			_, ok = these_mappings[a][b][c][d]
			if ! ok {
				these_mappings[a][b][c][d] = prices[i]
			}
		}
	}
	for a, _ := range these_mappings {
		for b, _ := range these_mappings[a] {
			for c, _ := range these_mappings[a][b] {
				for d, _ := range these_mappings[a][b][c] {
					_, ok := mappings[a]
					if ! ok {
						mappings[a] = make(map[int]map[int]map[int]int)
					}
					_, ok = mappings[a][b]
					if ! ok {
						mappings[a][b] = make(map[int]map[int]int)
					}
					_, ok = mappings[a][b][c]
					if ! ok {
						mappings[a][b][c] = make(map[int]int)
					}
					_, ok = mappings[a][b][c][d]
					if ! ok {
						mappings[a][b][c][d] = 0
					}
					mappings[a][b][c][d] += these_mappings[a][b][c][d]
				}
			}
		}
	}
}

func get_prices(start int64, iterations int) []int {
	prices := make([]int, iterations)
	for i := range iterations {
		start = ( start ^ ( start * 64 ) ) % 16777216
		start = ( ( start / 32 ) ^ start ) % 16777216
		start = ( ( start * 2048 ) ^ start ) % 16777216
		prices[i] = int(start % 10)
	}
	return prices
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

	mappings := make(map[int]map[int]map[int]map[int]int)

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		number, _ := strconv.Atoi(text_line)
		prices := get_prices(int64(number), 2000)
		process_prices(prices, mappings)
	}
    readFile.Close()

	most := 0
	for a, _ := range mappings {
		for b, _ := range mappings[a] {
			for c, _ := range mappings[a][b] {
				for d, _ := range mappings[a][b][c] {
					if mappings[a][b][c][d] > most {
						most = mappings[a][b][c][d]
					}
				}
			}
		}
	}
	fmt.Println(most)
}
