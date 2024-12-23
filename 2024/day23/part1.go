package main

import (
	"bufio"
    "fmt"
    "os"
	"sort"
	"strings"
)

		
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

	count := 0
	keys := make([]string, 0, len(mappings))
    for k := range mappings{
        keys = append(keys, k)
    }
    sort.Strings(keys)

	for _, k1 := range keys {
		for _, k2 := range keys {
			if k2 <= k1 {
				continue
			}
			for _, k3 := range keys {
				if k3 <= k2 {
					continue
				}
				if mappings[k1][k2] && mappings[k2][k3] && mappings[k3][k1] {
					if k1[0] == 't' || k2[0] == 't' || k3[0] == 't' {
						count++
					}
				}
			}
		}
	}
	
	fmt.Println(count)
}
