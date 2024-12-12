package main

import (
	"bufio"
    "fmt"
    "os"
	"strconv"
)

type Region struct {
	id int
	plots []*Plot
}

type Plot struct {
	x int
	y int
	label byte
	region_id int
}

func print_board(board [][]*Plot) {
	for _, row := range board {
		this_row := ""
		for _, plot := range row {
			this_row += strconv.Itoa(plot.region_id) + string(plot.label)
		}
		fmt.Println(this_row)
	}
}

func get_neighbors(board [][]*Plot, plot Plot) []*Plot {
	neighbors := make([]*Plot, 0)
	if plot.x > 0 {
		neighbors = append(neighbors, board[plot.y][plot.x - 1])
	}
	if plot.x < len(board[0]) - 1 {
		neighbors = append(neighbors, board[plot.y][plot.x + 1])
	}
	if plot.y > 0 {
		neighbors = append(neighbors, board[plot.y - 1][plot.x])
	}
	if plot.y < len(board) - 1 {
		neighbors = append(neighbors, board[plot.y + 1][plot.x])
	}
	return neighbors
}

func explore_plot(board [][]*Plot, regions []Region, plot Plot) {
	to_check := make(map[Plot]bool)
	to_check[plot] = true
	var this_plot Plot
	for len(to_check) > 0 {
		for k := range to_check {
			this_plot = k
			break
		}
		delete(to_check, this_plot)
		for _, neighbor := range get_neighbors(board, this_plot) {
			if neighbor.label == plot.label && neighbor.region_id == -1 {
				neighbor.region_id = plot.region_id
				regions[plot.region_id].plots = append(regions[plot.region_id].plots, neighbor)
				to_check[*neighbor] = true
			}
		}
	}
}

func get_perimeter (board [][]*Plot, region Region) int {
	count := 0
	for _, plot := range region.plots {
		count += 4
		for _, neighbor := range get_neighbors(board, *plot) {
			if neighbor.region_id == plot.region_id {
				count -= 1
			}
		}
	}
	return count
}

type Side struct {
	x1 int
	y1 int
	x2 int
	y2 int
}

func get_sides (board [][]*Plot, region Region) int {
	sides := make(map[Side][]bool)
	for _, plot := range region.plots {
		side := Side{x1: plot.x, y1: plot.y, x2: plot.x + 1, y2: plot.y}
		_, ok := sides[side]
		if ! ok {
			sides[side] = make([]bool, 4)
		}
		sides[side][0] = true

		side = Side{x1: plot.x + 1, y1: plot.y, x2: plot.x + 1, y2: plot.y + 1}
		_, ok = sides[side]
		if ! ok {
			sides[side] = make([]bool, 4)
		}
		sides[side][1] = true

		side = Side{x1: plot.x, y1: plot.y, x2: plot.x, y2: plot.y + 1}
		_, ok = sides[side]
		if ! ok {
			sides[side] = make([]bool, 4)
		}
		sides[side][2] = true

		side = Side{x1: plot.x, y1: plot.y + 1, x2: plot.x + 1, y2: plot.y + 1}
		_, ok = sides[side]
		if ! ok {
			sides[side] = make([]bool, 4)
		}
		sides[side][3] = true
	}
	for key, value := range sides {
		count := 0
		for _, v := range value {
			if v {
				count++
			}
		}
		if count > 1 {
			delete(sides, key)
		}
	}
	changed := true
	for changed {
		changed = false
		for first, first_edges := range sides {
			for second, second_edges := range sides {
				if first == second {
					continue
				}
				for edge := range 4 {
					if first_edges[edge] && second_edges[edge] && first.x2 == second.x1 && first.y2 == second.y1 {
						changed = true
						delete(sides, first)
						delete(sides, second)
						sides[Side{x1: first.x1, y1: first.y1, x2: second.x2, y2: second.y2}] = first_edges
					}
				}
			}
		}
	}
	return len(sides)
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

	board := make([][]*Plot, 0)
	y := 0
    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		this_line := []byte(text_line)
		board = append(board, make([]*Plot, 0))
		for x, v := range this_line {
			board[y] = append(board[y], &Plot{ x: x, y: y, label: v, region_id: -1 })
		}
		y++
    }

    readFile.Close()

	regions := make([]Region, 0)

	for x, row := range board {
		for y, _ := range row {
			plot := board[x][y]
			if plot.region_id == -1 {
				regions = append(regions, Region{id: len(regions), plots: make([]*Plot, 0)})
				plot.region_id = len(regions) - 1
				regions[plot.region_id].plots = append(regions[plot.region_id].plots, plot)
				explore_plot(board, regions, *plot)
				
			}
		}
	}
	price := 0
	for _, region := range regions {
		area := len(region.plots)
		sides := get_sides(board, region)
		price += area * sides
	}
	fmt.Println(price)
}
