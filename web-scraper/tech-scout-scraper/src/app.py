from pathlib import Path
from typing import List

from fastapi import BackgroundTasks, FastAPI, File, UploadFile

from .executor import Executor
from .schemas import Job
from .utils import get_jobs_from_config

app = FastAPI()


def scrape(jobs: List[Job]):
    executor = Executor(jobs)
    executor.run()


@app.post("/scrape")
async def root(scrape_task: BackgroundTasks, file: UploadFile = File(...)):
    config_file_path = Path("./scraper_config.json")
    with open(config_file_path, "wb") as f:
        f.write(file.file.read())
    jobs = get_jobs_from_config(config_file_path)
    scrape_task.add_task(scrape, jobs)
    return {"Scrape task started"}
