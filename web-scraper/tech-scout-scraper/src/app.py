from uvicorn.config import LOGGING_CONFIG
from pathlib import Path
from typing import List
import logging
from fastapi import BackgroundTasks, FastAPI, File, UploadFile

from .executor import Executor
from .schemas import Job
from .utils import get_jobs_from_config

app = FastAPI()

LOGGING_CONFIG["loggers"][__name__] = {
    "handlers": ["default"],
    "level": "INFO",
    "propagate": False,
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def scrape(jobs: List[Job]):
    executor = Executor(jobs)
    executor.run()


@app.post("/scrape")
async def root(scrape_task: BackgroundTasks, file: UploadFile = File(...)):
    logger.info(
        f"Saving the {file.filename} as scraper_config.json to current directory"
    )
    config_file_path = Path("./scraper_config.json")
    with open(config_file_path, "wb") as f:
        f.write(file.file.read())
    jobs = get_jobs_from_config(config_file_path)
    scrape_task.add_task(scrape, jobs)
    return {"Scrape task started"}


@app.get("/health")
async def health():
    # TODO: Need to implement after adding other services
    return {"Everything is working fine"}
