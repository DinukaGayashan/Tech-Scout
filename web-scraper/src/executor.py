import asyncio
import itertools
from typing import List

import aiohttp
from aiolimiter import AsyncLimiter

from schemas import Job, URL, Page, PageCollection


class Executor:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs
        self.execution_results = []

    @staticmethod
    def generate_urls(job: Job) -> List[URL]:
        return [
            URL(
                url=f"{job.url}/{job.category_path}/{category.path}?{job.pagination_parameter}={page}",
                category=category,
            )
            for category, page in itertools.product(job.categories, range(1, job.max_pages + 1))
        ]

    async def execute_job(self, job: Job) -> PageCollection:
        urls = self.generate_urls(job)

        limiter = AsyncLimiter(job.rate_limit - (job.rate_limit / 5), time_period=1)
        semaphore = asyncio.Semaphore(job.rate_limit)

        tasks = []

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            tasks.extend(asyncio.ensure_future(self.download_html(limiter, semaphore, url, session)) for url in urls)
            results = await asyncio.gather(*tasks, return_exceptions=True)

        return PageCollection(job=job, pages=results)

    def run(self) -> None:
        for job in self.jobs:
            self.execution_results.append(asyncio.run(self.execute_job(job)))

    def parse_pages(self): ...

    @staticmethod
    async def download_html(
        limiter: AsyncLimiter,
        semaphore: asyncio.Semaphore,
        url: URL,
        session: aiohttp.ClientSession,
    ) -> Page:
        await semaphore.acquire()
        async with limiter:
            async with session.get(url.url) as resp:
                content = await resp.read()
                semaphore.release()
                return Page(content=content, category=url.category)
