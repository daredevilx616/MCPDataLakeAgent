# Terminal BI Agent with MCP + SQLite

This repo wires up three pieces so you can iterate locally:

1. **SQLite analytics lake** – lightweight schema with customers, products, orders, and payments (see `src/db_setup.py`).
2. **Terminal AI agent** – `src/cli_agent.py` turns natural-language questions into SQL via OpenAI, executes the query, and prints the result set.
3. **Local MCP server** – `src/mcp_server.py` exposes read-only tools (`describe_schema`, `run_sql`) that point at the same SQLite file. `mcp.json` wires it up with stdio transport so any MCP-compatible client can attach.

## Quick start

```bash
# 1. Install deps (SQLite is bundled with Python)
python3 -m pip install --user --break-system-packages openai mcp flask python-dotenv

# 2. Configure secrets (not checked into git)
cp .env.example .env
# edit .env with your OpenAI key and optional default model

# 3. (Re)build the sample DB
python3 src/db_setup.py

# 4. Ask questions from the terminal
python3 src/cli_agent.py "What were total Q4 revenues by region?"
# or start an interactive loop
python3 src/cli_agent.py
```

Notes:
- The agent reads the schema before the first call and instructs the model to return JSON with `sql` and `rationale`. Results are rendered in a simple ASCII table.
- Set `OPENAI_MODEL` if you want something other than `gpt-4o-mini`.

## Running the MCP server

```bash
# from the repo root
python3 src/mcp_server.py
```

The server defaults to stdio transport and the database path from `MCP_DB_PATH` (see `mcp.json`). Once running, point your MCP client/IDE at this repo – most tools auto-pick up `mcp.json` in the workspace.

Exposed tools:
- `describe_schema()` – returns table/column metadata so the agent can ground itself.
- `run_sql(query)` – executes read-only SELECT/CTE statements.
- `create_table(schema_sql)` – runs raw DDL statements so you can spin up new tables based on an input schema.
- `insert_row(table, values)` – insert one row provided as a JSON object.
- `update_rows(table, updates, where_clause, params)` – update data with a simple WHERE filter.
- `delete_rows(table, where_clause, params)` – delete rows with a simple WHERE filter.

## Web UI

Prefer a browser flow? Fire up the Flask app:

```bash
# from the repo root
python3 src/web_app.py
```

Then open `http://127.0.0.1:5000`. The dark-themed page now includes:
- A left nav rail to toggle the connector drawer
- Multi-database connector forms (SQLite, PostgreSQL, MySQL, MS SQL, MongoDB) plus an “active DB” selector
- A chat workspace that mirrors the CLI output (generated SQL, rationale, tabular rows)

Connector changes are written locally to `connectors.json` (gitignored) and mirrored into `mcp.json` so MCP-aware clients stay aligned. The Flask app also reads `.env`, so keep that file present locally.

## Wiring an OpenAI agent to the MCP server

1. Use the CLI agent for turnkey experimentation, or
2. Configure an OpenAI "Models" agent (Assistants API or Responses API with MCP support) and pass `mcp.json` in your IDE/tooling so the agent can call `analytics-sqlite`.

At runtime, the AI agent can:
- call `describe_schema` to scope available tables,
- plan SQL via the LLM,
- send the SQL to `run_sql` to get live results, and
- answer the user with both rationale and data.

That’s enough to iterate locally before adding a web UI or additional MCP tools.
