package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
	"strings"
)

func get_stones(num int) []int {
	stones := make([]int, 0)
	if num == 0 {
		stones = append(stones, 1)
	} else {
		i := strconv.Itoa(num)
		if len(i) % 2 == 0 {
			first, _ := strconv.Atoi(i[:len(i)/2])
			second, _ := strconv.Atoi(i[len(i)/2:])
			stones = append(stones, first)
			stones = append(stones, second)
		} else {
			stones = append(stones, num * 2024)
		}
	}
	return stones
}
		
func main() {

	//	RESULTS := make([]map[int]int, 26)
	TOCHECK := make([]map[int]int, 76)

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	TOCHECK[0] = make(map[int]int)
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		for _, v := range strings.Fields(text_line) {
			i, err := strconv.Atoi(v)
			if err != nil { panic(err) }
			TOCHECK[0][i] = 1
		}
    }

    readFile.Close()

	for round := 0; round < 75; round++ {
		TOCHECK[round + 1] = make(map[int]int)
		for stone_value, count := range TOCHECK[round] {
			for _, new_stone := range get_stones(stone_value) {
				TOCHECK[round + 1][new_stone] = TOCHECK[round + 1][new_stone] + count
			}
		}
	}

	count := 0
	for _, v := range TOCHECK[75] {
		count += v
	}
	fmt.Println(count)
	
}
