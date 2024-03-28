from prettytable import PrettyTable

from libyear.export_format.export_format import Item
from libyear.utils import calculate_libyear


class ASCIIFormatter:
    pt: PrettyTable
    sort: str
    total_days: int

    def initialize(self, sort: bool):
        self.pt = PrettyTable()
        self.pt.field_names = ['Library', 'Current Version', 'Latest Version', 'Libyears behind']

        if sort:
            self.pt.sortby = 'Libyears behind'
            self.pt.reversesort = True

    def add_item(self, item: Item):
        self.pt.add_row([item.name, item.version, item.latest_version, item.libyear])

    def end(self, days: int):
        self.total_days = days

    def print(self):
        print(self.pt)
        print("Your system is %s libyears behind" % calculate_libyear(days=self.total_days))
