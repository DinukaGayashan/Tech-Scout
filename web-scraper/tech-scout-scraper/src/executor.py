import asyncio
import itertools
from http import HTTPStatus
from typing import List

import aiohttp
from aiolimiter import AsyncLimiter

from .html_parser import Parser
from .schemas import URL, Job, Page, PageCollection


class Executor:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs

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
        products = []
        for job in self.jobs:
            results = asyncio.run(self.execute_job(job))
            # pprint(results)
            parser = Parser(page_collection=results, job=job)
            products.extend(parser.parse_products())

        print(len(products))
        from pymongo import MongoClient

        client = MongoClient("mongodb://mongodb:27017")

        db = client["products"]
        db["nanotek"].delete_many({})
        print(db["nanotek"].count_documents({}))
        db["nanotek"].insert_many([dict(product) for product in products])
        print(db["nanotek"].count_documents({}))

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
                print(f"GET - {url.url} - {resp.status}")
                if resp.status == HTTPStatus.NOT_FOUND:
                    return -1
                semaphore.release()
                return Page(content=content, category=url.category)
