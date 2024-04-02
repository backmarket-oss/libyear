from libyear.export_format.ascii import ASCIIFormatter
from libyear.export_format.exceptions import FormatterNotImplementedError
from libyear.export_format.export_format import ExportFormat, Format
from libyear.export_format.json import JSONFormatter


def get_formatter(name: str) -> ExportFormat:
    match Format(name):
        case Format.ASCII:
            return ASCIIFormatter()
        case Format.JSON:
            return JSONFormatter()

    raise FormatterNotImplementedError()
