package main

import (
	"strings"
)

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
