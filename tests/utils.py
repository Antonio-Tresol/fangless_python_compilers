import sys
from pathlib import Path


def add_package_from_parent_to_context(package_name: str) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / package_name))
