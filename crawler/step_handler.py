import logging
from abc import ABC, abstractmethod

from _shared.document import Document
from _shared.downloader import Downloader
from crawler.config import CrawlStep
from crawler.entities import Crawl, Resource


class StepHandler(ABC):
    def __init__(self, crawl: Crawl, step: CrawlStep, downloader: Downloader, parent_resources: list[Resource]):
        self.crawl = crawl
        self.step = step
        self.downloader = downloader
        self.parent_resources = parent_resources

    @abstractmethod
    async def save_resources(self) -> list[Resource]:
        ...

    async def _download(self, path: str) -> Document:
        html_document = await self.downloader.document(path)
        return Document(html=html_document.html)

    async def _download_many(self, paths: list[str]) -> list[Document]:
        return [await self._download(path) for path in paths]


class FirstStepHandler(StepHandler):
    async def save_resources(self) -> list[Resource]:
        logging.info('Saving resources in the first step')
        document = await self._download('')
        resource = self.crawl.add_resource(self.step.label, document.html)
        [resource.add_link(a.name, a.path) for a in document.anchors(self.step.css_query)]

        logging.info('>>> 1 resource saved')
        return [resource]


class NextStepHandler(StepHandler):
    async def save_resources(self) -> list[Resource]:
        logging.info('>>> Saving resources in the next step')
        resources = []
        for parent_resource in self.parent_resources:
            documents = await self._download_many(parent_resource.paths)
            for document in documents:
                resource = self.crawl.add_child_resource(parent_resource, self.step.label, document.html)
                [resource.add_link(a.name, a.path) for a in document.anchors(self.step.css_query)]
                resources.append(resource)

        logging.info('>>> {} resources saved'.format(len(resources)))
        return resources


class LastStepHandler(StepHandler):
    async def save_resources(self) -> list[Resource]:
        logging.info('Saving resources in last step')
        resources = []
        for parent_resource in self.parent_resources:
            documents = await self._download_many(parent_resource.paths)
            for document in documents:
                resources.append(self.crawl.add_child_resource(parent_resource, self.step.label, document.html))

        logging.info('>>> {} resources saved'.format(len(resources)))
        return resources


class StepHandlerFactory:
    def __init__(self, downloader: Downloader):
        self.downloader = downloader

    def create(self, crawl: Crawl, crawl_step: CrawlStep, parent_resources: list[Resource]) -> StepHandler:
        if crawl_step.first:
            return FirstStepHandler(crawl, crawl_step, self.downloader, parent_resources)

        if crawl_step.last:
            return LastStepHandler(crawl, crawl_step, self.downloader, parent_resources)

        return NextStepHandler(crawl, crawl_step, self.downloader, parent_resources)