from pathlib import Path

from executor import Executor
from utils import get_jobs_from_config

if __name__ == "__main__":
    jobs = get_jobs_from_config(path=Path("web-scraper/scraper_config.json"))
    executor = Executor(jobs)
    executor.run()
    print(executor.execution_results)
