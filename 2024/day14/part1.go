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

//var BOARD_WIDTH int = 11
//var BOARD_HEIGHT int = 7
var BOARD_WIDTH int = 101
var BOARD_HEIGHT int = 103



func mod(a, b int) int {
    return (a % b + b) % b
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

	quadrant := make([]int, 4)
	for _, robot := range robots {
		new_x := mod(robot.x + ( 100 * robot.velocity_x), BOARD_WIDTH)
		new_y := mod(robot.y + ( 100 * robot.velocity_y), BOARD_HEIGHT)
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
	fmt.Println(quadrant[0] * quadrant[1] * quadrant[2] * quadrant[3])
}
