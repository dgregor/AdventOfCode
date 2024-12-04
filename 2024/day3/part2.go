package main

import (
    "fmt"
    "os"
	"regexp"
	"strconv"
	"strings"
)

func main() {

    filePath := os.Args[1]

	b, err := os.ReadFile(filePath)
    if err != nil {
        fmt.Print(err)
    }
	var total int
	on := true
	str := string(b)
	re := regexp.MustCompile(`(?:mul\(([0-9]{1,3}),([0-9]{1,3})\))|(?:do\(\))|(?:don't\(\))`)
	for _, v := range re.FindAllStringSubmatch(str, -1) {
		if strings.HasPrefix(v[0], "mul") {
			if on {
				first, _ := strconv.Atoi(v[1])
				second, _ := strconv.Atoi(v[2])
				total = total + ( first * second )
			}
		} else if v[0] == "do()" {
			on = true
		} else {
			on = false
		}
	}
	fmt.Println(total)
}
