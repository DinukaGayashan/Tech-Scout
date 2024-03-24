import asyncio
import itertools
from typing import List

import aiohttp
from aiolimiter import AsyncLimiter
from schemas import Job


class Executor:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs

    def _generate_urls(self, job: Job) -> None:
        for category, page in itertools.product(
            job.categories, range(1, job.max_pages + 1)
        ):
            job._urls.append(
                f"{job.url}/{job.category_path}/{category.path}?{job.pagination_parameter}={page}"
            )

    async def _execute_job(self, job: Job):
        self._generate_urls(job)

        limiter = AsyncLimiter(job.rate_limit - (job.rate_limit / 5), 1)
        semaphore = asyncio.Semaphore(job.rate_limit)

        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in job._urls:
                tasks.append(
                    asyncio.ensure_future(
                        self._download_html(limiter, semaphore, url, session)
                    )
                )

            results = await asyncio.gather(*tasks, return_exceptions=True)

        return results

    def run(self):
        asyncio.run(self._execute_job(self.jobs[0]))

    async def _download_html(
        self,
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
