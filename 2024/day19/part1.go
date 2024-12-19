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

func can_make(pattern string, towels Towels, tested map[string]bool) bool {
	if pattern == "" {
		return true
	}
	past_result, ok := tested[pattern]
	if ok {
		return past_result
	}
	starting_index := towels.starts[pattern[:1]]
	for _, color := range towels.colors[starting_index:] {
		if color == pattern {
			tested[pattern] = true
			return true
		}
		if strings.HasPrefix(pattern, color) {
			if can_make(pattern[len(color):], towels, tested) {
				tested[pattern] = true
				return true
			}
		}
		if color[:1] != pattern[:1] {
			break
		}
	}
	tested[pattern] = false
	return false
}

func main() {

	towels := Towels{colors: make([]string, 0), starts: make(map[string]int)}
	tested := make(map[string]bool)
	tested[""] = true

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
		tested[color] = true
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
		if can_make(text_line, towels, tested) {
			count++
		}
	}
    readFile.Close()

	fmt.Println(count)
}
