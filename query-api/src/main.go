package main

import (
	"database/sql"
	"fmt"
	"log"

	"net/http"
	"os"

	"github.com/go-sql-driver/mysql"

	"github.com/gin-gonic/gin"
	"gopkg.in/yaml.v3"
)

type DBConfig struct {
	User   string `yaml:"User"`
	Passwd string `yaml:"Passwd"`
	Net    string `yaml:"Net"`
	Addr   string `yaml:"Addr"`
	DBName string `yaml:"DBName"`
}

type Config struct {
	Categories []string `yaml:"categories"`
	DBConfig   DBConfig `yaml:"dbConfig"`
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
	ID       string `json:"id"`
	Category string `json:"category"`
	Name     string `json:"name"`
	Specs    string `json:"specs"`
	Shops    string `json:"shops"`
}

func getItems(c *gin.Context) {
	endpoint := c.Request.URL.Path
	var items = []Item{{Name: endpoint}}
	c.IndentedJSON(http.StatusOK, items)
}

func main() {
	var config Config
	config.getConfigs()

	dbConfig := mysql.Config{
		User:   config.DBConfig.User,
		Passwd: config.DBConfig.Passwd,
		Net:    config.DBConfig.Net,
		Addr:   config.DBConfig.Addr,
		DBName: config.DBConfig.DBName,
	}

	db, err := sql.Open("mysql", dbConfig.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("DB Connected!")

	defer db.Close()

	router := gin.Default()
	for _, category := range config.Categories {
		router.GET("query/"+category, getItems)
	}
	router.Run("localhost:8080")
}
