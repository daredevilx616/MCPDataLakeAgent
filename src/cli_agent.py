from __future__ import annotations

import argparse
import sqlite3
from typing import Any, List

from openai import OpenAI

from agent_core import DB_PATH, create_client, execute_sql, format_schema, generate_sql

def tabulate(rows: List[dict[str, Any]]) -> str:
    if not rows:
        return "(no rows returned)"
    columns = rows[0].keys()
    col_widths = {col: len(col) for col in columns}
    for row in rows:
        for col, value in row.items():
            col_widths[col] = max(col_widths[col], len(str(value)))
    header = " | ".join(f"{col:{col_widths[col]}}" for col in columns)
    separator = "-+-".join("-" * col_widths[col] for col in columns)
    data_lines = [
        " | ".join(f"{str(row[col]):{col_widths[col]}}" for col in columns) for row in rows
    ]
    return "\n".join([header, separator, *data_lines])

def handle_question(question: str, conn: sqlite3.Connection, schema: str, client: OpenAI) -> None:
    response = generate_sql(question, schema, client)
    sql = response.get("sql", "").strip()
    rationale = response.get("rationale", "").strip()
    if not sql:
        raise RuntimeError("Model response missing SQL")
    print("\n--- Generated SQL ---\n" + sql)
    if rationale:
        print("\n--- Rationale ---\n" + rationale)
    try:
        results, count = execute_sql(conn, sql)
    except sqlite3.DatabaseError as err:
        print(f"\nQuery failed: {err}")
        return
    print(f"\n--- Results ({count} rows) ---")
    print(tabulate(results))

def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal BI agent powered by OpenAI")
    parser.add_argument(
        "question",
        nargs="?",
        help="Optional one-off question. If omitted, starts an interactive shell.",
    )
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    schema = format_schema(conn.cursor())
    client = create_client()

    try:
        if args.question:
            handle_question(args.question, conn, schema, client)
            return

        print("Connected to", DB_PATH)
        print("Type 'exit' or Ctrl+C to quit.")
        while True:
            try:
                question = input("\nAsk a question> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break
            if question.lower() in {"exit", "quit"}:
                break
            if not question:
                continue
            handle_question(question, conn, schema, client)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
