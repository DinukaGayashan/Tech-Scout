package main

import (
	"fmt"
)

func main() {
	var s string = "abc"
	b := []byte(s)
	b[1] = 99
	fmt.Println(b)
}
