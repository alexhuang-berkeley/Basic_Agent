"""SQLite database query helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Tuple, Dict


def execute_query(db_path: Path, query: str, limit: int = 100) -> Tuple[int, List[Dict[str, object]]]:
    """Execute a SQL query with a row limit.

    Returns the total number of rows the query would return and a limited
    subset of rows as dictionaries.
    """
    conn = sqlite3.connect(db_path)
    try:
        count_sql = f"SELECT COUNT(*) FROM ({query}) as sub"
        row_count = conn.execute(count_sql).fetchone()[0]

        limited_query = f"{query} LIMIT {limit}"
        cur = conn.execute(limited_query)
        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()

    return row_count, rows


def format_rows(row_count: int, rows: List[Dict[str, object]], limit: int) -> str:
    """Format rows for display in the chat response."""
    lines = [f"Row count: {row_count}"]
    for row in rows:
        parts = [f"{k}={v}" for k, v in row.items()]
        lines.append(" | ".join(parts))
    if row_count > len(rows):
        lines.append(f"... {row_count - len(rows)} more rows")
    return "\n".join(lines)
