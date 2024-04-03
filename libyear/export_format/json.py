from typing import TextIO, List

from pydantic import BaseModel

from libyear.export_format.export_format import Item
from libyear.utils import calculate_libyear


class Dependency(BaseModel):
    name: str
    version: str
    latest_version: str
    libyear: str


class JsonOutput(BaseModel):
    dependencies: List[Dependency] = []
    libyears_behind: str = ''


class JSONFormatter:
    sort: bool  # Used to sort with libyear attribute and keep same initial behaviour
    json_output: JsonOutput

    def initialize(self, sort: bool):
        self.sort = sort
        self.json_output = JsonOutput()

    def add_item(self, item: Item):
        self.json_output.dependencies.append(
            Dependency(
                name=item.name,
                version=item.version,
                latest_version=item.latest_version,
                libyear=item.libyear
            )
        )

    def end(self, days: int):
        self.json_output.libyears_behind = calculate_libyear(days=days)

        if self.sort:
            self.json_output.dependencies.sort(key= lambda dep : (dep.libyear, dep.name))

    def print(self, output: TextIO):
        output.write(self.json_output.model_dump_json())
