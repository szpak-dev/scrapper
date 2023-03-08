import asyncio
from dataclasses import dataclass
import logging

import httpx


@dataclass
class HtmlDocument:
    path: str
    html: str


class Downloader:
    def __init__(self, root_url: str):
        self._root_url = root_url

    async def document(self, path: str) -> HtmlDocument:
        logging.info('> downloading <{}>'.format(path))

        url = '{}{}'.format(self._root_url, path)
        async with httpx.AsyncClient() as client:
            r = await client.get(url)

        return HtmlDocument(path, r.text)

    async def many_documents(self, paths: list[str]) -> list[HtmlDocument]:
        tasks = [asyncio.create_task(self.document(p)) for p in paths]
        task_results: list[HtmlDocument] = await asyncio.gather(*tasks)
        return task_results
