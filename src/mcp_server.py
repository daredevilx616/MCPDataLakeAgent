from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("MCP_DB_PATH", BASE_DIR / "data" / "sales.db"))

server = FastMCP(
    name="analytics-sqlite",
    instructions=(
        "Expose read-only access to the sample analytics database."
        " Only run SELECT/CTE queries against the configured SQLite file."
    ),
)

def query_db(sql: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@server.tool(name="describe_schema", description="Return a summary of available tables and columns.")
def describe_schema(_: Context | None = None) -> list[dict[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    summary: list[dict[str, str]] = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = ", ".join(f"{col['name']} ({col['type']})" for col in cursor.fetchall())
        summary.append({"table": table, "columns": columns})
    conn.close()
    return summary

@server.tool(name="run_sql", description="Execute a read-only SQL query against the analytics DB.")
def run_sql(query: str, context: Context | None = None) -> list[dict[str, Any]]:
    normalized = query.strip().lower()
    if not normalized.startswith(("select", "with", "pragma")):
        raise ValueError("Only read-only SELECT/CTE statements are allowed")
    if any(keyword in normalized for keyword in ("insert", "update", "delete", "drop", "alter")):
        raise ValueError("Mutating statements are blocked")
    if context:
        context.info(f"Running query: {query}")
    return query_db(query)

if __name__ == "__main__":
    server.run("stdio")
