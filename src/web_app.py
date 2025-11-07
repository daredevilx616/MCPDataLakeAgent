from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from agent_core import answer_question

BASE_DIR = Path(__file__).resolve().parent.parent
MCP_CONFIG_PATH = BASE_DIR / "mcp.json"
SERVER_KEY = "analytics-sqlite"

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


if __name__ == "__main__":
    app.run(debug=True)
