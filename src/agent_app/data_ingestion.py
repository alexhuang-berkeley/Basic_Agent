"""CSV ingestion and schema extraction utilities."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Dict
import csv


def ingest_csv_directory(csv_dir: Path, db_path: Path) -> List[Dict[str, List[str]]]:
    """Load all CSV files from csv_dir into a SQLite database at db_path.

    Returns a list of schema dictionaries with table names and columns.
    """
    conn = sqlite3.connect(db_path)
    schema_info = []
    for csv_file in csv_dir.glob("*.csv"):
        table_name = csv_file.stem
        with open(csv_file, newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)
            columns_clause = ", ".join(f'"{col}" TEXT' for col in headers)
            conn.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_clause});')
            for row in reader:
                placeholders = ", ".join("?" for _ in row)
                conn.execute(
                    f'INSERT INTO "{table_name}" VALUES ({placeholders});',
                    row,
                )
        schema_info.append({"name": table_name, "columns": headers})
    conn.commit()
    conn.close()
    return schema_info


def schema_metadata(csv_dir: Path, db_path: Path) -> str:
    """Ingest CSVs, return formatted schema string for prompts."""
    schema = ingest_csv_directory(csv_dir, db_path)
    from .prompts import schema_prompt

    return schema_prompt(schema)
