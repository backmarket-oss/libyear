import argparse
import json
import os
import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec
from importlib.util import spec_from_loader
from pathlib import Path
from unittest import mock

import pytest


def load_libyear_module():
    """As the module has no extension, this workaround is needed to load"""
    libyear_path = str(Path(__file__).parent.parent / "libyear/libyear")
    spec = spec_from_loader("libyear", SourceFileLoader("libyear", libyear_path))
    libyear = module_from_spec(spec)
    spec.loader.exec_module(libyear)
    sys.modules["libyear"] = libyear
    return libyear


libyear = load_libyear_module()


@pytest.fixture(scope="module")
def vcr_config():
    return {"decode_compressed_response": True}


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    # Put all cassettes in tests/cassettes/{module}/{test}.yaml
    return os.path.join("tests/cassettes/", request.module.__name__)


@pytest.mark.vcr()
def test_libyear_main_output(capsys):
    requirements_path = str(Path(__file__).parent / "data" / "requirements.txt")

    with mock.patch(
        "libyear.argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(r=requirements_path, sort=False, format="ASCII"),
    ):
        libyear.main()

    out, err = capsys.readouterr()
    out_lst = out.split("\n")

    assert err == ""
    assert (
        out_lst[0:3]
        == """\
+-------------------+-----------------+----------------+-----------------+
|      Library      | Current Version | Latest Version | Libyears behind |
+-------------------+-----------------+----------------+-----------------+""".split("\n")
    )

    ref_lst = """\
|     pyparsing     |      2.4.5      |     2.4.7      |       0.4       |
|      pathspec     |      0.6.0      |     0.8.1      |       1.1       |
|     packaging     |       19.2      |      20.8      |       1.23      |
|     typed-ast     |      1.4.0      |     1.4.1      |       0.61      |
|     virtualenv    |      16.6.2     |     20.2.2     |       1.4       |
|     pre-commit    |      1.20.0     |     2.9.3      |       1.11      |
|       regex       |    2019.12.9    |   2020.11.13   |       0.93      |
|       pyyaml      |      5.1.1      |     5.3.1      |       0.78      |
|        mypy       |      0.750      |     0.790      |       0.86      |
|       attrs       |      19.1.0     |     20.3.0     |       1.68      |
|      watchdog     |      0.9.0      |     1.0.2      |       2.31      |
|      identify     |      1.4.5      |     1.5.10     |       1.44      |
|      colorama     |      0.4.1      |     0.4.4      |       1.89      |
|       black       |     19.10b0     |     20.8b1     |       0.83      |
|         py        |      1.8.0      |     1.10.0     |       1.81      |
|   more-itertools  |      7.0.0      |     8.6.0      |       1.59      |
|   pytest-testmon  |      0.9.16     |     1.0.3      |       1.39      |
|       isort       |      4.3.17     |     5.6.4      |       1.52      |
|        toml       |      0.10.0     |     0.10.2     |       2.08      |
|      nodeenv      |      1.3.3      |     1.5.0      |       1.8       |
|       pytest      |      4.4.0      |     6.2.1      |       1.71      |
|        tox        |      3.14.2     |     3.20.1     |       0.85      |
|      pyflakes     |      2.1.1      |     2.2.0      |       1.11      |
|    atomicwrites   |      1.3.0      |     1.4.0      |       1.24      |
|       flake8      |      3.7.7      |     3.8.4      |       1.6       |
|      coverage     |      4.5.3      |     5.3.1      |       1.78      |
|        six        |      1.12.0     |     1.15.0     |       1.45      |
|   flake8-bugbear  |      19.3.0     |    20.11.1     |       1.66      |
|       click       |       7.0       |     7.1.2      |       1.59      |
|  mypy-extensions  |      0.4.1      |     0.4.3      |       1.15      |
|      appdirs      |      1.4.3      |     1.4.4      |       3.18      |
| typing-extensions |     3.7.4.1     |    3.7.4.3     |       0.82      |
|        cfgv       |      2.0.1      |     3.2.0      |       1.03      |
|    pycodestyle    |      2.5.0      |     2.6.0      |       1.28      |\
""".split("\n")

    def table_sort(s):
        """remove `|` + any spaces, in order to get alphabetic sort of first column"""
        return s.lstrip(" |")

    assert sorted(out_lst[3:-3], key=table_sort) == sorted(ref_lst, key=table_sort)

    assert (
        out_lst[-3:]
        == """\
+-------------------+-----------------+----------------+-----------------+
Your system is 47.2 libyears behind
""".split("\n")
    )


@pytest.mark.vcr()
def test_libyear_main_output_with_json(capsys):
    requirements_path = str(Path(__file__).parent / "data" / "requirements.txt")

    with mock.patch(
        "libyear.argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(r=requirements_path, sort=True, format="JSON"),
    ):
        libyear.main()

    out, _ = capsys.readouterr()
    dict_format = json.loads(out)

    assert dict_format == {
        "dependencies": [
            {
                "name": "toml",
                "version": "0.10.0",
                "latest_version": "0.10.2",
                "libyear": "2.08",
            },
            {
                "name": "six",
                "version": "1.12.0",
                "latest_version": "1.16.0",
                "libyear": "2.4",
            },
            {
                "name": "py",
                "version": "1.8.0",
                "latest_version": "1.11.0",
                "libyear": "2.7",
            },
            {
                "name": "entrypoints",
                "version": "0.3",
                "latest_version": "0.4",
                "libyear": "3.07",
            },
            {
                "name": "appdirs",
                "version": "1.4.3",
                "latest_version": "1.4.4",
                "libyear": "3.18",
            },
            {
                "name": "colorama",
                "version": "0.4.1",
                "latest_version": "0.4.6",
                "libyear": "3.92",
            },
            {
                "name": "regex",
                "version": "2019.12.9",
                "latest_version": "2023.12.25",
                "libyear": "4.04",
            },
            {
                "name": "cfgv",
                "version": "2.0.1",
                "latest_version": "3.4.0",
                "libyear": "4.06",
            },
            {
                "name": "typed-ast",
                "version": "1.4.0",
                "latest_version": "1.5.5",
                "libyear": "4.08",
            },
            {
                "name": "pyyaml",
                "version": "5.1.1",
                "latest_version": "6.0.1",
                "libyear": "4.12",
            },
            {
                "name": "pluggy",
                "version": "0.13.1",
                "latest_version": "1.4.0",
                "libyear": "4.18",
            },
            {
                "name": "pathspec",
                "version": "0.6.0",
                "latest_version": "0.12.1",
                "libyear": "4.19",
            },
            {
                "name": "mypy",
                "version": "0.750",
                "latest_version": "1.9.0",
                "libyear": "4.27",
            },
            {
                "name": "tox",
                "version": "3.14.2",
                "latest_version": "4.14.2",
                "libyear": "4.3",
            },
            {
                "name": "pyparsing",
                "version": "2.4.5",
                "latest_version": "3.1.2",
                "libyear": "4.32",
            },
            {
                "name": "typing-extensions",
                "version": "3.7.4.1",
                "latest_version": "4.10.0",
                "libyear": "4.33",
            },
            {
                "name": "black",
                "version": "19.10b0",
                "latest_version": "24.3.0",
                "libyear": "4.38",
            },
            {
                "name": "pre-commit",
                "version": "1.20.0",
                "latest_version": "3.7.0",
                "libyear": "4.41",
            },
            {
                "name": "mypy-extensions",
                "version": "0.4.1",
                "latest_version": "1.0.0",
                "libyear": "4.45",
            },
            {
                "name": "packaging",
                "version": "19.2",
                "latest_version": "24.0",
                "libyear": "4.48",
            },
            {
                "name": "nodeenv",
                "version": "1.3.3",
                "latest_version": "1.8.0",
                "libyear": "4.51",
            },
            {
                "name": "virtualenv",
                "version": "16.6.2",
                "latest_version": "20.25.1",
                "libyear": "4.61",
            },
            {
                "name": "identify",
                "version": "1.4.5",
                "latest_version": "2.5.35",
                "libyear": "4.68",
            },
            {
                "name": "isort",
                "version": "4.3.17",
                "latest_version": "5.13.2",
                "libyear": "4.68",
            },
            {
                "name": "pycodestyle",
                "version": "2.5.0",
                "latest_version": "2.11.1",
                "libyear": "4.7",
            },
            {
                "name": "more-itertools",
                "version": "7.0.0",
                "latest_version": "10.2.0",
                "libyear": "4.79",
            },
            {
                "name": "attrs",
                "version": "19.1.0",
                "latest_version": "23.2.0",
                "libyear": "4.83",
            },
            {
                "name": "filelock",
                "version": "3.0.12",
                "latest_version": "3.13.3",
                "libyear": "4.85",
            },
            {
                "name": "pyflakes",
                "version": "2.1.1",
                "latest_version": "3.2.0",
                "libyear": "4.85",
            },
            {
                "name": "flake8",
                "version": "3.7.7",
                "latest_version": "7.0.0",
                "libyear": "4.86",
            },
            {
                "name": "flake8-bugbear",
                "version": "19.3.0",
                "latest_version": "24.2.6",
                "libyear": "4.87",
            },
            {
                "name": "click",
                "version": "7.0",
                "latest_version": "8.1.7",
                "libyear": "4.89",
            },
            {
                "name": "pytest",
                "version": "4.4.0",
                "latest_version": "8.1.1",
                "libyear": "4.94",
            },
            {
                "name": "pytest-testmon",
                "version": "0.9.16",
                "latest_version": "2.1.1",
                "libyear": "4.95",
            },
            {
                "name": "mccabe",
                "version": "0.6.1",
                "latest_version": "0.7.0",
                "libyear": "4.99",
            },
            {
                "name": "coverage",
                "version": "4.5.3",
                "latest_version": "7.4.4",
                "libyear": "5.02",
            },
            {
                "name": "watchdog",
                "version": "0.9.0",
                "latest_version": "4.0.0",
                "libyear": "5.45",
            },
            {
                "name": "argh",
                "version": "0.26.2",
                "latest_version": "0.31.2",
                "libyear": "7.71",
            },
        ],
        "libyears_behind": "167.16",
    }
