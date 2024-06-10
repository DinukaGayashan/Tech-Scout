package main

import (
	"encoding/json"
	"strings"
)

func queryByName(items []Item, name string) ([]Item, error) {
	var result []Item

	for _, item := range items {
		if strings.Contains(strings.ToLower(item.Name), name) {
			result = append(result, item)
		}
	}

	return result, nil
}

func queryBySpecs(items []Item, spec string) ([]Item, error) {
	var result []Item

	for _, item := range items {
		var data map[string]interface{}
		json.Unmarshal(item.Specs, &data)
		for _, value := range data {
			if str, ok := value.(string); ok && strings.Contains(strings.ToLower(str), spec) {
				result = append(result, item)
				break
			}
		}
	}

	return result, nil
}

func queryByShops(items []Item, shop string) ([]Item, error) {
	var result []Item

	for _, item := range items {
		var data map[string]json.RawMessage
		json.Unmarshal(item.Shops, &data)

		var list []json.RawMessage
		for key, value := range data {
			if strings.Contains(strings.ToLower(key), shop) {
				shopMap := map[string]json.RawMessage{
					key: value,
				}
				shopJSON, _ := json.Marshal(shopMap)
				list = append(list, shopJSON)
			} else {
				var shopDetails map[string]interface{}
				json.Unmarshal(value, &shopDetails)
				for _, v := range shopDetails {
					if str, ok := v.(string); ok && strings.Contains(strings.ToLower(str), shop) {
						shopMap := map[string]json.RawMessage{
							key: value,
						}
						shopJSON, _ := json.Marshal(shopMap)
						list = append(list, shopJSON)
					}
				}
			}
		}
		if len(list) > 0 {
			shops, _ := json.Marshal(list)
			item.Shops = shops
			result = append(result, item)
		}
	}

	return result, nil
}

func itemsByQuerying(category string, itemRequestBody ItemRequestBody) ([]Item, error) {
	query := "SELECT * FROM items WHERE category = ?"
	args := []interface{}{}
	args = append(args, category)

	rows, _ := DB.Query(query, args...)
	defer rows.Close()

	var items []Item
	for rows.Next() {
		var item Item
		rows.Scan(&item.ID, &item.Category, &item.Name, &item.Specs, &item.Shops)
		items = append(items, item)
	}

	if itemRequestBody.Name != "" {
		items, _ = queryByName(items, strings.ToLower(itemRequestBody.Name))
	}
	if itemRequestBody.Specs != "" {
		items, _ = queryBySpecs(items, strings.ToLower(itemRequestBody.Specs))
	}
	if itemRequestBody.Shops != "" {
		items, _ = queryByShops(items, strings.ToLower(itemRequestBody.Shops))
	}

	return items, nil
}
