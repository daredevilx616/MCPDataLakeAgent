# MCP Data Lake Copilot

This repo centers on two pieces so you can iterate locally:

1. **SQLite analytics lake** – bundled sample data (customers, products, orders, payments) stored at `data/sales.db`.
2. **Local MCP server + web UI** – `src/mcp_server.py` exposes tools for schema inspection, querying, and mutations, while `src/web_app.py` provides the sticky chat interface with multi-database connector controls.

## Quick start

```bash
# 1. Install deps (SQLite is bundled with Python)
python3 -m pip install --user --break-system-packages openai mcp flask python-dotenv

# 2. Configure secrets (not checked into git)
cp .env.example .env
# edit .env with your OpenAI key and optional default model

# 3. Launch the browser experience
python3 src/web_app.py
```

Notes:
- The agent reads the schema before the first call and instructs the model to return JSON with `sql` and `rationale`. Results appear in the chat bubble with tables and multi-statement blocks.
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

Open `http://127.0.0.1:5000` once Flask is running. The dark-themed page includes:
- A left nav rail to toggle the connector drawer
- Multi-database connector forms (SQLite, PostgreSQL, MySQL, MS SQL, MongoDB) plus an “active DB” selector
- A chat workspace that mirrors the CLI output (generated SQL, rationale, tabular rows)

Connector changes are written locally to `connectors.json` (gitignored) and mirrored into `mcp.json` so MCP-aware clients stay aligned. The Flask app also reads `.env`, so keep that file present locally.

## Wiring an OpenAI agent to the MCP server

Configure an OpenAI "Models" agent (Assistants API or Responses API with MCP support) and pass `mcp.json` in your IDE/tooling so the agent can call `analytics-sqlite`.

At runtime, the AI agent can:
- call `describe_schema` to scope available tables,
- plan SQL via the LLM,
- send the SQL to `run_sql` to get live results, and
- answer the user with both rationale and data.

That’s enough to iterate locally before adding a web UI or additional MCP tools.
