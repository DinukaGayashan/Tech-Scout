.PHONY: format-code
format-code:
    black --line-length=120 tech-scout-scraper/*/*.py

.PHONY: run-scraper
run-scraper:
	fastapi run tech-scout-scraper/src/app.py