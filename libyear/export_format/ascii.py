from prettytable import PrettyTable

from libyear.export_format.export_format import Item


class ASCIIFormatter:
    pt: PrettyTable
    sort: str

    def initialize(self, sort: bool):
        self.pt = PrettyTable()
        self.pt.field_names = ['Library', 'Current Version', 'Latest Version', 'Libyears behind']

        if sort:
            self.pt.sortby = 'Libyears behind'
            self.pt.reversesort = True

    def add_item(self, item: Item):
        self.pt.add_row([item.name, item.version, item.latest_version, item.libyear])

    def print(self):
        print(self.pt)
