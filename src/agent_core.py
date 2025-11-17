from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

from typing import Any, List, Sequence

from datetime import date, timedelta

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "gpt-4o-mini"

load_dotenv(BASE_DIR / ".env")


def resolve_db_path() -> Path:
    mcp_config = BASE_DIR / "mcp.json"
    if mcp_config.exists():
        try:
            data = json.loads(mcp_config.read_text())
            server = data.get("mcpServers", {}).get("analytics-sqlite", {})
            env = server.get("env", {})
            candidate = env.get("MCP_DB_PATH")
            if candidate:
                path = Path(candidate)
                if not path.is_absolute():
                    path = (BASE_DIR / path).resolve()
                return path
        except json.JSONDecodeError:
            pass
    return (BASE_DIR / "data" / "sales.db").resolve()

def get_model_name() -> str:
    return os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)


def create_client() -> OpenAI:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Define it in the environment or .env file.")
    return OpenAI()


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(resolve_db_path())


def format_schema(cursor: sqlite3.Cursor) -> str:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    lines: List[str] = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        cols = ", ".join(f"{col[1]} ({col[2]})" for col in cursor.fetchall())
        lines.append(f"{table}: {cols}")
    return "\n".join(lines)


def rows_to_dicts(cursor: sqlite3.Cursor, rows: Sequence[Sequence[Any]]) -> List[dict[str, Any]]:
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def generate_sql(question: str, schema: str, client: OpenAI) -> dict[str, Any]:
    completion = client.chat.completions.create(
        model=get_model_name(),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data analyst that writes safe, read-only SQLite-compatible SQL. "
                    "Only reference tables present in the provided schema summary."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Schema:\n" + schema + "\n\n"
                    "Instruction: Generate a single SQL query that answers the question."
                    " Respond with a JSON object containing keys 'sql' and 'rationale'.\n"
                    f"Question: {question}"
                ),
            },
        ],
    )
    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty response")
    return json.loads(content)


def split_statements(sql: str) -> list[str]:
    statements: list[str] = []
    buffer = ""
    for char in sql:
        buffer += char
        if sqlite3.complete_statement(buffer):
            candidate = buffer.strip()
            if candidate:
                statements.append(candidate.rstrip(";"))
            buffer = ""
    if buffer.strip():
        statements.append(buffer.strip().rstrip(";"))
    return statements


def execute_sql(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    cursor = conn.cursor()
    statements = split_statements(sql)
    if not statements:
        raise RuntimeError("No SQL to execute.")
    result_sets: list[dict[str, Any]] = []
    for statement in statements:
        normalized = statement.lstrip().lower()
        cursor.execute(statement)
        if normalized.startswith(("select", "with", "pragma", "explain")):
            rows = cursor.fetchall()
            result_sets.append(
                {
                    "statement": statement,
                    "rows": rows_to_dicts(cursor, rows),
                    "row_count": len(rows),
                }
            )
        else:
            conn.commit()
            result_sets.append(
                {
                    "statement": statement,
                    "rows": [],
                    "row_count": cursor.rowcount if cursor.rowcount is not None else 0,
                }
            )
    if not result_sets:
        result_sets.append({"statement": statements[-1], "rows": [], "row_count": 0})
    return result_sets


def answer_question(question: str) -> dict[str, Any]:
    conn = get_connection()
    try:
        schema = format_schema(conn.cursor())
        client = create_client()
        response = generate_sql(question, schema, client)
        sql = response.get("sql", "").strip()
        rationale = response.get("rationale", "").strip()
        if not sql:
            raise RuntimeError("Model response missing SQL")
        return {
            "sql": sql,
            "rationale": rationale,
            "result_sets": execute_sql(conn, sql),
        }
    finally:
        conn.close()
