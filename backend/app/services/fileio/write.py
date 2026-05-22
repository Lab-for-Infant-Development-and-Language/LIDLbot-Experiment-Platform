import csv
from pathlib import Path
from .read import load_file

def append_csv_row(file_path, row, fieldnames=None):
    file_exists = file_path.is_file()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row)

def update_csv_row(file_path, row_index, updates):
    rows = load_file(file_path)
    if not rows:
        raise ValueError("CSV file empty. No rows to update.")
    
    target_row = rows[row_index]
    valid_fields = set(target_row.keys())
    invalid_fields = (set(updates.keys()) - valid_fields)

    if invalid_fields:
        invalid_str = ", ".join(sorted(invalid_fields))
        raise KeyError(f"Invalid CSV fields: {invalid_str}")
    
    target_row.update(updates)
    fieldnames = list(rows[0].keys())

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)