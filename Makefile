.PHONY: run-system
run-system:
	make -C discovery-server run-discovery-server
	make -C api-gateway run-api-gateway
	make -C product-matcher run-product-matcher
	make -C web-scraper run-scraper
	make -C query-api run-query-api
	
	
.PHONY: setup-dev-web-scraper
setup-dev-web-scraper:
	python -m venv venv && \
	./venv/bin/python -m pip install -r web-scraper/requirements-dev.txt && \
	./venv/bin/python -m uv pip install -r web-scraper/requirements.txt

.PHONY: run-web-scraper
run-web-scraper:
	./venv/bin/python -m uvicorn web-scraper.tech-scout-scraper.src.app:app --reload

.PHONY: run-product-matcher
run-product-matcher:
	./venv/bin/python -m uvicorn product-matcher.app:app --reload --port=8002

.PHONY: generate-requirements-webscraper
generate-requirements-web-scraper:
	cd web-scraper && ./venv/bin/python -m uv pip freeze | uv pip compile - -o requirements.txt

.PHONY: run-docker
run-docker:
	docker compose up

.PHONY: build-web-scraper
build-scraper:
	cd web-scraper && \
	rm -rf dist build && \
	./venv/bin/python -m build --sdist --wheel --installer=uv --verbose

.PHONY: start-mysql
start-mysql:
	docker run --name tech-scout-mysql -e MYSQL_ROOT_PASSWORD=admin -d mysql:latest

