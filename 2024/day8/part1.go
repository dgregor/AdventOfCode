package main

import (
	"bufio"
    "fmt"
    "os"
)

type Antinode struct {
	x int
	y int
}

type Antenna struct {
	x int
	y int
}

func get_antinodes (antennas []Antenna, max_x int, max_y int) []Antinode {
	antinodes := make([]Antinode, 0)
	for i, first := range antennas {
		for j, second := range antennas {
			if i == j {
				continue
			}
			new_x := first.x - ( 2 * ( first.x - second.x ))
			new_y := first.y - ( 2 * ( first.y - second.y ))
			if new_x >= 0 && new_x <= max_x && new_y >= 0 && new_y <= max_y {
				antinodes = append(antinodes, Antinode{ x: new_x, y: new_y} )
			}
		}
	}
	return antinodes
}

func main() {

	antennas := make(map[byte][]Antenna)

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string

	var max_x int
	row := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		this_line := []byte(text_line)
		if max_x == 0 {
			max_x = len(this_line)
		}
		for this_x, v := range this_line {
			if v == '.' {
				continue
			}
			_, ok := antennas[v]
			if ! ok {
				antennas[v] = make([]Antenna, 0)
			}
			antennas[v] = append(antennas[v], Antenna{ x: this_x, y: row })
		}
		row = row + 1
    }

    readFile.Close()

	all_antinodes := make(map[Antinode]bool)
	for _, v := range antennas {
		these_antinodes := get_antinodes(v, max_x - 1, row - 1)
		for _, antinode := range these_antinodes {
			all_antinodes[antinode] = true
		}
	}

	fmt.Println(len(all_antinodes))
}
