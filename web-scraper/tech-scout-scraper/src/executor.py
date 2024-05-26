import asyncio
import itertools
import logging
import os
from datetime import datetime
from http import HTTPStatus
from typing import List
from uuid import UUID, SafeUUID

import aiohttp
from aiolimiter import AsyncLimiter
from pymongo import MongoClient
from uvicorn.config import LOGGING_CONFIG

from .html_parser import Parser
from .schemas import URL, Job, Page, PageCollection

LOGGING_CONFIG["loggers"][__name__] = {
    "handlers": ["default"],
    "level": "INFO",
    "propagate": False,
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs
        self.mongodb_client = MongoClient()
        self.db_name = "products"
        self.collection_suffix = (
            str(datetime.now().strftime("%Y-%m-%d-%H-%M"))
            + "-"
            + str(UUID(bytes=os.urandom(16), version=5, is_safe=SafeUUID.safe))[:8]
        )
        self.total_parsed_count = 0

    def get_collection_name(self, shop: str) -> str:
        return shop + "-" + self.collection_suffix

    @staticmethod
    def generate_urls(job: Job) -> List[URL]:
        urls = []
        for category, page in itertools.product(
            job.categories, range(1, job.max_pages + 1)
        ):
            if job.pagination_path_config:
                urls.append(
                    URL(
                        url=f"{job.url}/{job.category_path}/{category.path}/{job.pagination_path}/{page}",
                        category=category,
                    )
                )
                continue

            if job.pagination_parameter_config:
                urls.append(
                    URL(
                        url=f"{job.url}/{job.category_path}/{category.path}?{job.pagination_parameter}={page}",
                        category=category,
                    )
                )

        return urls

    async def execute_job(self, job: Job) -> PageCollection:
        urls = self.generate_urls(job)

        limiter = AsyncLimiter(4 * job.rate_limit / 5, time_period=1)
        semaphore = asyncio.Semaphore(job.rate_limit)

        tasks = []

        async with aiohttp.ClientSession(raise_for_status=False) as session:
            tasks.extend(
                asyncio.ensure_future(
                    self.download_html(limiter, semaphore, url, session)
                )
                for url in urls
            )
            results = await asyncio.gather(*tasks, return_exceptions=True)

        filtered_results = [result for result in results if not isinstance(result, int)]
        return PageCollection(pages=filtered_results)

    def run(self) -> None:
        for job in self.jobs:
            results = asyncio.run(self.execute_job(job))
            parser = Parser(page_collection=results, job=job)
            products = parser.parse_products()
            self.total_parsed_count += len(products)
            self.upload_parsed_products(products, self.get_collection_name(job.shop))

        logger.info(f"Total parsed product count: {self.total_parsed_count}")

    def upload_parsed_products(self, products, collection_name) -> None:
        db = self.mongodb_client[self.db_name]
        collection = db[collection_name]
        collection.insert_many([dict(product) for product in products])

    @staticmethod
    async def download_html(
        limiter: AsyncLimiter,
        semaphore: asyncio.Semaphore,
        url: URL,
        session: aiohttp.ClientSession,
    ) -> Page | int:
        await semaphore.acquire()
        async with limiter:
            async with session.get(url.url) as resp:
                content = await resp.read()
                logger.info(f"GET - {url.url} - {resp.status}")
                if resp.status == HTTPStatus.NOT_FOUND:
                    return -1
                semaphore.release()
                return Page(content=content, category=url.category)
