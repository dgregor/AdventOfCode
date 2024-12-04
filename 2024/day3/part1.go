package main

import (
    "fmt"
    "os"
	"regexp"
	"strconv"
)

func main() {

    filePath := os.Args[1]

	b, err := os.ReadFile(filePath)
    if err != nil {
        fmt.Print(err)
    }
	var total int
	str := string(b)
	re := regexp.MustCompile(`mul\(([0-9]{1,3}),([0-9]{1,3})\)`)
	for _, v := range re.FindAllStringSubmatch(str, -1) {
		first, _ := strconv.Atoi(v[1])
		second, _ := strconv.Atoi(v[2])
		total = total + ( first * second )
	}
	fmt.Println(total)
}
