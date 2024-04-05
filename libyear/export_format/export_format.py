from enum import Enum
from typing import Protocol
from typing import TextIO

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
    def initialize(self, sort: bool):
        """
        Use to set data before we iterate over the packages
        """
        pass

    def add_item(self, item: Item):
        """
        Use to set data for each iteration of the packages
        """
        pass

    def end(self, days: int):
        """
        Use to set data after we iterate over the packages
        """
        pass

    def print(self, output: TextIO):
        """
        Use to print the data
        """
        pass
