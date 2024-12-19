package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
	"strings"
)

type Towel struct {
	colors string
	len int
}

type Towels struct {
	colors []string
	starts map[string]int
}

type Design struct {
	pattern string
}

func num_combos(pattern string, towels Towels, combos map[string]int) int {
	past_result, ok := combos[pattern]
	if ok {
		return past_result
	}
	combo_count := 0
	starting_index := towels.starts[pattern[:1]]
	for _, color := range towels.colors[starting_index:] {
		if color == pattern {
			combo_count++
		} else if strings.HasPrefix(pattern, color) {
			combo_count += num_combos(pattern[len(color):], towels, combos)
		}
		if color[:1] != pattern[:1] {
			break
		}
	}
	combos[pattern] = combo_count
	return combo_count
}

func main() {

	towels := Towels{colors: make([]string, 0), starts: make(map[string]int)}
	combos := make(map[string]int)
	combos[""] = 1

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	fileScanner.Scan()
	text_line = fileScanner.Text()
	for _, text := range strings.Split(text_line, ",") {
		color := strings.ReplaceAll(text, " ", "")
		towels.colors = append(towels.colors, color)
		if len(color) == 1 {
			combos[color] = 1
		}
	}
	fileScanner.Scan()

	sort.Strings(towels.colors)
	for i, color := range towels.colors {
		first := color[:1]
		_, ok := towels.starts[first]
		if ! ok {
			towels.starts[first] = i
		}
	}
	count := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		these_combos := num_combos(text_line, towels, combos)
		count += these_combos
	}
    readFile.Close()

	fmt.Println(count)
}
