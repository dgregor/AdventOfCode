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
		perimeter := get_perimeter(board, region)
		price += area * perimeter
	}
	fmt.Println(price)
	
}
