import json
from pathlib import Path
from typing import List

from schemas import Job


def get_jobs_from_config(path: Path) -> List[Job]:
    with open(path, "r", encoding="utf-8") as scraper_config:
        configs = json.load(scraper_config)

    return [Job(**config) for config in configs]
