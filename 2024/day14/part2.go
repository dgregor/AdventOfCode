package main

import (
	"bufio"
    "fmt"
    "os"
	"regexp"
	"strconv"
)

type Robot struct {
	x int
	y int
	velocity_x int
	velocity_y int
}

var BOARD_WIDTH int = 101
var BOARD_HEIGHT int = 103

func mod(a, b int) int {
    return (a % b + b) % b
}

func get_board_density(board [][]int) int {
	neighbor_threshold := 2
	neighbors := 0
	for y := range BOARD_HEIGHT {
		for x := range BOARD_WIDTH {
			if board[y][x] == 0 {
				continue
			}
			count := 0
			if x > 0 {
				if board[y][x-1] > 0 {
					count++
				}
				if y > 0 {
					if board[y-1][x-1] > 0 {
						count++
					}
				}
				if y < BOARD_HEIGHT - 1 {
					if board[y+1][x-1] > 0 {
						count++
					}
				}
			}
			if x < BOARD_WIDTH - 1 {
				if board[y][x+1] > 0 {
					count++
				}
				if y > 0 {
					if board[y-1][x+1] > 0 {
						count++
					}
				}
				if y < BOARD_HEIGHT - 1 {
					if board[y+1][x+1] > 0 {
						count++
					}
				}
			}
			if y > 0 {
				if board[y-1][x] > 0 {
					count++
				}
			}
			if y < BOARD_HEIGHT - 1 {
				if board[y+1][x] > 0 {
					count++
				}
			}
			if count >= neighbor_threshold {
				neighbors++
			}
		}
	}
	return neighbors
}

func print_board (robots []Robot, iteration int, only_tree bool) bool{
	board := make([][]int, BOARD_HEIGHT)
	for i := range BOARD_HEIGHT {
		board[i] = make([]int, BOARD_WIDTH)
	}
	for _, robot := range robots {
		new_x := mod(robot.x + ( iteration * robot.velocity_x), BOARD_WIDTH)
		new_y := mod(robot.y + ( iteration * robot.velocity_y), BOARD_HEIGHT)
		board[new_y][new_x]++
	}
	density := get_board_density(board)
	if ! only_tree || density > 300 {
		for _, row := range board {
			this_string := ""
			for _, num := range row {
				if num == 0 {
					this_string += " "
				} else {
					this_string += strconv.Itoa(num)
				}
			}
			fmt.Println(this_string)
		}
	}
	return density > 300
}

func main() {

    filePath := os.Args[1]
    readFile, err := os.Open(filePath)

    if err != nil {
        fmt.Println(err)
    }

	robots := make([]Robot, 0)
	
    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)
	var text_line string
	re := regexp.MustCompile(`p=((?:-?)[0-9]+),((?:-?)[0-9]+) v=((?:-?)[0-9]+),((?:-?)[0-9]+)`)

    for fileScanner.Scan() {
		text_line = fileScanner.Text()
		match := re.FindStringSubmatch(text_line)
		x, _ := strconv.Atoi(match[1])
		y, _ := strconv.Atoi(match[2])
		velocity_x, _ := strconv.Atoi(match[3])
		velocity_y, _ := strconv.Atoi(match[4])
		robots = append(robots, Robot{x: x, y: y, velocity_x: velocity_x, velocity_y: velocity_y})
	}

    readFile.Close()

	for i := range 1000000 {
		quadrant := make([]int, 4)
		for _, robot := range robots {
			new_x := mod(robot.x + ( i * robot.velocity_x), BOARD_WIDTH)
			new_y := mod(robot.y + ( i * robot.velocity_y), BOARD_HEIGHT)
			if new_x < BOARD_WIDTH / 2 {
				if new_y < BOARD_HEIGHT / 2 {
					quadrant[0]++
				} else if new_y > BOARD_HEIGHT / 2 {
					quadrant[1]++
				}
			} else if new_x > BOARD_WIDTH / 2 {
				if new_y < BOARD_HEIGHT / 2 {
					quadrant[2]++
				} else if new_y > BOARD_HEIGHT / 2 {
					quadrant[3]++
				}
			}
		}
		if print_board(robots, i, true) {
			fmt.Println(i)
			break
		}
	}
}
