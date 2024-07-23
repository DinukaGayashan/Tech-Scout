from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

import consul
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .executor import Executor
from .log import logger
from .schemas import Job
from .utils import get_jobs_from_config


# def deregister_scraper():
#     Consul().agent.service.deregister("scraper")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # client = consul.Consul()
    #
    # client.agent.service.register(
    #     name="scraper",
    #     # check=consul.Check.tcp(
    #     #     host="0.0.0.0",
    #     #     port=8000,
    #     #     interval="5s",
    #     #     deregister="1m",
    #     # ),
    # )

    # TODO: Needs to some testing not works properly
    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def scrape(jobs: List[Job]):
    executor = Executor(jobs)
    executor.run()


@app.post("/scrape")
async def root(scrape_task: BackgroundTasks, file: UploadFile = File(...)):
    logger.info(f"Saving the {file.filename} as scraper_config.json to current directory")
    config_file_path = Path("./web-scraper/scraper_config.json")
    with open(config_file_path, "wb") as f:
        f.write(file.file.read())
    jobs = get_jobs_from_config(config_file_path)
    scrape_task.add_task(scrape, jobs)
    return {"Scrape task started"}


@app.get("/dev")
async def dev(scrape_task: BackgroundTasks):
    logger.info("Loading the scraper config")
    config_file_path = Path("./web-scraper/scraper_config.json")
    jobs = get_jobs_from_config(config_file_path)
    scrape_task.add_task(scrape, jobs)
    return {"Scrape task started"}


@app.get("/health")
async def health():
    # TODO: Need to implement after adding other services
    return {"Everything is working fine"}
