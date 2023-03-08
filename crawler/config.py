from dataclasses import dataclass
from typing import Protocol


@dataclass
class CrawlStep(Protocol):
    level: int
    label: str
    css_query: str
    query_params: str
    first: bool
    last: bool


@dataclass
class CrawlConfig(Protocol):
    manufacturer: str
    root_url: str
    steps: list[CrawlStep]
