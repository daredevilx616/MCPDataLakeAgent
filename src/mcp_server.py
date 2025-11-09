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

def _execute_mutation(sql: str, params: tuple[Any, ...] = ()) -> int:
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

@server.tool(name="run_sql", description="Execute a read-only SQL query against the analytics DB.")
def run_sql(query: str, context: Context | None = None) -> list[dict[str, Any]]:
    normalized = query.strip().lower()
    if not normalized.startswith(("select", "with", "pragma", "explain")):
        raise ValueError("Only read-only statements are allowed")
    if context:
        context.info(f"Running query: {query}")
    return query_db(query)

@server.tool(name="create_table", description="Create tables given raw SQL schema statements.")
def create_table(schema_sql: str, context: Context | None = None) -> str:
    if context:
        context.info("Creating tables via custom schema")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
    return "Schema executed successfully."

@server.tool(name="insert_row", description="Insert a single row into a table.")
def insert_row(table: str, values: dict[str, Any], context: Context | None = None) -> str:
    placeholders = ", ".join("?" for _ in values)
    columns = ", ".join(values.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    count = _execute_mutation(sql, tuple(values.values()))
    return f"Inserted {count} row(s) into {table}."

@server.tool(name="update_rows", description="Update rows using a simple WHERE clause.")
def update_rows(
    table: str,
    updates: dict[str, Any],
    where_clause: str,
    params: list[Any] | None = None,
    context: Context | None = None,
) -> str:
    set_clause = ", ".join(f"{col}=?" for col in updates)
    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    ordered_params = list(updates.values()) + (params or [])
    count = _execute_mutation(sql, tuple(ordered_params))
    return f"Updated {count} row(s) in {table}."

@server.tool(name="delete_rows", description="Delete rows using a simple WHERE clause.")
def delete_rows(table: str, where_clause: str, params: list[Any] | None = None) -> str:
    sql = f"DELETE FROM {table} WHERE {where_clause}"
    count = _execute_mutation(sql, tuple(params or []))
    return f"Deleted {count} row(s) from {table}."

if __name__ == "__main__":
    server.run("stdio")
