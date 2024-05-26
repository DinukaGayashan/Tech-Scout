package main

import (
	"database/sql"
	"fmt"
	"log"
	"strings"

	"net/http"
	"os"

	"github.com/ArthurHlt/go-eureka-client/eureka"
	"github.com/gin-gonic/gin"

	"github.com/go-sql-driver/mysql"
	"gopkg.in/yaml.v3"
)

var DB *sql.DB
var config Config

type DBConfig struct {
	User      string `yaml:"User"`
	Passwd    string `yaml:"Passwd"`
	Net       string `yaml:"Net"`
	Addr      string `yaml:"Addr"`
	DBName    string `yaml:"DBName"`
	TableName string `yaml:"TableName"`
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

type ItemRequestBody struct {
	Name  string `json:"name"`
	Specs string `json:"specs"`
	Shops string `json:"shops"`
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

func itemsByQuerying(category string, itemRequestBody ItemRequestBody) ([]Item, error) {
	query := "SELECT * FROM items WHERE category = ?"
	args := []interface{}{}
	args = append(args, category)

	if itemRequestBody.Name != "" {
		parts := strings.Split(itemRequestBody.Name, " ")
		for _, j := range parts {
			query += " AND name LIKE ?"
			args = append(args, "%"+j+"%")
		}
	}
	if itemRequestBody.Specs != "" {
		parts := strings.Split(itemRequestBody.Specs, " ")
		for _, j := range parts {
			query += " AND specs LIKE ?"
			args = append(args, "%"+j+"%")
		}
	}
	if itemRequestBody.Shops != "" {
		parts := strings.Split(itemRequestBody.Shops, " ")
		for _, j := range parts {
			query += " AND shops LIKE ?"
			args = append(args, "%"+j+"%")
		}
	}

	rows, _ := DB.Query(query, args...)
	defer rows.Close()

	var items []Item
	for rows.Next() {
		var item Item
		rows.Scan(&item.ID, &item.Category, &item.Name, &item.Specs, &item.Shops)
		items = append(items, item)
	}
	return items, nil
}

func getItems(c *gin.Context) {
	endpoint := c.Request.URL.Path
	parts := strings.Split(endpoint, "/")
	category := parts[2]
	var items []Item

	var itemRequestBody ItemRequestBody
	if c.Request.Body != nil && c.Request.ContentLength != 0 {
		if err := c.BindJSON(&itemRequestBody); err != nil {
			return
		}
	}
	var err error
	items, err = itemsByQuerying(category, itemRequestBody)
	if err != nil {
		log.Fatal(err)
	}

	c.IndentedJSON(http.StatusOK, items)
}

func main() {
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

	client := eureka.NewClient([]string{"http://localhost:8761/eureka"})
	instance := eureka.NewInstanceInfo("localhost", "query-api", "127.0.0.1", 8001, 30, false)
	client.RegisterInstance("query-api", instance)
	client.GetApplication(instance.App)
	client.GetInstance(instance.App, instance.HostName)
	client.SendHeartbeat(instance.App, instance.HostName)

	router := gin.Default()
	for _, category := range config.Categories {
		router.GET("query/"+category, getItems)
	}
	router.Run("localhost:8001")
}
