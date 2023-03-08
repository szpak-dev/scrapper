from dataclasses import dataclass
from typing import Protocol


@dataclass
class ScrapProperty(Protocol):
    name: str
    css_query: str
    node_name: str
    #
    # @property
    # def options(self) -> list[str]:
    #     return [self.name, self.css_query, self.node_name]


@dataclass
class ScrapConfig(Protocol):
    manufacturer: str
    resource_label: str
    properties: list[ScrapProperty]
    #
    # @property
    # def options(self) -> dict[str, str]:
    #     return {self.resource_label: [p.options for p in self.properties]}
