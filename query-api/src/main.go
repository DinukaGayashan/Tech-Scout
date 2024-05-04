package main

import (
	"database/sql"
	"fmt"
	"log"
	"strings"

	"net/http"
	"os"

	"github.com/go-sql-driver/mysql"

	"github.com/gin-gonic/gin"
	"gopkg.in/yaml.v3"
)

var DB *sql.DB

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

type Item struct {
	ID       int32  `json:"id"`
	Category string `json:"category"`
	Name     string `json:"name"`
	Specs    string `json:"specs"`
	Shops    string `json:"shops"`
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

func itemsByCategory(category string) ([]Item, error) {
	var items []Item

	rows, err := DB.Query("SELECT * FROM structured_data.items WHERE category = ?", category)
	if err != nil {
		return nil, fmt.Errorf("itemsByCategory %q: %v", category, err)
	}
	defer rows.Close()

	for rows.Next() {
		var item Item
		if err := rows.Scan(&item.ID, &item.Category, &item.Name, &item.Specs, &item.Shops); err != nil {
			return nil, fmt.Errorf("itemsByCategory %q: %v", category, err)
		}
		items = append(items, item)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("itemsByCategory %q: %v", category, err)
	}
	return items, nil
}

func getItems(c *gin.Context) {
	endpoint := c.Request.URL.Path
	parts := strings.Split(endpoint, "/")
	category := parts[2]
	items, err := itemsByCategory(category)
	if err != nil {
		log.Fatal(err)
	}

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

	var err error
	DB, err = sql.Open("mysql", dbConfig.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := DB.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("DB Connected!")
	defer DB.Close()

	router := gin.Default()
	for _, category := range config.Categories {
		router.GET("query/"+category, getItems)
	}
	router.Run("localhost:8080")
}
