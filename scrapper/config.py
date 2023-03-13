from dataclasses import dataclass
from typing import Protocol


@dataclass
class ScrapProperty(Protocol):
    name: str
    css_query: str
    fetch_attr: str


@dataclass
class ScrapConfig(Protocol):
    target: str
    resource_label: str
    properties: list[ScrapProperty]
