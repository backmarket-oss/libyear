import logging
import os
import re

REQUIREMENT_NAME_RE = r"^([^=><]+)"
REQUIREMENT_VERSION_LT_RE = r"<([^$,]*)"
REQUIREMENT_VERSION_LTE_RE = r"[<=]=([^$,]*)"

logger = logging.getLogger(__name__)


def get_requirement_name_and_version(requirement):
    no_requirement = None, None, None
    # Remove comments if they are on the same line
    requirement = requirement.split()[0].strip()
    if not requirement:
        logger.warning("Requirement not found")
        return no_requirement

    name = re.findall(REQUIREMENT_NAME_RE, requirement)
    if not name:
        logger.warning("Name not found in the requirement")
        return no_requirement

    version = re.findall(REQUIREMENT_VERSION_LTE_RE, requirement)
    version_lt = re.findall(REQUIREMENT_VERSION_LT_RE, requirement)
    if not version_lt and not version:
        logger.warning("version and latest version not found in the requirement")
        return no_requirement

    if version:
        return name[0], version[0], None

    return name[0], None, version_lt[0]


def get_requirement_files(path_or_file):
    if os.path.isfile(path_or_file):
        yield path_or_file
        return

    for path, _, files in os.walk(path_or_file):
        for name in files:
            yield os.path.join(path, name)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == ""
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
        or line.startswith("--")
    )


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path).readlines() as lines:
            requirements.update(line.strip() for line in lines if is_requirement(line))
    return list(requirements)


def calculate_libyear(days: int) -> str:
    """
    Calculation of the libyear
    """
    return str(round(days / 365, 2))
