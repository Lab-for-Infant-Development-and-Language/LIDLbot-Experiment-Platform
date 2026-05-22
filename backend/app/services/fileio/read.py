import csv
import json
from pathlib import Path
from app.core.exceptions import UnsupportedFileType

def load_file(file_path):
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: '{file_path}'.")

    match file_path.suffix.lower():
        case ".json":
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        case ".csv":
            with open(file_path, newline="", encoding="utf-8") as file:
                return list(csv.DictReader(file))
        case _:
            raise UnsupportedFileType(f"Unsupported file type: '{file_path.suffix}'.")