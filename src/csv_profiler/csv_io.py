import csv
from pathlib import Path
from typing import Union
from io import StringIO


def read_csv(filepath):
    """
    Read CSV data from a file path.

    Args:
        filepath: Path to CSV file

    Returns:
        List of rows as dictionaries
    """
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        return read_csv_text(csvfile.read())


def read_csv_text(csv_text):
    """
    Read CSV data from a text string.

    Args:
        csv_text: CSV content as string

    Returns:
        List of rows as dictionaries
    """
    csvfile = StringIO(csv_text)
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    return rows


def read_csv_file(path: Union[str, Path]):
    return read_csv(str(path))
