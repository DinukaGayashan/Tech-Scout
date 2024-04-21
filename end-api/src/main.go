package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	// "fmt"
)

type Item struct {
	Name string `json:"name"`
}

var items = []Item{{Name: "abc"}}

func getItems(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, items)
}

func main() {
	router := gin.Default()
	router.GET("/items", getItems)
	router.Run("localhost:8080")
}
