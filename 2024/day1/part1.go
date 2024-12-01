package main

import (
    "bufio"
    "fmt"
    "os"
	"sort"
	"strings"
	"strconv"
)

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var list_one []int
	var list_two []int
	var text_line string

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		i, err := strconv.Atoi(strings.Fields(text_line)[0])
		if err != nil { panic(err) }
		list_one = append(list_one, i)
		i, err = strconv.Atoi(strings.Fields(text_line)[1])
		if err != nil { panic(err) }
		list_two = append(list_two, i)
    }

    readFile.Close()

	sort.Ints(list_one)
	sort.Ints(list_two)
	
	var diff int
	diff = 0
	for i, v := range list_one {
		d := v - list_two[i]
		if d < 0 {
			d = -d
		}
		diff += d
	}
	fmt.Println(diff)
}
