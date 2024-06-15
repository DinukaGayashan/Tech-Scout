package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"strings"

	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/go-sql-driver/mysql"
	consulAPI "github.com/hashicorp/consul/api"
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
	ID       int32           `json:"id"`
	Category string          `json:"category"`
	Name     string          `json:"name"`
	Specs    json.RawMessage `json:"specs"`
	Shops    json.RawMessage `json:"shops"`
}

type ItemRequestBody struct {
	Name     string  `json:"name"`
	Specs    string  `json:"specs"`
	Shops    string  `json:"shops"`
	MinPrice float64 `json:"minPrice"`
	MaxPrice float64 `json:"maxPrice"`
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

func registerOnDiscovery() {
	config := consulAPI.DefaultConfig()
	client, err := consulAPI.NewClient(config)
	if err != nil {
		log.Fatal(err)
	}

	registration := &consulAPI.AgentServiceRegistration{
		ID:      "query-api",
		Name:    "query-api",
		Address: "localhost",
		Port:    8001,
	}
	err = client.Agent().ServiceRegister(registration)
	if err != nil {
		log.Fatal(err)
	}
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

	registerOnDiscovery()

	router := gin.Default()
	for _, category := range config.Categories {
		router.GET("query/"+category, getItems)
	}
	router.Run("localhost:8001")
}
