package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
	"strings"
)

func swap_first(pages []string, rules map[string]map[string]bool) bool {
	for i, x := range pages {
		for j, y := range pages[:i] {
			if rules[x][y] {
				pages[i] = y
				pages[j] = x
				return true
			}
		}
	}
	return false
}

func is_good(pages []string, rules map[string]map[string]bool) bool {
	good := true
	for i, x := range pages {
		for _, y := range pages[:i] {
			if rules[x][y] {
				good = false
				break
			}
			if ! good {
				break
			}
		}
	}
	return good
}

func main() {

	rules := make(map[string]map[string]bool)

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	var printings []string
	var done_with_rules bool

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		if text_line == "" {
			done_with_rules = true
		} else if done_with_rules {
			printings = append(printings, text_line)
		} else {
			parts := strings.Split(text_line, "|")
			_, exists := rules[parts[0]]
			if ! exists {
				rules[parts[0]] = make(map[string]bool)
			}
			rules[parts[0]][parts[1]] = true
		}
    }

    readFile.Close()

	var total int
	for _, printing := range printings {
		pages := strings.Split(printing, ",")
		good := is_good(pages, rules)
		if good {
			continue
		}
		for swap_first(pages, rules) {
			continue
		}
		middle, _ := strconv.Atoi(pages[len(pages) / 2])
		total = total + middle
	}
	fmt.Println(total)
}
