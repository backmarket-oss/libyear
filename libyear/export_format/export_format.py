from enum import Enum
from typing import Protocol

from pydantic import BaseModel


class Format(Enum):
    ASCII = "ASCII"
    JSON = "JSON"


class Item(BaseModel):
    name: str
    version: str
    latest_version: str
    libyear: str


class ExportFormat(Protocol):
    def initialize(self, sort: str | None):
        pass

    def add_item(self, item: Item):
        pass

    def print(self):
        pass
