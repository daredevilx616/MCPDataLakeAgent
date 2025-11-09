from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from agent_core import answer_question

BASE_DIR = Path(__file__).resolve().parent.parent
MCP_CONFIG_PATH = BASE_DIR / "mcp.json"
CONNECTORS_PATH = BASE_DIR / "connectors.json"
SERVER_KEY = "analytics-sqlite"

DEFAULT_CONNECTORS: dict[str, Any] = {
    "active": "sqlite",
    "sqlite": {"path": "./data/sales.db"},
    "postgresql": {"host": "", "port": "5432", "database": "", "username": "", "password": ""},
    "mysql": {"host": "", "port": "3306", "database": "", "username": "", "password": ""},
    "mssql": {"server": "", "database": "", "username": "", "password": ""},
    "mongodb": {"uri": "", "database": "", "collection": ""},
}

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


def load_mcp_config() -> dict[str, Any]:
    if MCP_CONFIG_PATH.exists():
        with MCP_CONFIG_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return {"mcpServers": {}}


def save_mcp_config(config: dict[str, Any]) -> None:
    MCP_CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")


def extract_db_path(config: dict[str, Any]) -> str:
    server = config.get("mcpServers", {}).get(SERVER_KEY, {})
    env = server.get("env", {})
    return env.get("MCP_DB_PATH", "")


def load_connectors() -> dict[str, Any]:
    if CONNECTORS_PATH.exists():
        with CONNECTORS_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(json.dumps(DEFAULT_CONNECTORS))


def save_connectors(connectors: dict[str, Any]) -> None:
    CONNECTORS_PATH.write_text(json.dumps(connectors, indent=2), encoding="utf-8")


def sync_mcp_env(connectors: dict[str, Any]) -> None:
    config = load_mcp_config()
    servers = config.setdefault("mcpServers", {})
    server = servers.setdefault(
        SERVER_KEY,
        {
            "command": "python3",
            "args": ["src/mcp_server.py"],
            "env": {},
            "transport": {"type": "stdio"},
        },
    )
    env = server.setdefault("env", {})
    sqlite_path = connectors.get("sqlite", {}).get("path") or "./data/sales.db"
    env["MCP_DB_PATH"] = sqlite_path
    env["ACTIVE_DB"] = connectors.get("active", "sqlite")
    for key, value in connectors.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                env_key = f"{key.upper()}_{sub_key.upper()}"
                env[env_key] = sub_value
    save_mcp_config(config)


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/query")
def api_query():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Question is required."}), 400
    try:
        payload = answer_question(question)
        return jsonify({"question": question, **payload})
    except Exception as exc:  # pragma: no cover - surfaced to client
        return jsonify({"error": str(exc)}), 500


@app.get("/api/mcp")
def get_mcp_config():
    config = load_mcp_config()
    return jsonify({"db_path": extract_db_path(config), "config": config})


@app.post("/api/mcp")
def update_mcp_config():
    config = load_mcp_config()
    data = request.get_json(silent=True) or {}
    db_path = (data.get("db_path") or "").strip()
    if not db_path:
        return jsonify({"error": "Database path is required."}), 400

    servers = config.setdefault("mcpServers", {})
    server = servers.setdefault(
        SERVER_KEY,
        {
            "command": "python3",
            "args": ["src/mcp_server.py"],
            "env": {},
            "transport": {"type": "stdio"},
        },
    )
    env = server.setdefault("env", {})
    env["MCP_DB_PATH"] = db_path
    save_mcp_config(config)
    return jsonify({"db_path": db_path, "config": config})


@app.get("/api/connectors")
def get_connectors():
    connectors = load_connectors()
    return jsonify(connectors)


@app.post("/api/connectors")
def update_connectors():
    data = request.get_json(silent=True) or {}
    connectors = load_connectors()

    connectors["active"] = (data.get("active") or connectors.get("active") or "sqlite").strip()
    for key in ("sqlite", "postgresql", "mysql", "mssql", "mongodb"):
        incoming = data.get(key)
        if isinstance(incoming, dict):
            target = connectors.setdefault(key, {})
            for field, value in incoming.items():
                if isinstance(value, str):
                    target[field] = value.strip()
                else:
                    target[field] = value

    save_connectors(connectors)
    sync_mcp_env(connectors)
    return jsonify(connectors)


if __name__ == "__main__":
    app.run(debug=True)
