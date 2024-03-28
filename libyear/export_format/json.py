from typing import TextIO

from libyear.export_format.export_format import Item


class JSONFormatter:
    def initialize(self, sort: bool):
        pass

    def add_item(self, item: Item):
        pass

    def end(self, days: int):
        pass

    def print(self, output: TextIO):
        pass
