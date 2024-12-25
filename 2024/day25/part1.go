package main

import (
	"bufio"
    "fmt"
    "os"
)

type Key struct {
	lengths []int
}

type Lock struct {
	lengths []int
}

func main() {


    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	start := true
	is_lock := true
	this_one := make([]int, 5)
	keys := make([]Key, 0)
	locks := make([]Lock, 0)
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		if start {
			if text_line[0] == '#' {
				is_lock = true
			} else {
				is_lock = false
			}
			start = false
			this_one = make([]int, 5)
		}
		if text_line == "" {
			start = true
			if is_lock {
				locks = append(locks, Lock{lengths: this_one})
			} else {
				keys = append(keys, Key{lengths: this_one})
			}
		} else {
			for i := range 5 {
				if text_line[i] == '#' {
					this_one[i]++
				}
			}
		}
    }
	if is_lock {
		locks = append(locks, Lock{lengths: this_one})
	} else {
		keys = append(keys, Key{lengths: this_one})
	}

    readFile.Close()
	fit := 0
	for _, key := range keys {
		for _, lock := range locks {
			is_good := true
			for i := range 5 {
				if key.lengths[i] + lock.lengths[i] > 7 {
					is_good = false
					break
				}
			}
			if is_good {
				fit++
			}
		}
	}
	fmt.Println(fit)
				
}
