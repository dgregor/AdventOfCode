package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

type File struct {
	id int
	size int
}

func main() {

	files := make(map[int]File)
	free_spaces := make([]int, 0)
	places := make([]int, 0)

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
				files[i/2] = File{ id: i / 2, size: int_v }
				for j := 0; j < int_v; j++ {
					places = append(places, i/2)
				}
			} else {
				free_spaces = append(free_spaces, int_v)
				for j := 0; j < int_v; j++ {
					places = append(places, -1)
				}
			}
		}
    }

    readFile.Close()

	for i := len(places) - 1; i >= 0; i-- {
		if places[i] > 0 {
			for j := 0; j < i; j++ {
				if places[j] == -1 {
					places[j] = places[i]
					places[i] = -1
				}
			}
		}
	}
	total := 0
	for i := 0; i < len(places) - 1; i++ {
		if places[i] == -1 {
			break
		}
		total += i * places[i]
	}
	//	fmt.Println(files)
	//fmt.Println(free_spaces)
	//fmt.Println(places)
	fmt.Println(total)
}
