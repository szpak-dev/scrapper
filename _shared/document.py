from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Anchor:
    name: str
    path: str


class Document:
    def __init__(self,  html: str):
        self._html = html
        self._html_soup = BeautifulSoup(html, features='html.parser')

    @property
    def html(self) -> str:
        return self._html

    def anchors(self, css_query: str) -> list[Anchor]:
        return [Anchor(a.text, a.get('href')) for a in self._html_soup.select(css_query)]

    def anchors_one(self, css_query: str) -> Anchor:
        node = self._html_soup.select_one(css_query)
        return Anchor(node.get('href'), node.get('text'))

    def query_html(self, css_query: str, fetch_attr: str) -> list[str]:
        return [node.get(fetch_attr) for node in self._html_soup.select(css_query)]

    def query_html_one(self, css_query: str, fetch_attr: str) -> str:
        node = self._html_soup.select_one(css_query)

        if node is None:
            return ''

        value = node.get(fetch_attr)

        if value is None:
            return node.text

        return value
