package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"gopkg.in/yaml.v3"
)

type Config struct {
	Categories []string `yaml:"categories"`
}

func (c *Config) getConfigs() *Config {
	yamlFile, err := os.ReadFile("config.yaml")
	if err != nil {
		log.Printf("yamlFile.Get err   #%v ", err)
	}
	err = yaml.Unmarshal(yamlFile, c)
	if err != nil {
		log.Fatalf("Unmarshal: %v", err)
	}
	return c
}

type Item struct {
	Name string `json:"name"`
}

func getItems(c *gin.Context) {
	endpoint := c.Request.URL.Path
	var items = []Item{{Name: endpoint}}
	c.IndentedJSON(http.StatusOK, items)
}

func main() {
	var config Config
	config.getConfigs()

	router := gin.Default()
	for _, category := range config.Categories {
		router.GET("query/"+category, getItems)
	}
	router.Run("localhost:8080")
}
