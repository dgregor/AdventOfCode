package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
	"strings"
)

func get_sets(mappings map[string]map[string]bool, keys []string, current_set []string, size int) [][]string {
	rv := make([][]string, 0)
	if len(current_set) >= size {
		rv = append(rv, current_set)
		return rv
	}
	for _, key := range keys {
		if key <= current_set[len(current_set)-1] {
			continue
		}
		good := true
		for i := range len(current_set) {
			if ! mappings[current_set[i]][key] {
				good = false
				break
			}
		}
		if good {
			new_list := make([]string, len(current_set))
			for i, v := range current_set {
				new_list[i] = v
			}
			new_list = append(new_list, key)
			rv = append(rv, new_list)
		}
	}
	return rv
}

func main() {


	mappings := make(map[string]map[string]bool)

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		parts := strings.Split(text_line, "-")
		_, ok := mappings[parts[0]]
		if ! ok {
			mappings[parts[0]] = make(map[string]bool)
		}
		mappings[parts[0]][parts[1]] = true
		_, ok = mappings[parts[1]]
		if ! ok {
			mappings[parts[1]] = make(map[string]bool)
		}
		mappings[parts[1]][parts[0]] = true
    }
    readFile.Close()

	keys := make([]string, 0, len(mappings))
    for k := range mappings {
        keys = append(keys, k)
    }
    sort.Strings(keys)

	sets := make([][]string, 0)
	for _, k1 := range keys {
		for _, k2 := range keys {
			if k2 <= k1 {
				continue
			}
			if mappings[k1][k2] {
				this_set := make([]string, 2)
				this_set[0] = k1
				this_set[1] = k2
				sets = append(sets, this_set)
			}
		}
	}
	for i := 3; i < 30; i++ {
		new_set := make([][]string, 0)
		for _, this_set := range sets {
			matches := get_sets(mappings, keys, this_set, i)
			for _, match := range matches {
				new_set = append(new_set, match)
			}
		}
		if len(new_set) == 1 {
			fmt.Println(strings.Join(new_set[0], ","))
			break
		}
		sets = new_set
	}
	

}
