package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

type Gap struct {
	start int
	length int
}

func main() {

	places := make([]int, 0)
	gaps := make([]Gap, 0)

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
		this_line := []byte(text_line)
		for i, v := range this_line {
			int_v, _ := strconv.Atoi(string(v))
			if i % 2 == 0 {
				for j := 0; j < int_v; j++ {
					places = append(places, i/2)
				}
			} else {
				if int_v > 0 {
					gaps = append(gaps, Gap{ start: len(places), length: int_v })
					for j := 0; j < int_v; j++ {
						places = append(places, -1)
					}
				}
			}
		}
    }

    readFile.Close()

	this_id := -1
	this_length := 0
	for i := len(places) - 1; i >= 0; i-- {
		if this_id == -1 {
			this_length = 1
			this_id = places[i]
		} else if places[i] == this_id {
			this_length++
		} else {
			for j := 0; j < len(gaps); j++ {
				if gaps[j].start >= i {
					break
				}
				if gaps[j].length >= this_length {
					for k := 0; k < this_length; k++ {
						places[gaps[j].start + k] = this_id
					}
					for k := 0; k < this_length; k++ {
						places[i + k + 1] = -1
					}
					gaps[j] = Gap{start: gaps[j].start + this_length, length: gaps[j].length - this_length}
					break
				}
			}
			this_id = places[i]
			this_length = 1
		}
	}
	total := 0
	for i := 0; i < len(places) - 1; i++ {
		if places[i] > 0 {
			total += i * places[i]
		}
	}
	fmt.Println(total)
}
