.PHONY: run-discovery-server
run-discovery-server:
	docker run -d --name=discovery-server -p 8500:8500 -v .:/ds consul:1.15.4
	docker exec discovery-server consul services register ds/service-registry.json
	