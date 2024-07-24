import time

from fastapi import BackgroundTasks, FastAPI
from pymongo import MongoClient

app = FastAPI()

scraped_data = []
reference_data = dict()

scrape_data_status = False


def download_scrape_data(host: str = "localhost", port: int = 27017):
    mongodb_client = MongoClient(host=host, port=port)

    db = mongodb_client.get_database("products")

    collections = db.list_collection_names()

    for collection in collections:
        for document in db[collection].find({}):
            scraped_data.append(document)

    time.sleep(10)
    print("Sleeping is over")
    global scrape_data_status
    scrape_data_status = True


def download_reference_data(): ...


@app.post("/download")
async def download(download_task: BackgroundTasks):
    download_task.add_task(download_scrape_data)

    return {"Everything is fine"}


@app.get("/status")
def status():
    if scrape_data_status:
        print(scraped_data)

    return scrape_data_status
