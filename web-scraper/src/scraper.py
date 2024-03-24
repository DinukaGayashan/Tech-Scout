import json
from pathlib import Path

from executor import Executor
from schemas import Job


def get_jobs_from_config(path: Path) -> None:
    with open(path, "r", encoding="utf-8") as scraper_config:
        configs = json.load(scraper_config)

    jobs = []
    for config in configs:
        jobs.append(Job(**config))

    return jobs


if __name__ == "__main__":
    jobs = get_jobs_from_config(path=Path("web-scraper/src/scraper_config.json"))
    executor = Executor(jobs)
    executor.run()
