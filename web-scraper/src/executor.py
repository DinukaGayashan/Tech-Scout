import asyncio
import itertools
from typing import List

import aiohttp
from aiolimiter import AsyncLimiter

from schemas import Job


class Executor:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs

    @staticmethod
    def generate_urls(job: Job) -> List[str]:
        return [
            f"{job.url}/{job.category_path}/{category.path}?{job.pagination_parameter}={page}"
            for category, page in itertools.product(
                job.categories, range(1, job.max_pages + 1)
            )
        ]

    async def execute_job(self, job: Job):
        urls = self.generate_urls(job)

        limiter = AsyncLimiter(job.rate_limit - (job.rate_limit / 5), time_period=1)
        semaphore = asyncio.Semaphore(job.rate_limit)

        tasks = []

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            tasks.extend(
                asyncio.ensure_future(
                    self.download_html(limiter, semaphore, url, session)
                )
                for url in urls
            )
            results = await asyncio.gather(*tasks, return_exceptions=True)

        return results

    def run(self):
        asyncio.run(self.execute_job(self.jobs[0]))

    @staticmethod
    async def download_html(
        limiter: AsyncLimiter,
        semaphore: asyncio.Semaphore,
        url: str,
        session: aiohttp.ClientSession,
    ) -> bytes:
        await semaphore.acquire()
        async with limiter:
            async with session.get(url) as resp:
                content = await resp.read()
                semaphore.release()
                return content
